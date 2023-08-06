#!/usr/bin/env python3

import boxx
from boxx import pathjoin, np

import os
import cv2
import json
import base64


def dir_to_b64_dic(dirr):
    bnames = os.listdir(dirr)
    return {
        bname: open(pathjoin(dirr, bname), "rb").read()
        for bname in bnames
        if boxx.isfile(pathjoin(dirr, bname))
    }


def b64_dic_to_dir(b64_dic, dirr):
    os.makedirs(dirr, exist_ok=True)
    for bname, binary in b64_dic.items():
        with open(pathjoin(dirr, bname), "wb") as f:
            f.write(binary)


def b64_dic_to_json_str(b64_dic):
    base64_dic = {
        k: base64.b64encode(binary).decode("ascii") for k, binary in b64_dic.items()
    }
    return json.dumps(base64_dic)


def json_str_to_b64_dic(json_str):
    js = json.loads(json_str)
    b64_dic = {k: base64.b64decode(b64) for k, b64 in js.items()}
    return b64_dic


def decode_b64_dic(b64_dic):
    dic = {
        k: cv2.imdecode(np.frombuffer(binary, np.uint8), cv2.IMREAD_UNCHANGED)
        if k[-3:] in ["jpg", "png"]
        else binary
        for k, binary in b64_dic.items()
    }

    return {
        k: v[:, :, ::-1]
        if isinstance(v, np.ndarray) and v.ndim == 3 and v.shape[-1] == 3
        else v
        for k, v in dic.items()
    }


def encode_img_dic(img_dic):
    def f(name, img):
        if isinstance(img, np.ndarray):
            if img.ndim == 3 and img.shape[-1] == 3:
                img = img[:, :, ::-1]
            return cv2.imencode(name[-4:], img)[1].tobytes()
        return img

    return {name: f(name, img) for name, img in img_dic.items()}


def filter_too_long_string_in_json(js, max_len=20000):
    return {
        k: "Filtered too_long_%s for json, original len() is %s"
        % (type(v).__name__, len(v))
        if (isinstance(v, (str, bytes)) and len(v) > max_len)
        else v
        for k, v in js.items()
    }


def test(dirr="__pycache__"):
    dic = dir_to_b64_dic(dirr)

    tdir = "/tmp/b64_dic"
    b64_dic_to_dir(dic, tdir)
    os.system(f"tree {tdir}")
    boxx.tree - dic

    js = b64_dic_to_json_str(dic)
    redic = json_str_to_b64_dic(js)

    boxx.tree - redic
    boxx.g()


if __name__ == "__main__":
    from boxx import *

    test()
