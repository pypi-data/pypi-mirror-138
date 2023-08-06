#!/usr/bin/env python3
#
# Copyright 2022 Jonathan L. Komar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import abc
from fpinpy.meta.decorators import overrides
from typing import Iterator, TypeVar, Generic, Callable
# Declare module-scoped type variables for generics
T = TypeVar('T')
U = TypeVar('U')

class SinglyLinkedListIterator:
    """Forward and backward iterator

        This is intended to provide an iterative, performant way
        to implement exposed functions. The iterator itself
        is not intended to be exposed to the outside, although
        it can be used.
    """
    def __init__(self, singly_linked_list, reverse: bool=False):
        if reverse:
            self._state = self._make_reversed_state(singly_linked_list)
        else:
            self._state = singly_linked_list

    def __iter__(self):
        return self

    def __next__(self):
        """
            Does not return Nil
        """
        if not self._state.isEmpty():
            next_elem = self._state.head()
            self._state= self._state.tail()
            return next_elem
        else:
            raise StopIteration

    def _make_reversed_state(self, aList):
        """ Iterative implementation of traversing the list backwards.


            Recursive implementation

            def _reversed(acc, aList):
                if aList.isEmpty():
                    return acc
                else:
                    return _reversed(SinglyLinkedList.cons(internal_state.head(), accumulator), internal_state.tail())
            return _reversed(accumulator, aList)
        """
        internal_state = aList
        stack = [] # LIFO
        while not internal_state.isEmpty():
            head = internal_state.head()
            tail = internal_state.tail()
            internal_state = internal_state.tail()
            stack.append(head)
        return SinglyLinkedList.list(*reversed(stack))

