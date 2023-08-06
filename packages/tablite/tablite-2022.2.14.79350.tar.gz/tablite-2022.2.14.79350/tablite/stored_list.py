import math
import pickle
import sqlite3

from pathlib import Path
from random import choice
from string import ascii_lowercase

from tempfile import gettempdir
from itertools import count

from tablite.datatypes import DataTypes

# Queries for StoredList
sql_create = "CREATE TABLE records (id INTEGER PRIMARY KEY, data BLOB);"
sql_journal_off = "PRAGMA journal_mode = OFF"
sql_sync_off = "PRAGMA synchronous = OFF "
sql_delete = "DELETE FROM records WHERE id = ?"
sql_insert = "INSERT INTO records VALUES (?, ?);"
sql_update = "UPDATE records SET data = ? WHERE id=?;"
sql_select = "SELECT data FROM records WHERE id=?"


def tempfile(prefix='tmp', suffix='.db'):
    """ generates a safe tempfile which windows can't handle. """
    safe_folder = Path(gettempdir())
    while 1:
        n = "".join(choice(ascii_lowercase) for _ in range(10))
        name = f"{prefix}{n}{suffix}"
        p = safe_folder / name
        if not p.exists():
            break
    return p


class Page(list):
    ids = count()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pid = next(Page.ids)
        self._len = 0
        self.loaded = True
        self.size = 0

    def __str__(self):
        return f"Page({self.pid}) {'loaded' if self.loaded else 'stored'} ({self.len} items)"

    def __repr__(self):
        return self.__str__()

    @property
    def len(self):
        """
        `list` uses __len__ to determine list.__iter__'s stop point so we can't use __len__
        to determine the length of the page if it hasn't been loaded.
        return: integer.
        """
        if self.loaded:
            return self.__len__()
        else:
            return self._len

    def load(self, data):
        self.extend(data)
        self.loaded = True

    def store(self):
        self.loaded = False
        self._len = self.__len__()
        data = self.copy()
        self.clear()
        return data


