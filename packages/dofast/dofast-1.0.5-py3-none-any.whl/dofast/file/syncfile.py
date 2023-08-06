#!/usr/bin/env python
import os
from typing import Dict, List, Optional, Set, Tuple

import codefast as cf
import pandas as pd

from dofast.oss import Bucket

cf.logger.level = 'info'


class BaseLoader(object):
    pass


class _OSSLoader(BaseLoader):
    def __init__(self, require_encryption: bool = False) -> None:
        """
        Args:
            require_encryption(bool): encrypte file or not before uploading
        """
        self.bucket = Bucket()
        self.require_encryption = require_encryption

    def pull(self, file_name: str, remote_dir: str, local_dir: str):
        """ Download file from bucket.
        Args:
            file_name(str): file name with no path
            remote_dir(str): remote dir path of file
            local_dir(str): local dir path to save file
        """
        remote_path = os.path.join(remote_dir, file_name)
        local_path = os.path.join(local_dir, file_name)
        self.bucket.download(remote_path, local_path)
        return self

    def push(self, file_name: str, remote_dir: str, local_dir: str):
        """ Upload file to bucket.
        Args:
            file_name(str): local file path, e.g., /tmp/abc.md
        """
        local_path = os.path.join(local_dir, file_name)
        self.bucket.upload(local_path,
                           remote_dir,
                           encryption=self.require_encryption)
        return self


class SyncFile(object):
    def __init__(self,
                 name: str,
                 remote_dir: str,
                 local_dir: str,
                 loader_name: str = None) -> None:
        self.remote_dir = remote_dir
        self.name = name
        self.local_dir = local_dir
        self.loader = None
        if loader_name == 'oss_loader':
            self.loader = _OSSLoader()

    def set_loader(self, loader):
        self.loader = loader
        return self

    def pull(self):
        # pull file from remote to local
        if not cf.io.exists(self.local_dir):
            cf.io.mkdir(self.local_dir)
        self.loader.pull(self.name, self.remote_dir, self.local_dir)
        return self

    def push(self):
        self.loader.push(self.name, self.remote_dir, self.local_dir)
        return self

    @property
    def path(self):
        return os.path.join(self.local_dir + self.name)

    def loads(self):
        return cf.io.reads(self.path)

    def loadjs(self):
        return cf.js(self.path)

    def info(self):
        print(self)
        return self

    def __repr__(self):
        return '\n'.join(
            ('{:<20}: {}'.format(k, v) for k, v in self.__dict__.items()))
