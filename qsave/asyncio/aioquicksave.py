import os
from .aiosession import AsyncSession
try:
    import aiofiles
    aiofiles_installed = True
except ImportError:
    aiofiles_installed = False


class AsyncQuickSave:
    def __init__(
        self,
        path: os.PathLike,
        pretty: bool = False,
        **kwargs
    ) -> None:
        if not aiofiles_installed:
            raise ImportError(
                "Aiofiles package is not installed. "
                "To use AsyncQuickSave, install package with aiofiles support: "
                "pip install qsave[aiofiles]"
            )

        self.dbpath = path
        self.pretty = pretty
        self.kwargs = kwargs

    def session(
        self,
        commit_on_expire: bool = True
    ) -> AsyncSession:
        return AsyncSession(
            self.dbpath,
            commit_on_expire,
            pretty=self.pretty,
            **self.kwargs
        )
