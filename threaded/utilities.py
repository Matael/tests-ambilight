#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# utilities.py
#
# Copyright © 2013 Mathieu Gaborit (matael) <mathieu@matael.org>
#
#
# Distributed under WTFPL terms
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

"""
Some utilities for other ambilight scripts
"""

import Queue

class CycleQueue(Queue.Queue):
    """ Particular Queue with new method reinit to get back to
    initial state.

    Standard use :

        q = CycleQueue()

        q.put('elem1')
        q.put('elem2')
        # etc...

        # lock current state, say state1
        q.lockstate()

        q.get()
        # etc... 'till queue is empty

        q.reinit() # get back to state1

    """

    def __init__(self, *args, **kw):
        Queue.Queue.__init__(self, *args, **kw)
        self._backup = []

    def lockstate(self):
        """ Lock current state """

        for i in self.queue:
            self._backup.append(i)


    def reinit(self):
        """ Get back to previous locked state """

        # check if a non-empty backup exists
        if self._backup == []:
            raise IndexError('Backup list is empty')

        # reset the queue
        self.queue.clear()

        # push locked elements back to queue
        for t in self._backup: self.put(t)

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance.  Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """

        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
