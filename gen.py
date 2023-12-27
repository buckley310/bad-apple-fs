import cv2
import json
import zlib


def read_video():
    i = 1
    v = cv2.VideoCapture("video.webm")
    while (frame := v.read())[0]:
        print("processing frame:", i, "/", v.get(cv2.CAP_PROP_FRAME_COUNT))
        yield frame[1]
        i += 1


def main():
    scale = 8

    subpixels = (
        (1 * scale, 3 * scale),
        (0 * scale, 3 * scale),
        (1 * scale, 2 * scale),
        (1 * scale, 1 * scale),
        (1 * scale, 0 * scale),
        (0 * scale, 2 * scale),
        (0 * scale, 1 * scale),
        (0 * scale, 0 * scale),
    )

    frames = []
    for img in read_video():
        frame = []
        for y in range(len(img) // (4 * scale)):
            ln = ""
            for x in range(len(img[0]) // (2 * scale)):
                outi = 0
                for xa, ya in subpixels:
                    outi <<= 1
                    outi += img[y * 4 * scale + ya][x * 2 * scale + xa][0] > 127
                ln += chr(0x2800 + outi)
            frame.append(ln)
        frames.append(frame)
        print("\n".join(frame))

    with open("frames.dat", "wb") as f:
        f.write(zlib.compress(json.dumps(frames).encode("ascii")))


main()
