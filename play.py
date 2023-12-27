import sys
import time
import json
import zlib
from fuse import FUSE, Operations


class Play(Operations):
    def __init__(self):
        self.fps = 29.97
        with open("frames.dat", "rb") as f:
            self.frames = json.loads(zlib.decompress(f.read()))

    def readdir(self, path, _):
        yield "."
        yield ".."
        if path == "/":
            start = time.time()
            flen = len(self.frames)
            wid = len(self.frames[0][0])
            for i in range(flen):
                yield " ".join(
                    [
                        str(int((i / self.fps + start) * 1000)),
                        str(i).rjust(4, "0"),
                        " " * 8,
                        f"[{('='*int(wid*(i+1)/flen)).ljust(wid)}]",
                    ]
                )

        else:
            target = int(path.split("/")[1].split(" ")[0]) / 1000
            delay = target - time.time()
            if delay > 0:
                time.sleep(delay)

            fnum = int(path.split("/")[1].split(" ")[1])
            for i in range(len(self.frames[fnum])):
                yield str(i).rjust(2, "0") + " \u2502" + self.frames[fnum][i] + "\u2502"

    def getattr(self, path, _=None):
        m = time.timezone
        try:
            m += int(path.split("/")[1].split(" ")[1]) / self.fps
        except IndexError:
            pass
        return {
            "st_atime": 0,
            "st_ctime": 0,
            "st_gid": 0,
            "st_mode": 0x8000 if path.count("/") > 1 else 0x4000,
            "st_mtime": m,
            "st_nlink": 1,
            "st_size": 0,
            "st_uid": 0,
        }


FUSE(Play(), sys.argv[1])
