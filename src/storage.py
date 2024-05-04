"""
Abstraction to wrap both regular Zarr stores and Arraylake Zarr stores.
"""

from abc import ABC, abstractmethod

import arraylake
import zarr


class AbstractStorage(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def get_zarr_store(self):
        pass

    @abstractmethod
    def commit(self, message):
        pass


class ZarrFSSpecStorage(AbstractStorage):
    zarr_version = 2

    def __init__(self, uri):
        self.uri = uri
        self._store = zarr.storage.FSStore(uri)

    def initialize(self):
        self._store.clear()

    def get_zarr_store(self):
        return self._store

    def commit(self, message):
        # no-op
        # vanilla Zarr stores are not transactional
        pass


class ArraylakeStorage(AbstractStorage):
    zarr_version = 3

    def __init__(self, repo_name: str):
        self._repo_name = repo_name
        self._client = arraylake.Client()
        self._repo = None

    def initialize(self):
        try:
            self._client.delete_repo(self._repo_name, imsure=True, imreallysure=True)
        except ValueError:
            pass
        finally:
            self._repo = self._client.create_repo(self._repo_name)

    def get_zarr_store(self):
        if self._repo is None:
            self._repo = self._client.get_repo(self._repo_name)
        return self._repo.store

    def commit(self, message):
        self._repo.commit(message)
