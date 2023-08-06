#!/usr/bin/env python
import hashlib
import os
from typing import Dict, List, Optional, Set, Tuple

import codefast as cf
from authc import get_redis_cn

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


def md5sum(file_path: str) -> str:
    """ Calculate md5sum of file.
    Args:
        file_path(str): file path
    """
    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()


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
        self.loader_name = loader_name
        if loader_name == 'oss_loader':
            self.loader = _OSSLoader()
        self._redis = get_redis_cn()

    def set_loader(self, loader):
        self.loader = loader
        return self

    def pull(self, overwrite: bool = False):
        """pull file from remote to local
        Args:
            overwrite(bool): overwrite local file or not
        """
        if not cf.io.exists(self.local_dir):
            cf.io.mkdir(self.local_dir)
        if not cf.io.exists(
                os.path.join(self.local_dir + self.name)) or overwrite:
            self.loader.pull(self.name, self.remote_dir, self.local_dir)
        return self

    def push(self):
        self.loader.push(self.name, self.remote_dir, self.local_dir)
        return self

    @property
    def path(self):
        """ Everytime the file is visited, it will sync with remote server.
        """
        _path = os.path.join(self.local_dir + self.name)
        if not cf.io.exists(_path):
            self.pull()
        else:
            md5sum_key = 'md5sum_{}'.format(md5sum(_path))
            if not self._redis.exists(md5sum_key):
                self.push()
                self._redis.set(md5sum_key, _path, ex=60 * 60 * 24 * 30)
        return _path

    def copy(self, name: str) -> 'SyncFile':
        """ Quickly create a new SyncFile object with same remote_dir and local_dir.
        """
        return SyncFile(name, self.remote_dir, self.local_dir, self.loader_name)

    def loads(self):
        return cf.io.reads(self.path)

    def loadjs(self):
        return cf.js(self.path)

    def info(self):
        print(self)
        return self

    def __repr__(self):
        return '\n'.join(('{:<20}: {}'.format(k, v)
                          for k, v in self.__dict__.items()
                          if not k.startswith('_')))
