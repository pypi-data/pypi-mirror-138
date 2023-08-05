import logging

import win32process, win32job, win32api

logger = logging.getLogger("WatchRestart")


hjob = None


def killJob():
    global hjob
    if hjob is not None:
        win32api.CloseHandle(hjob)
        hjob = None


def restartJob(job):
    global hjob
    killJob()

    command = " ".join(job)
    cwd = None
    dwCreationFlags = win32process.CREATE_SUSPENDED

    startup = win32process.STARTUPINFO()
    (hProcess, hThread, processId, threadId) = win32process.CreateProcess(
        None, command, None, None, True, dwCreationFlags, None, cwd, startup
    )

    hjob = win32job.CreateJobObject(None, "")
    extended_info = win32job.QueryInformationJobObject(hjob, win32job.JobObjectExtendedLimitInformation)
    extended_info["BasicLimitInformation"]["LimitFlags"] = win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    win32job.SetInformationJobObject(hjob, win32job.JobObjectExtendedLimitInformation, extended_info)
    win32job.AssignProcessToJobObject(hjob, hProcess)

    win32process.ResumeThread(hThread)
    win32api.CloseHandle(hProcess)
    win32api.CloseHandle(hThread)