class SinglyLinkedList(Generic[T]): # Generic[T] is a subclass of metaclass=ABCMeta (ABC)
    """The base class for singly-linked list objects
    """

    @staticmethod
    def list(*args):
        if len(args) == 0:
            return SinglyLinkedList.nil()
        else:
            output = SinglyLinkedList.nil()
            for i in range(len(args)-1, -1, -1):
                output = Cons(args[i], output)
            return output

    @classmethod
    def nil(cls):
        """Returns singleton Nil.

        """
        return Nil()

    @classmethod
    def cons(cls, head: T, tail):# Tail is Cons[T]
        return Cons(head, tail)

    def __iter__(self):
        """ Non-functional iterator for performance in some cases.

            This is not intended for use outside of this class, but
            was added here for ease of iterating the list using data
            sharing.
        """
        return SinglyLinkedListIterator(self)

    def __reversed__(self):
        return SinglyLinkedListIterator(self, reverse=True)

    @abc.abstractmethod
    def head(self):
        raise NotImplementedError

    @abc.abstractmethod
    def tail(self):# -> SinglyLinkedList[T]
        raise NotImplementedError

    @abc.abstractmethod
    def isEmpty(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def setHead(self, head: T):# -> SinglyLinkedList[T]
        """Instance method to replace first element

            of list with a new value.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def length() -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def reverse(self):
        return SinglyLinkedList.list(*reversed(self))

    @abc.abstractmethod
    def foldLeft(self, identity: U, function: Callable[[U], Callable[[T], U]]):
        raise NotImplementedError

    #@abc.abstractmethod
    #def foldRight(self, identity: U, function: Callable[[U], Callable[[T], U]]):
    #    return self.reverse().foldLeft(identity, lambda x: lambda y: function(y)(x))

    def map(self, function: Callable[T, U]):# -> SinglyLinkedList[U]:
        """ Map a function T -> U to each element in a list.

            Map can be defined here in the superclass for both subclasses,
            because the implementation is abstracted enough to allow for this.
        """
        #return self.foldLeft(self.list(), lambda h: lambda t: self.cons(function(h), t))
        accumulator = []
        for elem in self:
            accumulator.append(function(elem))
        return SinglyLinkedList.list(*accumulator)

    @abc.abstractmethod
    def drop(self, n: int):
        """Remove n elements from the front of the list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

class Nil(SinglyLinkedList[T]):
    """Represents empty list.
    """

    def __init__(self):
        pass

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    @overrides(SinglyLinkedList)
    def head(self) -> T:
        raise RuntimeError("head called on empty list")

    @overrides(SinglyLinkedList)
    def tail(self) -> SinglyLinkedList[T]:
        raise RuntimeError("tail called on empty list")

    @overrides(SinglyLinkedList)
    def isEmpty(self) -> bool:
        return True

    @overrides(SinglyLinkedList)
    def setHead(self, head: T):# -> SinglyLinkedList[T]
        raise RuntimeError("setHead called on empty list.")

    @overrides(SinglyLinkedList)
    def length(self) -> int:
        return 0

    @overrides(SinglyLinkedList)
    def foldLeft(self, identity: U, function: Callable[[U, T], U]):# TODO add out type
        """ Nil implementation returns the identity element (Neutral). """
        return identity

    @overrides(SinglyLinkedList)
    def drop(self, n: int) -> SinglyLinkedList[T]:
        return self

    @overrides(SinglyLinkedList)
    def __str__(self):
        return "[NIL]"

    def __repr__(self):
        return "Nil"

    def __eq__(self, o):
        return instanceof(Nil, o)

class Cons(SinglyLinkedList[T]):
    """Represents non-empty list.
    """

    def __init__(self,
                 head: T,
                 tail: SinglyLinkedList[T]):
        self._head = head
        assert isinstance(tail, Cons) or isinstance(tail, Nil), f"Type was {type(tail)} but should have been Cons or Nil"
        self._tail = tail
        self._length = tail.length() + 1

    @overrides(SinglyLinkedList)
    def head(self) -> T:
        return self._head

    @overrides(SinglyLinkedList)
    def tail(self) -> SinglyLinkedList[T]:
        return self._tail

    @overrides(SinglyLinkedList)
    def isEmpty(self) -> bool:
        return False

    @overrides(SinglyLinkedList)
    def setHead(self, head: T) -> SinglyLinkedList[T]:
        return SinglyLinkedList.cons(head, self.tail())

    @overrides(SinglyLinkedList)
    def length(self):
        return self._length

    @overrides(SinglyLinkedList)
    def drop(self, n: int) -> SinglyLinkedList[T]:
        if n <= 0:
            """Case 0 or negative"""
            return self
        else:
            """Case >0 until 0 or list is Nil"""
            def _drop_iterative(n: int) -> SinglyLinkedList[T]:
                # init state
                output = self
                while n != 0 and not output.isEmpty():
                    # next state
                    output = output.tail()
                    n -= 1
                return output
            return _drop_iterative(n)

    @overrides(SinglyLinkedList)
    def foldLeft(self, identity: U, function: Callable[[U], Callable[[T], U]]) -> U:
        """ Implemented imperatively as technique to avoid too many stack calls.

            Alternatively, an iterator could be defined for this list so that a for loop
            can be used.

            Usage: folderLeft(list(), lambda head: lambda tail: Cons(function(h), t)

            Effective recursive implementation

            def _foldLeft(acc: U, lst: SinglyLinkedList[T]):
                if lst.isEmpty():
                    return acc
                else:
                    return _foldLeft(function(acc)(lst.head()), lst.tail())
            return _foldLeft(identity, self)

        """
        accumulator = identity # (empty/Nil)
        for elem in self:
           accumulator = function(accumulator)(elem)
        return accumulator

    @overrides(SinglyLinkedList)
    def __str__(self) -> str:
        accumulator = ""
        def toString(accumulator: str, aList: SinglyLinkedList) -> str:
            if aList.isEmpty():
                return accumulator
            else:
                accumulator = accumulator.__add__(str(aList.head())).__add__(", ")
                return toString(accumulator , aList.tail())
        return f"[{toString(accumulator, self)}NIL]"

    def __repr__(self) -> str:
        accumulator = ""
        def toString(accumulator: str, aList: SinglyLinkedList) -> str:
            if aList.isEmpty():
                return accumulator + ", " + repr(aList) + ")"
            else:
                accumulator = accumulator + f"Cons(" + repr(aList.head())
                return toString(accumulator, aList.tail())
        return f"{toString(accumulator, self)}"
