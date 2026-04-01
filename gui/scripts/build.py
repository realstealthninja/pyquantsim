#!/usr/bin/env python3
import shutil
from subprocess import run

run(["cxfreeze", "build"])
shutil.copytree("assets/", "dist/assets", dirs_exist_ok=True)
shutil.copytree("qml/", "dist/qml", dirs_exist_ok=True)
shutil.copy("README", "dist/")
shutil.copy("../LICENSE", "dist/")