class StoredList(object):
    """
    Python list stored on disk using sqlite's fast mmap.
    """
    default_page_size = 200_000
    storage_file = tempfile()
    _conn = sqlite3.connect(database=str(storage_file))  # SQLite3 connection
    with _conn as c:
        c.execute(sql_create)
        c.execute(sql_journal_off)
        c.execute(sql_sync_off)

    def __init__(self, data=None, page_size=None):
        if page_size is None:
            page_size = StoredList.default_page_size
        if not isinstance(page_size, int):
            raise TypeError
        self._page_size = page_size
        self.pages = []

        if data is not None:
            if isinstance(data, int):
                raise TypeError(f"Did you do data={data} instead of page_size={data}?")
            self.extend(data)

        self._loaded_page = None

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        if not isinstance(value, int):
            raise TypeError
        elif value < 0:
            raise ValueError
        elif self._page_size == value:
            pass  # leave as is.
        elif value > self._page_size:  # leave the page size. It won't make a difference.
            self._page_size = value
        else:  # pages will have to be reduced.
            print(f"reducing page size from {self._page_size} to {value}")
            self._page_size = value

            SL = StoredList(page_size=value, data=self)

            for page in self.pages[:]:
                self._delete_page(page)
            assert not self.pages
            self.extend(SL)

    def _new_page(self):
        """ internal method that stores current page and creates a new empty page"""
        _ = [self._store_page(p) for p in self.pages if p.loaded]
        if any(p.loaded for p in self.pages):
            raise AttributeError("other pages are loaded.")

        page = Page()
        self.pages.append(page)

        data = pickle.dumps(page.copy())  # empty list.
        with self._conn as c:
            c.execute(sql_insert, (page.pid, data))  # INSERT the empty list.

        return page

    def _store_page(self, page):
        """ internal method that stores page data to disk.
        :param page: Page
        """
        assert isinstance(page, Page)
        data = page.store()
        assert not page.loaded
        data_as_bytes = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        page.size = len(data_as_bytes)
        with self._conn as c:
            c.execute(sql_update, (data_as_bytes, page.pid))  # UPDATE
        return page

    def _load_page(self, page):
        """ internal method that loads the data from a page.
        :param page: Page
        """
        assert isinstance(page, Page)
        if page.loaded:
            return page

        _ = [self._store_page(p) for p in self.pages if p.loaded]

        if any(p.loaded for p in self.pages):
            raise AttributeError("other pages are loaded.")

        with self._conn as c:
            q = c.execute(sql_select, (page.pid,))  # READ
            data = q.fetchone()[0]
            unpickled_data = pickle.loads(data)

        page.load(unpickled_data.copy())
        return page

    def _delete_page(self, page):
        """ internal method that deletes a page of data. """
        assert isinstance(page, Page)
        page.clear()  # in case it holds data.
        self.pages.remove(page)

        with self._conn as c:
            c.execute(sql_delete, (page.pid,))  # DELETE

        del page

        return None

    # PUBLIC METHODS.

    def __len__(self):
        return sum(p.len for p in self.pages)

    def __iter__(self):
        for page in self.pages:
            p1 = page.pid
            assert isinstance(page, Page)
            page = self._load_page(page)
            assert page.pid == p1

            assert isinstance(page, list)
            for value in page:
                yield value
            page = self._store_page(page)
            assert not page.loaded

    def __reversed__(self):
        for page in reversed(self.pages):
            self._load_page(page)
            for value in reversed(page):
                yield value

    def __repr__(self):
        return f"StoredList(page_size={self._page_size}, data={len(self)})"

    def __str__(self):
        return f"StoredList(page_size={self._page_size}, data={len(self)})"

    def append(self, value):
        """ Append object to the end of the list. """
        if not self.pages:
            last_page = self._new_page()
        else:
            assert self.pages, "there must be at least one page."
            last_page = self.pages[-1]

        if last_page.len == self._page_size:
            last_page = self._new_page()
        last_page.append(value)

    def clear(self):
        """ Remove all items from list. """
        for page in self.pages[:]:
            self._delete_page(page)

    def copy(self):
        """ Return a shallow copy of the list. """
        SL = StoredList(page_size=self.page_size)
        for page in self.pages:
            page = self._load_page(page)
            SL.extend(page.copy())
        return SL

    def count(self, item):
        """ Return number of occurrences of item. """
        return sum(1 for v in self if v == item)

    def extend(self, items):
        """ Extend list by appending elements from the iterable. """
        if not self.pages:
            last_page = self._new_page()
        else:
            last_page = self.pages[-1]
        # last_page = self._last_page()
        space = self._page_size - last_page.len
        c = 0
        for i in items:
            if not space:
                last_page = self._new_page()
                space = self._page_size
            last_page.append(i)
            c += 1
            space -= 1
        assert c == len(items), (c, len(items))

    def index(self, item):
        """
        Return first index of value.
        Raises ValueError if the value is not present.
        """
        for ix, v in enumerate(self):
            if v == item:
                return ix
        raise ValueError(f"{item} is not in list")

    def insert(self, index, item):
        """ Insert object before index. """
        if not isinstance(index, int):
            raise TypeError
        if abs(index) > len(self):
            raise IndexError("index out of range")
        if index < 0:
            index = len(self) + index

        c = 0
        page = None
        for page in self.pages[:]:
            assert isinstance(page, Page)
            if c <= index <= page.len + c:
                break
            c += page.len
        ix = index - c

        assert isinstance(page, Page)
        loaded_page = self._load_page(page)
        loaded_page.insert(ix, item)

        if page.len < self._page_size:  # if there is space on the page...
            return
        # else -  split the data in half and insert a page.
        n = page.len // 2

        A, B = page[:n], page[n:]
        page.clear()
        page.extend(A)

        page_ix = self.pages.index(page)

        new_page = self._new_page()
        new_page.extend(B)

        self.pages.remove(new_page)
        self.pages.insert(page_ix + 1, new_page)

    def pop(self, index=None):
        """
        Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range.
        """
        if index is None:
            index = -1
        if not isinstance(index, int):
            raise TypeError
        if abs(index) > len(self):
            raise IndexError("list index out of range")
        if index < 0:
            index = len(self) + index

        c = 0
        for page in self.pages[:]:
            if c <= index < page.len + c:
                page = self._load_page(page)
                ix = index - c
                value = page.pop(ix)
                if len(page) == 0:
                    self._delete_page(page)
                return value
            else:
                c += page.len

    def remove(self, item):
        """
        Remove first occurrence of value.

        Raises ValueError if the value is not present.
        """
        for page in self.pages[:]:
            self._load_page(page)
            if item in page:
                page.remove(item)
                return
            if not page:
                self._delete_page(page)

        raise ValueError(f"{item} not in list")

    def reverse(self):
        """ Reverse *IN PLACE*. """
        self.pages.reverse()
        for page in self.pages:
            page = self._load_page(page)
            new_data = list(reversed(page))
            page.clear()
            page.extend(new_data)
            self._store_page(page)

    def sort(self, key=None, reverse=False):
        """ Implements an IN PLACE hybrid of quicksort and merge sort.
        See more on https://en.wikipedia.org/wiki/External_sorting
        """
        if key is not None:
            raise NotImplementedError(f"key is not supported.")

        _before = len(self)
        for page in self.pages:
            page = self._load_page(page)
            assert isinstance(page, Page)
            assert len(page) == page.len > 0
            page.sort(reverse=reverse)
            self._store_page(page)
        assert _before == len(self), "bad logic."

        if len(self.pages) == 1:  # then we're done.
            return

        # else ... merge is required.
        working_buffer = []
        for page in self.pages:
            page = self._load_page(page)
            SL = StoredList(data=page)
            working_buffer.append(SL)

        while len(working_buffer) > 1:
            A = working_buffer.pop(0)
            assert isinstance(A, StoredList)
            iterA = iter(A)
            B = working_buffer.pop(0)
            assert isinstance(B, StoredList)
            iterB = iter(B)

            C = StoredList(page_size=self._page_size)
            a, b = next(iterA), next(iterB)

            buffer = []
            while True:
                if len(buffer) == self._page_size:
                    C.extend(buffer)
                    buffer.clear()

                if (reverse and a >= b) or (not reverse and a <= b):
                    buffer.append(a)
                    try:
                        a = next(iterA)
                    except StopIteration:
                        buffer.append(b)
                        C.extend(buffer)
                        C.extend(list(iterB))
                        break
                else:
                    buffer.append(b)
                    try:
                        b = next(iterB)
                    except StopIteration:
                        buffer.append(a)
                        C.extend(buffer)
                        C.extend(list(iterA))
                        break

            working_buffer.append(C)

        L = working_buffer.pop(0)
        assert len(L) == len(self)
        for page in self.pages[:]:
            self._delete_page(page)
        self.extend(L)

    def __add__(self, other):
        """
        A = [1,2,3]
        B = [4,5,6]
        C = A+B
        C = [1,2,3,4,5,6]
        """
        if not isinstance(other, (StoredList, list)):
            raise TypeError
        SL = StoredList(self._page_size)
        SL.extend(self)
        SL.extend(other)
        return SL

    def __contains__(self, item):
        return any(item == i for i in self)

    def __delitem__(self, index):
        _ = self.pop(index)

    def __eq__(self, other):
        """ Return self==value. """
        if not isinstance(other, (StoredList, list)):
            raise TypeError

        if len(self) != len(other):
            return False

        if any(a != b for a, b in zip(self, other)):
            return False
        return True

    def __getitem__(self, item):
        if not isinstance(item, (slice, int)):
            raise TypeError

        if isinstance(item, int):
            if not isinstance(item, int):
                raise TypeError
            if abs(item) > len(self):
                raise IndexError("list index out of range")
            if item < 0:
                item = len(self) + item
            c = 0
            for page in self.pages:
                if c <= item <= page.len + c:
                    ix = item - c
                    self._load_page(page)
                    return page[ix]  # <--- Exit for integer item
                c += page.len

        assert isinstance(item, slice)
        start, stop, step = DataTypes.infer_range_from_slice(item, len(self))

        n_items = abs(stop - start) // step
        if n_items > self._page_size:
            L = list()
        else:
            L = StoredList(page_size=self._page_size)

        if step > 0:
            if start > stop:
                return L  # <-- Exit no data.
            # else ....
            A = 0
            for page in self.pages:
                B = page.len + A
                if stop < A:
                    break
                if B < start:
                    A += page.len
                    continue

                if start >= A:
                    start_ix = start - A
                else:  # A > start:
                    steps = math.ceil((A-start) / step)
                    start_ix = (start + (steps * step)) - A
                if stop < B:
                    stop_ix = stop - A
                else:
                    stop_ix = page.len

                self._load_page(page)
                data = page[start_ix:stop_ix:step]
                L.extend(data)

                A += page.len

        else:  # step < 0 == backward traverse
            if start < stop:
                return L  # <-- Exit no data.
            # else ...
            B = len(self)
            for page in reversed(self.pages):
                A = B - page.len
                if start < A:
                    B -= page.len
                    continue
                if B < stop:
                    break

                if start > B:
                    steps = abs(math.floor((start-B) / step))
                    start_ix = start + (steps * step) - A
                else:  # start <= B
                    start_ix = start-A

                if item.stop is None:
                    stop_ix = None
                else:  # stop - A:
                    stop_ix = max(stop - A, 0)

                if stop_ix is not None and start_ix < stop_ix or start_ix < 0:
                    pass  # the step is bigger than the slice.
                else:
                    self._load_page(page)
                    data = page[start_ix:stop_ix:step]
                    L.extend(data)

                B -= page.len

        return L  # <-- Exit with data.

    def __ge__(self, other):
        """ Return self>=value. """
        return all(a >= b for a, b in zip(self, other))

    def __gt__(self, other):
        """ Return self>value. """
        return all(a > b for a, b in zip(self, other))

    def __iadd__(self, other):
        """ Implement self+=value.
        >>> A = [1,2,3]
        >>> A += [4,5]
        >>> print(A)
        [1,2,3,4,5]
        """
        if not isinstance(other, (StoredList, list)):
            raise TypeError
        self.extend(other)
        return self

    def __imul__(self, value):
        """ Implement self*=value. """
        if not isinstance(value, int):
            raise TypeError
        if value <= 0:
            raise ValueError
        elif value == 1:
            return self
        else:
            new_list = StoredList(page_size=self._page_size)
            for i in range(value):
                new_list.extend(self)
            return new_list

    def __le__(self, other):
        """ Return self<=value. """
        return all(a <= b for a, b in zip(self, other))

    def __lt__(self, other):
        """ Return self<value. """
        return all(a < b for a, b in zip(self, other))

    def __mul__(self, value):
        """ Return self*value. """
        if not isinstance(value, int):
            raise TypeError
        if value <= 0:
            raise ValueError
        new_list = StoredList(page_size=self._page_size)
        for i in range(value):
            new_list += self
        return new_list

    def __ne__(self, other):
        """ Return self!=value. """
        if not isinstance(other, (StoredList, list)):
            raise TypeError
        if len(self) != len(other):
            return True
        return any(a != b for a, b in zip(self, other))

    def __rmul__(self, value):
        """ Return value*self. """
        return self.__mul__(value)

    def __setitem__(self, key, value):
        """ Set self[key] to value. """
        if not isinstance(key, int):
            raise TypeError
        if abs(key) > len(self):
            raise KeyError("index out of range")
        c = 0
        if key < 0:
            key = len(self) + key

        for page in self.pages:
            if c < key < c + page.len:
                self._load_page(page)
                ix = key - c
                page[ix] = value
                return

    def __sizeof__(self):
        """ Return the size of the list in memory, in bytes.
        To drop any cached data, call `clear_cache()`

        """
        return sum(p.__sizeof__() for p in self.pages)

    def clear_cache(self):
        _ = [self._store_page(p) for p in self.pages if p.loaded]

    def disk_size(self):
        """ drops all pages to disk using `clear_cache` and then
        returns the number of bytes stored """
        self.clear_cache()
        return sum(p.size for p in self.pages)

    def __hash__(self):
        raise TypeError("unhashable type: List")

    def __copy__(self):
        SL = StoredList(self._page_size)
        for page in self.pages:
            self._load_page(page)
            SL.extend(page)  # page data is copied in the extend function
        return SL

