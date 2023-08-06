from __future__ import annotations

from functools import reduce
from typing import TypeVar, Generic, Optional, List, Callable, Dict, Any, Set, Collection, Generator

T = TypeVar('T')
Y = TypeVar('Y')


class Stream(Generic[T]):
    def __init__(self, coll: Collection[T]):
        self.stream = coll

    def map(self, f: Callable[[T], Y]) -> Stream[Y]:
        return Stream([f(i) for i in self.stream if i])

    def filter(self, f: Callable[[T], bool]) -> Stream[T]:
        return Stream([i for i in self.stream if not f(i)])

    def order_by(self, f: Callable[[T], int]) -> Stream[T]:
        v = list(self.stream)
        v.sort(key=f)
        return Stream(v)

    def find_first(self, f: Callable[[T], bool]) -> Optional[T]:
        for i in self.stream:
            if f(i):
                return i
        return None

    def find_any(self, f: Callable[[T], bool]) -> Optional[T]:
        return self.find_first(f)

    def any_match(self, f: Callable[[T], bool]) -> bool:
        for i in self.stream:
            if f(i):
                return True
        return False

    def all_match(self, f: Callable[[T], bool]) -> bool:
        return False not in [f(i) for i in self.stream]

    def distinct(self) -> Stream[T]:
        return Stream(set(self.stream))

    def for_each(self, f: Callable[[T], Any]) -> Stream[T]:
        return Stream([f(i) for i in self.stream])

    def max(self) -> Optional[T]:
        if self.stream:
            return max(list(self.stream))
        return None

    def min(self) -> Optional[T]:
        if self.stream:
            return min(list(self.stream))
        return None

    def none_match(self, f: Callable[[T], bool]) -> bool:
        return not self.any_match(f)

    def flatten(self) -> Stream[T]:
        return Stream([item for sublist in self.stream for item in sublist])

    def count(self) -> int:
        return len(self.stream)

    def list(self) -> List[T]:
        return list([i for i in self.stream if i])

    def set(self) -> Set[T]:
        r = set(self.stream)
        r.discard(None)
        return r

    def dict(self, f: Callable[[T], Y]) -> Dict[Y, T]:
        d = {}
        for i in self.stream:
            d[f(i)] = i
        return d

    def take(self, start: int, step: int, cnt: int, ) -> Stream[T]:
        cnt = min(len(self.stream) - start, cnt)
        return Stream(self.stream[start:start + cnt:step])

    def limit(self, cnt: int) -> Stream[T]:
        return self.take(start=0, step=1, cnt=cnt)

    def skip(self, cnt: int) -> Stream[T]:
        return self.take(start=cnt, step=1, cnt=len(self.stream))

    def concat(self, i: Stream[T]) -> Stream[T]:
        return Stream(list(self.stream) + list(i.stream))

    def fold(self, f: Callable[[T, T], Y]) -> Y:
        return reduce(f, self.stream[1:], list(self.stream)[0])

    def zip(self, i: Stream[Y]) -> Stream[(T, Y)]:
        return Stream(coll=list(zip(self.stream, i.list())))

    def emit(self) -> Generator[T]:
        for i in self.stream:
            yield i
