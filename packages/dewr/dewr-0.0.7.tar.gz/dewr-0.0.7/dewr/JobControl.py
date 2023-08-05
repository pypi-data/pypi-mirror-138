import sys, time, logging

if sys.platform == "win32":
    from .JobControl_win32 import killJob, restartJob
else:
    from .JobControl_posix import killJob, restartJob

logger = logging.getLogger("JobControl")

intervalTable = {
    "WAIT_CHANGE": 1,
    "WILL_CLEANUP": 0.05,
    "WILL_RESTART": 0.05,
}

# 实现清理后短暂延迟再重启的状态机逻辑
class JobControl:
    def __init__(self, job):
        self.job = job
        # WAIT_CHANGE WILL_CLEANUP WILL_RESTART
        # 启动时启动作业
        self.state = "WILL_RESTART"
        self.timeout = intervalTable[self.state]
        self.prevState = self.state
        self.timerStartTime = time.monotonic()

    def modifyState(self, s):
        self.prevState = self.state
        self.state = s
        self.timeout = intervalTable[s]
        self.timerStartTime = time.monotonic()
        logger.debug("MODIFY_STATE: %s -> %s", self.prevState, self.state)

    # 返回新的 timeout
    def onValidChange(self):
        # 一直发现一直推迟
        self.modifyState("WILL_CLEANUP")
        # 调用方会重置定时器
        return intervalTable[self.state]

    # 外部调用它是为了获得新的阻塞超时
    def onExcludedChange(self):
        if self.state != "WAIT_CHANGE":
            self.timeout = max(0.001, (self.timerStartTime + intervalTable[self.state]) - time.monotonic())
            logger.debug("onExcludedChange_DECREASE_INTERVAL")
            # 调用方会重置定时器
            return self.timeout

    # 返回 None 或者新的 timeout
    def onTimer(self):
        if self.state == "WILL_CLEANUP":
            # 按照约定，由调用方维护定时器，所以这里不检测时间间隔
            elapsed = time.monotonic() - self.timerStartTime
            logger.info("DO_CLEANUP: after %.3fs", elapsed)
            # assert elapsed >= intervalTable[self.state]
            killJob()
            self.modifyState("WILL_RESTART")
            return intervalTable[self.state]
        elif self.state == "WILL_RESTART":
            elapsed = time.monotonic() - self.timerStartTime
            logger.info("DO_RESTART: after %.3fs", elapsed)
            # assert elapsed >= intervalTable[self.state]
            restartJob(self.job)
            self.modifyState("WAIT_CHANGE")
            return intervalTable[self.state]

    # 休眠辅助函数，为了能检测出 Ctrl+C
    def sleep(self, seconds):
        for i in range(seconds):
            time.sleep(1)
