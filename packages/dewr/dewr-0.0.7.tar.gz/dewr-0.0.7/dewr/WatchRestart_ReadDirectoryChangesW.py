import re, logging
import win32file, win32con, pywintypes
from .JobControl import JobControl

logger = logging.getLogger("WatchRestart")


FILE_LIST_DIRECTORY = 0x0001
FILE_NOTIFY_CHANGE_CREATION = 0x00000040


class NeedRebuildError(Exception):
    pass


class WatchExit(BaseException):
    pass


class DirObj:
    def __init__(self, iocp, dir):
        super().__init__()
        self.dir = dir
        self.hdir = None
        self.hdir = win32file.CreateFile(
            dir,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS | win32con.FILE_FLAG_OVERLAPPED,
            None,
        )
        win32file.CreateIoCompletionPort(self.hdir, iocp.hiocp, 0, 0)

    def close(self):
        if self.hdir is not None:
            win32file.CloseHandle(self.hdir)
        self.hdir = None


idAlloc = 0


class IOCPRequest:
    def __init__(self):
        global idAlloc
        idAlloc += 1
        self.id = idAlloc
        self.overlapped = pywintypes.OVERLAPPED()
        self.overlapped.object = self.id


class IOCPReadDirectoryChangesW(IOCPRequest):
    def __init__(self, dirObj, exclude):
        super().__init__()
        self.dirObj = dirObj
        self.exclude = exclude
        self.buf = win32file.AllocateReadBuffer(4096)
        self.isValidChange = None

    def post(self, iocp):
        self.isValidChange = None
        try:
            logger.debug("win32file.ReadDirectoryChangesW: %s", self.dirObj.hdir)
            win32file.ReadDirectoryChangesW(
                self.dirObj.hdir,
                self.buf,
                True,
                FILE_NOTIFY_CHANGE_CREATION
                | win32con.FILE_NOTIFY_CHANGE_FILE_NAME
                | win32con.FILE_NOTIFY_CHANGE_DIR_NAME
                | win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
                | win32con.FILE_NOTIFY_CHANGE_SECURITY
                | win32con.FILE_NOTIFY_CHANGE_SIZE
                | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
                self.overlapped,
            )
        except pywintypes.error as e:
            # 不是目录是文件  87  The parameter is incorrect.
            logger.error("WATCH_TARGET_LOST_WHEN_POST: %s %s", self.dirObj.dir, e)
            raise NeedRebuildError
        iocp.reqMap[self.id] = self

    def makeResult(self, nBytes):
        if nBytes == 0:
            # 缓冲区不够用
            logger.error("BUFFER_OVERFLOW: %s", self.dirObj.dir)
            self.isValidChange = True
            return
        results = win32file.FILE_NOTIFY_INFORMATION(self.buf, nBytes)
        for action, file in results:
            file = file.replace("\\", "/")
            excluded = self.exclude.search(file)
            logger.debug("CHANGE_FOUND: excluded=%s %d %s", excluded, action, file)
            if excluded:
                continue
            logger.debug("VALID_CHANGE: %d %s", action, file)
            self.isValidChange = True


class IOCP:
    def __init__(self):
        self.hiocp = win32file.CreateIoCompletionPort(win32file.INVALID_HANDLE_VALUE, 0, 0, 0)
        self.reqMap = {}

    def get(self, timeout):
        ms = int(timeout * 1000)
        (rc, nBytes, key, overlapped) = win32file.GetQueuedCompletionStatus(self.hiocp, ms)
        reqID = overlapped and overlapped.object or 0
        req = self.reqMap.pop(reqID, None)
        logger.debug("GetQueuedCompletionStatus: %d %d %d reqID=%s", rc, nBytes, key, reqID)
        if rc == 0:
            req.makeResult(nBytes)
            return req
        elif rc == 258:
            # 258 (0x102) The wait operation timed out.
            return None
        elif rc == 5:
            # Access is denied.
            # 意味着文件被删除
            logger.error("WATCH_TARGET_LOST_WHEN_GET: %s", req.dirObj.dir)
            raise NeedRebuildError
        elif rc == 995:
            # The I/O operation has been aborted because of either a thread exit or an application request.
            return None
        else:
            raise Exception(f"win32file.GetQueuedCompletionStatus: error {rc}")


class WatchRestart:
    def __init__(self, dirs, excludePattern, job):
        logger.info("INIT: %s %s %s", dirs, excludePattern, job)
        self.dirs = dirs
        self.exclude = re.compile(excludePattern)
        self.job = job
        self.ctl = JobControl(job)
        self.iocp = IOCP()
        self.dirObjs = []
        self.run()

    def fillDirObjs(self):
        for dir in self.dirs:
            while True:
                try:
                    dirObj = DirObj(self.iocp, dir)
                    self.dirObjs.append(dirObj)
                    break
                except pywintypes.error:
                    logger.error("WATCH_TARGET_MUST_EXIST: %s", dir)
                    self.ctl.sleep(5)

    def fillQueue(self):
        for dirObj in self.dirObjs:
            req = IOCPReadDirectoryChangesW(dirObj, self.exclude)
            req.post(self.iocp)

    def cleanupQueueForRebuild(self):
        logger.debug("CLEANUP_QUEUE_BEGIN: len(iocp.reqMap)=%d", len(self.iocp.reqMap))
        for req in self.iocp.reqMap.values():
            logger.debug("win32file.CancelIo(%s)", req.dirObj.hdir)
            win32file.CancelIo(req.dirObj.hdir)
        for i in range(len(self.iocp.reqMap)):
            self.iocp.get(0)
        logger.debug("CLEANUP_QUEUE_END: len(iocp.reqMap)=%d", len(self.iocp.reqMap))
        assert len(self.iocp.reqMap) == 0

    def cleanupDirObjs(self):
        for dirObj in self.dirObjs:
            dirObj.close()
        self.dirObjs.clear()

    def cleanup(self):
        if self.iocp is None:
            logger.info("NEED_NOT_CLEANUP")
            return
        logger.info("CLEANUP_BEGIN")
        self.cleanupQueueForRebuild()
        self.cleanupDirObjs()
        logger.info("CLEANUP_END")

    def rebuild(self):
        logger.info("REBUILD_BEGIN")
        self.cleanup()
        self.fillDirObjs()
        self.fillQueue()
        logger.info("REBUILD_OK")

    def loopGet(self):
        while True:
            req = self.iocp.get(self.ctl.timeout)
            if req:
                if req.isValidChange:
                    self.ctl.onValidChange()
                else:
                    self.ctl.onExcludedChange()
            else:
                self.ctl.onTimer()
            if req:
                req.post(self.iocp)

    def run(self):
        while True:
            try:
                self.rebuild()
                self.loopGet()
            except NeedRebuildError:
                self.cleanup()
                logger.info("NEED_REBUILD_LATER")
                self.ctl.sleep(15)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s")
    WatchRestart([".", "tmp"], r"\.(?:pid|log)$", ["busybox", "sh", "sleep66.sh"])
