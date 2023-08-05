import sys
import logging
import argparse
import dewr


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s")

    parser = argparse.ArgumentParser(description="dewr")
    parser.add_argument("-g", nargs="?", const=1, help="debug")
    parser.add_argument("-d", nargs="+", help="directories to watch")
    parser.add_argument("-e", help="exclude pattern")
    parser.add_argument("args", nargs="+", help="args of subprocess.Popen")

    args = parser.parse_args()

    print(args.g, "DDDD")
    if args.g is not None:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.args[0].endswith(".sh"):
        args.args.insert(0, "sh")
        if sys.platform == "win32":
            args.args.insert(0, "busybox")

    """
	dewr -d . tmp -e "\.(?:pid|log)$" -- sleep66.sh
	python3 -m dewr.cli -d . tmp -e "\.(?:pid|log)$" -- sleep66.sh
	"""
    try:
        dewr.WatchRestart(args.d, args.e, args.args)
    except KeyboardInterrupt:
        # 静默退出，别打错误堆栈了
        pass


if __name__ == "__main__":
    main()
