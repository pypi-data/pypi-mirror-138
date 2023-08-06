# -*- coding: utf-8 -*-
# MegEngine is Licensed under the Apache License, Version 2.0 (the "License")
#
# Copyright (c) 2014-2021 Megvii Inc. All rights reserved.
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT ARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hashlib
import os
import tarfile

from ....logger import get_logger

IMG_EXT = (".jpg", ".png", ".jpeg", ".ppm", ".bmp", ".pgm", ".tif", ".tiff", ".webp")

logger = get_logger(__name__)


def _default_dataset_root():
    default_dataset_root = os.path.expanduser(
        os.path.join(os.getenv("XDG_CACHE_HOME", "~/.cache"), "megengine")
    )

    return default_dataset_root

def calculate_md5(filename):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def is_img(filename):
    return filename.lower().endswith(IMG_EXT)


def untar(path, to=None, remove=False):
    if to is None:
        to = os.path.dirname(path)
    with tarfile.open(path, "r") as tar:
        tar.extractall(path=to)

    if remove:
        os.remove(path)


def untargz(path, to=None, remove=False):
    if path.endswith(".tar.gz"):
        if to is None:
            to = os.path.dirname(path)
        with tarfile.open(path, "r:gz") as tar:
            tar.extractall(path=to)
    else:
        raise ValueError("path %s does not end with .tar" % path)

    if remove:
        os.remove(path)
