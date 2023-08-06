"""
A collection of some python library/project specific utilities.
Possibly more generic ones to follow
"""
import glob
import os
import shutil
import sys


def _removeFolder(path: str, root="./") -> None:
    shutil.rmtree(os.path.join(root, path), ignore_errors=True)


def cleanBuilds() -> bool:
    """
    Finds common build/dist fdlders and removes them recursively from the base
    of the project, where 'tasks.py' is
    """

    _removeFolder("dist")
    _removeFolder("build")

    ret = glob.glob("*egg-info")
    if len(ret) > 0:
        _removeFolder(ret[0])

    # As taskr tasks return true or false for status
    return True


def cleanCompiles() -> bool:
    """
    Finds compiled (.pyc) files and removes them recursively from the base
    of the project, where 'tasks.py' is
    """
    for root, dirs, files in os.walk(".", topdown=False):
        if "__pycache__" in dirs:
            _removeFolder("__pycache__", root)
        for name in files:
            if ".pyc" in name:
                os.remove(os.path.join(root, name))

    # As taskr tasks return true or false for status
    return True


def inVenv() -> bool:
    """
    Let's you know if you're in a virtual environment or not.
    """
    return sys.prefix != sys.base_prefix or os.environ.get("VITRUAL_ENV") is not None


def readEnvFile(filename) -> dict:
    """
    Reads in a file of ENV settings and returns a dict
    Ana alternative way of running 'source vars.env' before a command
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")

    ret = {}
    with open(filename) as file:
        for line in file:
            pair = line.split("=")
            ret[pair[0].strip()] = pair[1].strip()

    return ret


def _bump(version: str) -> str:
    """
    Internal function for easier testing
    TODO - use regex maybe - seems overkill
    """
    cleaned = version.replace("'", "").replace(",", "").replace('"', "")  # "1.2.3"
    verSplit = cleaned.split(".")  # ["1", "2", "3"]
    oldMinor = verSplit[2].strip()  # "3"
    newMinor = str(int(oldMinor) + 1)  # "4"
    newVersion = f"{verSplit[0]}.{verSplit[1]}.{newMinor}"  # "1.2.4"
    return newVersion


def bumpVersion(version: str = None) -> bool:
    """
    Bumps the minor version in setup.py by 1, or the given argument
    """
    filename = "setup.py"

    with open(filename, "r") as fd:
        temp = fd.read()

    try:
        out = []
        for line in temp.split("\n"):
            if "version=" in line:
                toReplace = line.split("=")[1]
                if version is None:
                    version = _bump(toReplace)
                line = line.replace(toReplace, f'"{version}",')
                out.append(line)
            else:
                out.append(line)
    except Exception as e:
        raise Exception(f"while bumping version: {e}")

    with open(filename, "w") as fd:
        fd.write("\n".join(out))

    return True
