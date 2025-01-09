import os
import threading
from .session import Session


class QuickSave:
    def __init__(
        self,
        path: os.PathLike,
        pretty: bool = False,
        **kwargs
    ) -> None:
        self.dbpath = path
        self.lock = threading.Lock()
        self.pretty = pretty
        self.kwargs = kwargs

    def session(
        self,
        commit_on_expire: bool = True
    ) -> Session:
        return Session(
            self.dbpath,
            commit_on_expire,
            pretty=self.pretty,
            lock=self.lock,
            **self.kwargs
        )
