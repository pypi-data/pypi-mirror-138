# dewr

## Feature:
* Restart job when start or files change.
* Kill job when exit.

## Install
```sh
pip3 install -U dewr
```

## Usage
```py
import logging
import dewr
logging.basicConfig(
	level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s"
)
dewr.WatchRestart(["."], r"\.(?:pid|log)$", ["sh", "sleep66.sh"])

```

```sh
dewr -d . /Another/Dir/To/Watch -e "\.(pid|log)$|^(dist|bin|log|node_modules|\.git)(/|$)" -- sleep66.sh
```


