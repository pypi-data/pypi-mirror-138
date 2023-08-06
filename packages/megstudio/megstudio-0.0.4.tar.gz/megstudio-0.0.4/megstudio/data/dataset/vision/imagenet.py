# -*- coding: utf-8 -*-
# BSD 3-Clause License
#
# Copyright (c) Soumith Chintala 2016,
# All rights reserved.
# ---------------------------------------------------------------------
# MegEngine is Licensed under the Apache License, Version 2.0 (the "License")
#
# Copyright (c) 2014-2021 Megvii Inc. All rights reserved.
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT ARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# This file has been modified by Megvii ("Megvii Modifications").
# All Megvii Modifications are Copyright (C) 2014-2021 Megvii Inc. All rights reserved.
# ---------------------------------------------------------------------
import os
import shutil

from ....logger import get_logger
from .folder import ImageFolder

logger = get_logger(__name__)


class ImageNet(ImageFolder):
    r"""Load ImageNet from raw files or folder. Expected folder looks like:
    
    .. code-block:: shell
    
        ${root}/
        |       [REQUIRED TAR FILES]
        |-  ILSVRC2012_img_train.tar
        |-  ILSVRC2012_img_val.tar
        |-  ILSVRC2012_devkit_t12.tar.gz
        |       [OPTIONAL IMAGE FOLDERS]
        |-  train/cls/xxx.${img_ext}
        |-  val/cls/xxx.${img_ext}
        |-  ILSVRC2012_devkit_t12/data/meta.mat
        |-  ILSVRC2012_devkit_t12/data/ILSVRC2012_validation_ground_truth.txt
    
    If the image folders don't exist, raw tar files are required to get extracted and processed.

        * if ``root`` contains ``self.target_folder`` depending on ``train``:

          * initialize ImageFolder with target_folder.

        * else:

          * if all raw files are in ``root``:

            * parse ``self.target_folder`` from raw files.
            * initialize ImageFolder with ``self.target_folder``.

          * else:

            * raise error.

    Args:
        root: root directory of imagenet data, if root is ``None``, use default_dataset_root.
        train: if ``True``, load the train split, otherwise load the validation split.

    """

    raw_file_meta = {
        "train": ("ILSVRC2012_img_train.tar", "1d675b47d978889d74fa0da5fadfb00e"),
        "val": ("ILSVRC2012_img_val.tar", "29b22e2961454d5413ddabcf34fc5622"),
        "devkit": ("ILSVRC2012_devkit_t12.tar.gz", "fa75699e90414af021442c21a62c3abf"),
    }  # ImageNet raw files
    default_train_dir = "train"
    default_val_dir = "val"
    default_devkit_dir = "ILSVRC2012_devkit_t12"

    def __init__(self, root: str = None, train: bool = True, **kwargs):
        # process the root path
        if root is None:
            self.root = self._default_root
        else:
            self.root = root

        if not os.path.exists(self.root):
            raise FileNotFoundError("dir %s does not exist, please select dataset imagenet in this repo" % self.root)

        self.devkit_dir = os.path.join(self.root, self.default_devkit_dir)

        if not os.path.exists(self.devkit_dir):
            logger.warning("devkit directory %s does not exists, please select dataset imagenet in this repo", self.devkit_dir)
            self._prepare_devkit()

        self.train = train

        if train:
            self.target_folder = os.path.join(self.root, self.default_train_dir)
        else:
            self.target_folder = os.path.join(self.root, self.default_val_dir)

        if not os.path.exists(self.target_folder):
            raise FileNotFoundError(
                "expected image folder %s does not exist, and raw files do not exist in %s, please select dataset imagenet in this repo"
                % (self.target_folder, self.root)
            )
        super().__init__(self.target_folder, **kwargs)

    @property
    def _default_root(self):
        return "/home/megstudio/dataset/ILSVRC2012"
