#!/usr/bin/env python3
"""Turn Snap entries off. Open positions and the pullback lane are left alone."""
import os
import shutil
import py_compile

TARGET = "main.py"
BACKUP = "main.py.bak_snapoff"

OLD = "    ENABLE_SNAP = True\n"
NEW = "    ENABLE_SNAP = False\n"


def fail(msg):
    shutil.copy2(BACKUP, TARGET)
    print(msg)
    print(f"restored from {BACKUP} — bot file was not changed")


def main():
    if not os.path.exists(TARGET):
        print(f"STOPPED missing {TARGET}")
        return
    shutil.copy2(TARGET, BACKUP)
    text = open(TARGET, encoding="utf-8").read().replace("\r\n", "\n").replace("\r", "\n")
    if "ENABLE_SNAP = False" in text and OLD not in text:
        fail("STOPPED Snap is already off")
        return
    n = text.count(OLD)
    if n != 1:
        fail(f"STOPPED snap flag count={n}")
        return
    text = text.replace(OLD, NEW, 1)
    open(TARGET, "w", encoding="utf-8").write(text)
    try:
        py_compile.compile(TARGET, doraise=True)
    except Exception as e:
        fail(f"STOPPED compile: {e}")
        return
    print("DONE pieces=1")
    print(f"backup={BACKUP}")


if __name__ == "__main__":
    main()
