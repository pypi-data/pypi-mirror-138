import time, sys
import re
import os
import logging
import subprocess, signal
import atexit


logger = logging.getLogger("JobControl")

hjob = None


def killJob():
    global hjob

    if hjob is not None:
        # hjob.send_signal(signal.SIGINT)
        # poll() 返回 None 表示还没死
        if hjob.poll() is None:
            logger.info("killpg: %s", hjob.pid)
            os.killpg(hjob.pid, signal.SIGINT)
        hjob.wait(2)
        hjob = None


def restartJob(job):
    global hjob
    killJob()

    hjob = subprocess.Popen(job, start_new_session=True)
    logger.info("RESTART: pid=%d %s", hjob.pid, job)


def onExit():
    logger.info("EXIT_CLEANUP")
    killJob()


atexit.register(onExit)


def onSignalForExit(signalNumber, frame):
    logger.info("onSignalForExit: %d", signalNumber)
    sys.exit()


def onSIGCHLD(signalNumber, frame):
    global hjob
    logger.info("onSIGCHLD")
    if hjob is not None:
        ret = hjob.poll()
        logger.debug("onSIGCHLD_poll_got: %s", ret)
        # 正常退出时不去杀进程组
        hjob = None


"""
按 Ctrl+C 产生 SIGINT 默认处理会调用 atexit
默认的 SIGHUP 处理就打印一下 Hangup，不会调用 atexit
默认的 SIGTERM 处理就打印一下 Terminated，不会调用 atexit
按 Ctrl+\ 产生 SIGQUIT 信号，默认处理时打印 ^\Quit (core dumped) 然后产生一个 core 文件，不会调用 atexit
按 Ctrl+Z 产生 SIGSTOP 信号，只能由操作系统处理，打印 ^Z\n[1]+  Stopped 然后进程没死，进入 T 状态
发送 SIGCONT 信号可以使 T 进程恢复执行

所以得处理一些信号，执行 sys.exit()
"""
signal.signal(signal.SIGHUP, onSignalForExit)
signal.signal(signal.SIGINT, onSignalForExit)
signal.signal(signal.SIGTERM, onSignalForExit)
signal.signal(signal.SIGCHLD, onSIGCHLD)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s")
    restartJob(["sh", "dev1.sh"])
    time.sleep(999)
