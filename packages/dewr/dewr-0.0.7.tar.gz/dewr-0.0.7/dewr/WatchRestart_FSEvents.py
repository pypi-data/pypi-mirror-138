"""
https://github.com/gorakhargosh/watchdog/blob/master/src/watchdog/observers/fsevents2.py

"""

import sys, time, os, os.path, glob, queue, threading, re, logging
import AppKit, FSEvents, CoreFoundation
from .JobControl import JobControl


logger = logging.getLogger("WatchRestart")


RESTART_DELAY = 0.05


class WatchRestart:
    def __init__(self, dirs, excludePattern, job):
        self.dirs = dirs
        self.realDirs = [os.path.realpath(x) + "/" for x in dirs]
        self.exclude = re.compile(excludePattern)
        self.job = job
        self.ctl = JobControl(job)
        self.pool = AppKit.NSAutoreleasePool.alloc().init()
        self.runLoop = FSEvents.CFRunLoopGetCurrent()
        self.streamRef = None
        self.timer = None
        self.run()

    def destroyTimer(self):
        if self.timer is not None:
            CoreFoundation.CFRunLoopTimerInvalidate(self.timer)
            CoreFoundation.CFRunLoopRemoveTimer(self.runLoop, self.timer, FSEvents.kCFRunLoopDefaultMode)
            self.timer = None

    def resetTimer(self, timeout):
        self.destroyTimer()
        self.timer = CoreFoundation.CFRunLoopTimerCreate(None, 0, timeout, 0, 0, self.onTimer, None)
        CoreFoundation.CFRunLoopAddTimer(self.runLoop, self.timer, FSEvents.kCFRunLoopDefaultMode)

    def onTimer(self, timer, info):
        timeout = self.ctl.onTimer()
        if timeout is not None:
            self.resetTimer(timeout)

    def normalizeFile(self, file):
        for realDir in self.realDirs:
            if file.startswith(realDir):
                file = file[len(realDir) :]
                return file
        logger.error("normalizeFile_FAIL:", file)
        return file

    def onBatchEvent(self, streamRef, clientCallBackInfo, numEvents, eventPaths, eventFlags, eventIDs):
        found = False
        needRebuild = False
        for flag, file in zip(eventFlags, eventPaths):
            file = self.normalizeFile(file)
            excluded = self.exclude.search(file)
            logger.debug("CHANGE_FOUND: excluded=%s %x %s", excluded, flag, file)
            if excluded:
                continue
            logger.debug("VALID_CHANGE: %x %s", flag, file)
            found = True
            if flag & (
                FSEvents.kFSEventStreamEventFlagMount
                | FSEvents.kFSEventStreamEventFlagUnmount
                | FSEvents.kFSEventStreamEventFlagRootChanged
                | FSEvents.kFSEventStreamEventFlagMustScanSubDirs
            ):
                logger.info("NEED_REBUILD: %x %s", flag, file)
                needRebuild = True
        if needRebuild:
            self.rebuildLater()
            self.rebuild()
        if found:
            self.resetTimer(self.ctl.onValidChange())

    def rebuildLater(self):
        self.cleanup()
        logger.info("NEED_REBUILD_LATER")
        self.ctl.sleep(15)

    def cleanup(self):
        if self.streamRef is not None:
            FSEvents.FSEventStreamStop(self.streamRef)
            FSEvents.FSEventStreamInvalidate(self.streamRef)
            FSEvents.FSEventStreamRelease(self.streamRef)
            self.streamRef = None

    def rebuild(self):
        while True:
            try:
                self.reallyRebuild()
                return
            except Exception as e:
                logger.error("REBUILD_FAIL:", e)
                self.rebuildLater()

    def reallyRebuild(self):
        logger.info("REBUILD_BEGIN")
        self.cleanup()
        self.streamRef = FSEvents.FSEventStreamCreate(
            FSEvents.kCFAllocatorDefault,
            self.onBatchEvent,
            None,
            self.dirs,
            FSEvents.kFSEventStreamEventIdSinceNow,
            0.05,
            FSEvents.kFSEventStreamCreateFlagWatchRoot
            | FSEvents.kFSEventStreamCreateFlagUseCFTypes
            | FSEvents.kFSEventStreamCreateFlagFileEvents,
        )
        assert self.streamRef
        FSEvents.FSEventStreamScheduleWithRunLoop(self.streamRef, self.runLoop, FSEvents.kCFRunLoopDefaultMode)
        ok = FSEvents.FSEventStreamStart(self.streamRef)
        assert ok
        logger.info("REBUILD_OK")

    def run(self):
        self.rebuild()
        FSEvents.CFRunLoopRun()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s")
    WatchRestart([".", "tmp2"], r"\.(?:pid|log)$", ["sh", "sleep66.sh"])
