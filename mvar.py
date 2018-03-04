import threading
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class MVar(Generic[T]):
    def __init__(self, value: Optional[T] = None) -> None:
        self._value = value
        self._cond = threading.Condition()

    def take(self) -> T:
        with self._cond:
            while self._value is None:
                self._cond.wait()
            ret = self._value
            self._value = None
            self._cond.notify_all()
            return ret

    def put(self, value: T) -> None:
        with self._cond:
            while not self._value is None:
                self._cond.wait()
            self._value = value
            self._cond.notify_all()

    def read(self) -> T:
        with self._cond:
            while self._value is None:
                self._cond.wait()
            return self._value

    def swap(self, value: T) -> T:
        with self._cond:
            while self._value is None:
                self._cond.wait()
            ret = self._value
            self._value = value
            return ret

    def try_take(self) -> Optional[T]:
        with self._cond:
            ret = self._value
            self._value = None
            self._cond.notify_all()
            return ret

    def try_put(self, value: T) -> bool:
        with self._cond:
            ret = self._value
            if self._value is None:
                self._value = value
                self._cond.notify_all()
                return True
            else:
                return False

    def empty(self) -> bool:
        return (self._value is None)
