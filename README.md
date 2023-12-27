# Bad Apple Filesystem

https://youtu.be/8iZHCBoArc4

[![Video](https://img.youtube.com/vi/8iZHCBoArc4/hqdefault.jpg)](https://youtu.be/8iZHCBoArc4)

## Usage
First, grab the source video, and name it `video.webm`.
Then run:
```
nix run .#gen

mkdir ./mnt
nix run . ./mnt

ls -lR --time-style=+%M:%S
```

##

You can also run `gen.py` and `play.py` directly, but you need to install OpenCV and Fusepy first.
