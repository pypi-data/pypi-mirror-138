from pathlib import Path
from typing import List

from gasbullet import cache as cachemod
from gasbullet import skeleton as gasbullet_skeleton


def myfilter(paths: List[Path], cache: cachemod.Cache):

    # filter on only file types and substrings in paths
    dirs = set(filter(lambda _str: Path(_str).is_dir(), paths))
    symlinks = set(filter(lambda _str: Path(_str).is_symlink(), paths))
    paths_filtered = paths - dirs - symlinks

    ignore = set()
    for x in [".tox/", ".venv/", ".git/"]:
        ignore |= set(
            filter(lambda _str: x in str(Path(_str).resolve()).lower(), paths)
        )
    paths_filtered -= ignore

    powershell = set()
    for ext in [".ps1"]:
        powershell |= set(
            filter(lambda _str: Path(_str).suffix.lower() == ext, paths_filtered)
        )

    shortcuts = set()
    for ext in [".lnk"]:
        shortcuts |= set(
            filter(lambda _str: Path(_str).suffix.lower() == ext, paths_filtered)
        )

    py = set()
    for ext in [".pyc"]:
        py |= set(filter(lambda _str: Path(_str).suffix.lower() == ext, paths_filtered))

    # stuff below relies on magic
    gasbullet_skeleton.set_mymap_magic_types(paths_filtered, cache)
    cache.cache(cache.mymap)

    text1 = set(
        filter(lambda x: cache.mymap[x].startswith("text/"), cache.mymap.keys())
    )
    text2 = set(
        filter(
            lambda x: cache.mymap[x].startswith("application/json"),
            cache.mymap.keys(),
        )
    )
    empty = set(
        filter(lambda x: cache.mymap[x].startswith("inode/x-empty"), cache.mymap.keys())
    )
    icons = set(
        filter(lambda x: cache.mymap[x].startswith("image/x-icon"), cache.mymap.keys())
    )

    text = text1 | text2

    tosign = paths_filtered
    tosign -= ignore
    tosign -= text
    tosign -= shortcuts
    tosign -= empty
    tosign -= icons
    tosign -= py
    tosign |= powershell

    cache.data = tosign
