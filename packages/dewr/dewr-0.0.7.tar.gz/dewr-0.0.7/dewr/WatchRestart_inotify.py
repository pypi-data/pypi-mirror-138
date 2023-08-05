"""
https://github.com/chrisjbillington/inotify_simple

"""

import os, glob, re, logging, select
from struct import unpack_from
from ctypes import CDLL, get_errno
from errno import EINTR
from .JobControl import JobControl

logger = logging.getLogger("WatchRestart")


def _libc_call(function, *args):
    while True:
        rc = function(*args)
        if rc != -1:
            return rc
        errno = get_errno()
        if errno != EINTR:
            raise OSError(errno, os.strerror(errno))


_libc = CDLL("libc.so.6", use_errno=True)

IN_MODIFY = 0x00000002  # file was modified

IN_MOVED_FROM = 0x00000040  # file was moved from X
IN_MOVED_TO = 0x00000080  # file was moved to Y
IN_CREATE = 0x00000100  # subfile was created
IN_DELETE = 0x00000200  # subfile was deleted
IN_DELETE_SELF = 0x00000400  # self was deleted
IN_MOVE_SELF = 0x00000800  # self was moved

IN_UNMOUNT = 0x00002000  # backing fs was unmounted
IN_Q_OVERFLOW = 0x00004000  # event queue overflowed
IN_IGNORED = 0x00008000  # file was ignored

IN_EXCL_UNLINK = 0x04000000  # exclude events on unlinked objects
IN_ISDIR = 0x40000000  # event occurred against dir


class WatchRestart:
    def __init__(self, dirs, excludePattern, job):
        self.dirs = dirs
        self.exclude = re.compile(excludePattern)
        self.job = job
        self.ctl = JobControl(job)
        self.ep = None
        self.fd = None
        self.wd2scope = {}

        self.run()

    def rebuild(self):
        while True:
            logger.debug("REBUILD_BEGIN")
            self.cleanup()
            if self.reallyRebuild():
                logger.debug("REBUILD_OK")
                return
            else:
                self.cleanup()
                logger.debug("REBUILD_FAIL_THEN_DELAY")
                self.ctl.sleep(15)

    def cleanup(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        if self.ep is not None:
            self.ep.close()
            self.ep = None
        self.wd2scope = {}

    def reallyRebuild(self):
        self.fd = _libc_call(_libc.inotify_init1, os.O_CLOEXEC | os.O_NONBLOCK)
        self.ep = select.epoll()
        # 默认是水平触发
        self.ep.register(self.fd, select.EPOLLIN | select.EPOLLPRI | select.EPOLLERR)
        mask = (
            IN_MODIFY
            | IN_MOVED_FROM
            | IN_MOVED_TO
            | IN_CREATE
            | IN_DELETE
            | IN_DELETE_SELF
            | IN_MOVE_SELF
            | IN_UNMOUNT
            | IN_Q_OVERFLOW
            | IN_IGNORED
            | IN_EXCL_UNLINK
        )

        for dir in self.dirs:
            try:
                wd = _libc_call(_libc.inotify_add_watch, self.fd, os.fsencode(dir), mask)
                logger.debug("WATCH_RECURSIVE: %s", dir)
                self.wd2scope[wd] = ""
                for subdir in glob.glob(dir + "/**/", recursive=True):
                    subdir = subdir[:-1]
                    scope = subdir[len(dir) + 1 :] + "/"
                    excluded = self.exclude.search(scope) is not None
                    logger.debug("SUBDIR_SCOPE: %s -> %s | excluded=%s", subdir, scope, excluded)
                    if excluded:
                        continue
                    try:
                        wd = _libc_call(_libc.inotify_add_watch, self.fd, os.fsencode(subdir), mask)
                        self.wd2scope[wd] = scope
                    except FileNotFoundError:
                        logger.error("SUBDIR_NOT_FOUND: %s", subdir)
            except FileNotFoundError:
                logger.error("WATCH_TARGET_MUST_EXIST: %s", dir)
                return False

        return True

    def run(self):
        self.rebuild()
        buf = b""
        while True:
            logger.debug("WAIT_READ")
            events = self.ep.poll(self.ctl.timeout)
            needRebuild = False
            hasValidChange = False
            if events:
                try:
                    buf += os.read(self.fd, 1024)
                    logger.debug("READ: %d", len(buf))
                    pos = 0
                    # 对缓冲区做解析
                    while pos + 17 <= len(buf):
                        wd, mask, cookie, nameLen = unpack_from("iIII", buf, pos)
                        pos += 16 + nameLen
                        name = os.fsdecode(buf[pos - nameLen : buf.index(b"\x00", pos - nameLen)])
                        # 处理解析出来的一项
                        logger.debug("EVENT: %d %x %d %s", wd, mask, cookie, nameLen)
                        if mask & (IN_ISDIR | IN_Q_OVERFLOW):
                            needRebuild = True
                        subdirScoped = self.wd2scope[wd]
                        file = subdirScoped + name
                        excluded = self.exclude.search(file) is not None
                        logger.debug("CHANGE_FOUND: excluded=%s %x %s", excluded, mask, file)
                        if not excluded:
                            logger.debug("VALID_CHANGE: %x %s", mask, file)
                            hasValidChange = True
                    # 删除已经解析过的缓冲区
                    buf = buf[pos:]
                except BlockingIOError:
                    logger.error("BlockingIOError")
            if needRebuild:
                self.rebuild()
            if events:
                if hasValidChange:
                    self.ctl.onValidChange()
                else:
                    self.ctl.onExcludedChange()
            else:
                self.ctl.onTimer()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s")
    WatchRestart([".", "tmp2"], r"\.(?:pid|log)$", ["sh", "sleep66.sh"])
