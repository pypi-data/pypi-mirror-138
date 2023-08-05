import sys

if sys.platform == "win32":
    from .WatchRestart_ReadDirectoryChangesW import WatchRestart
elif sys.platform == "darwin":
    from .WatchRestart_FSEvents import WatchRestart
else:
    from .WatchRestart_inotify import WatchRestart
