import os
from .aio import aopen_file, awrite_file


class AsyncSession:
    def __init__(
        self,
        filepath: os.PathLike,
        commit_on_expire: bool = False,
        pretty: bool = False,
        **kwargs
    ) -> None:
        self.cache_upserts = {}
        self.cache_deletes = []
        self.bef_data = None
        self.file = filepath
        self.commit_on_expire = commit_on_expire
        self.pretty = pretty
        self.kwargs = kwargs
        self.is_closed = None

    async def _open_bef_data(self) -> None:
        if self.is_closed is True:
            raise ValueError("operation on closed session.")

        if self.bef_data is None:
            self.bef_data: dict = await aopen_file(
                filename=self.file,
                **self.kwargs
            )

    async def commit(self):
        self.bef_data.update(
            self.cache_upserts
        )
        for k in self.cache_deletes:
            self.bef_data.pop(k, None)
        await awrite_file(
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

    async def open(self):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        await self._open_bef_data()
        return self

    async def close(self):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        if self.commit_on_expire is True:
            await self.commit()
        self.bef_data = None
        self.cache_upserts.clear()
        self.cache_deletes.clear()
        self.is_closed = True

    async def __aenter__(self):
        return await self.open()

    async def __aexit__(self, *args, **kwargs):
        await self.close()

    def __getitem__(self, key):
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
        yield from self.bef_data

    def __eq__(self, value):
        return value in self.bef_data

    def __repr__(self):
        return self.bef_data.__repr__()

    def __len__(self):
        return len(self.bef_data)

    def get(self, key, default = None):
        return self.bef_data.get(key, default)

    def setdefault(self, key, default = None):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        return self.cache_upserts.setdefault(key, default)

    def pop(self, key, default = None):
        return self.bef_data.pop(key, default)

    def keys(self):
        yield from self.bef_data.keys()

    def values(self):
        yield from self.bef_data.values()

    def items(self):
        yield from self.bef_data.items()

    def clear(self):
        if self.is_closed is True:
            raise ValueError("operation on closed session.")
        self.bef_data = {}

    def update(self, data: dict):
        self.bef_data.update(data)

    def copy(self) -> dict:
        return self.bef_data.copy()

    def popitem(self) -> tuple:
        return self.bef_data.popitem()
