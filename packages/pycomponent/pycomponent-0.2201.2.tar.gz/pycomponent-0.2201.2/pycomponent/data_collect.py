#!/usr/bin/env python3
import os
import boxx
from boxx import *
from boxx import listdir, pathjoin
import shutil
from pathlib import Path
from threading import Lock

"""
可复用的数据回流模块
默认情况下:
- 每天 check 一次数量超限
    - rm 超限数目 * 2
- 每次 or time to check 剩余空间超限
    - 剩余空间超限, 直接 rm max(1GB, 剩余空间)
"""


def get_size(start_path="."):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


class DataCollect:
    def __init__(
        self,
        root,
        free_disk_size=2 ** 30,
        max_num=None,
        check_interval=24 * 60 * 3600,
        log=True,
    ):
        self.root = root
        os.makedirs(root, exist_ok=True)
        self.free_disk_size = free_disk_size
        self.max_num = max_num
        self.del_lock = Lock()
        self.log = log

        if self.max_num:
            boxx.setTimeout(
                lambda: boxx.setInterval(self.check_num, check_interval), check_interval
            )

    def sort_listdir(self):
        return sorted(map(str, Path(self.root).iterdir()), key=os.path.getmtime)

    def get_free_space(self):
        return shutil.disk_usage(self.root)[-1]

    def check_num(self):
        bnames = os.listdir(self.root)
        if len(bnames) > self.max_num:
            with self.del_lock:
                paths = self.sort_listdir()
                rmn = 2 * (len(bnames) - self.max_num)
                if self.log:
                    print(
                        f"DataCollect: now={len(paths)}, max_num={self.max_num}, need to rm {rmn} items."
                    )
                for _ in range(rmn):
                    if len(paths):
                        path = paths.pop(0)
                        self.rm(path)

    @staticmethod
    def rm(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    @staticmethod
    def format_size(size):
        return f"{boxx.strnum(size/2**30, 2)}GB"

    def check_free_sapce(self):
        free_sapce = self.get_free_space()
        ok = free_sapce > self.free_disk_size
        if not ok:

            def rm_over_limit(multiple=2):
                with self.del_lock:
                    if self.log:
                        print(
                            f"DataCollect: To keep {self.format_size(self.free_disk_size)} free space, need to rm {self.format_size(multiple * self.free_disk_size - free_sapce)}"
                        )
                    paths = self.sort_listdir()
                    while self.get_free_space() < multiple * self.free_disk_size and len(
                        paths
                    ):
                        path = paths.pop(0)
                        self.rm(path)

            boxx.setTimeout(rm_over_limit)
        return ok

    def new_dir(self, makedir=True):
        self.check_free_sapce()
        dirr = pathjoin(self.root, boxx.localTimeStr())
        if makedir:
            os.makedirs(dirr, exist_ok=True)
        return dirr

    @classmethod
    def test_max_num(cls):
        root = "/tmp/test-DataCollect/"
        data_collect = cls(root, max_num=5, check_interval=4)

        for i in range(10):
            dirr = data_collect.new_dir()
            boxx.sleep(0.1)
            os.system(f"dd if=/dev/zero of={dirr + '/' + str(i)} bs=10M count=1")
        boxx.mg()


if __name__ == "__main__":
    DataCollect.test_max_num()
