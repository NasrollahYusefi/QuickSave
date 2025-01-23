import os
import threading
from .io import open_file, write_file


class Session:
    def __init__(
        self,
        filepath: os.PathLike,
        commit_on_expire: bool = False,
        pretty: bool = False,
        lock: threading.RLock = None,
        **kwargs
    ) -> None:
        self.cache_upserts = {}
        self.cache_deletes = []
        self.bef_data = None
        self.file = filepath
        self.commit_on_expire = commit_on_expire
        self.pretty = pretty
        self.kwargs = kwargs
        self.lock = lock
        self.is_closed = None

    def _open_bef_data(self) -> None:
        if self.is_closed is True:
            raise ValueError("operation on closed session.")

        if self.bef_data is None:
            self.bef_data: dict = open_file(
                filename=self.file,
                **self.kwargs
            )

    def commit(self):
        self._open_bef_data()

        self.bef_data.update(
            self.cache_upserts
        )
        for k in self.cache_deletes:
            self.bef_data.pop(k, None)
        write_file(
            filename=self.file,
            data=self.bef_data,
            pretty=self.pretty,
            **self.kwargs
        )
        self.cache_upserts.clear()
        self.cache_deletes.clear()

    def rollback(self):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        self.cache_upserts.clear()
        self.cache_deletes.clear()

    def open(self):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        return self

    def close(self):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        if self.commit_on_expire is True:
            self.commit()
        self.bef_data = None
        self.cache_upserts.clear()
        self.cache_deletes.clear()
        self.is_closed = True

    def __enter__(self):
        self.lock.acquire()
        return self.open()

    def __exit__(self, *args, **kwargs):
        self.close()
        self.lock.release()

    def __getitem__(self, key):
        self._open_bef_data()
        return self.bef_data[key]

    def __setitem__(self, key, value):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        self.cache_upserts[key] = value

    def __delitem__(self, key):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        self.cache_deletes.append(key)

    def __iter__(self):
        self._open_bef_data()
        yield from self.bef_data

    def __repr__(self):
        self._open_bef_data()
        return self.bef_data.__repr__()

    def __len__(self):
        self._open_bef_data()
        return len(self.bef_data)

    def get(self, key, default = None):
        self._open_bef_data()
        return self.bef_data.get(key, default)

    def setdefault(self, key, default = None):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        return self.cache_upserts.setdefault(key, default)

    def pop(self, key, default = None):
        self._open_bef_data()
        return self.bef_data.pop(key, default)

    def keys(self):
        self._open_bef_data()
        yield from self.bef_data.keys()

    def values(self):
        self._open_bef_data()
        yield from self.bef_data.values()

    def items(self):
        self._open_bef_data()
        yield from self.bef_data.items()

    def clear(self):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        self.bef_data = {}

    def update(self, data: dict):
        self._open_bef_data()
        self.bef_data.update(data)

    def copy(self) -> dict:
        self._open_bef_data()
        return self.bef_data.copy()

    def popitem(self) -> tuple:
        self._open_bef_data()
        return self.bef_data.popitem()
