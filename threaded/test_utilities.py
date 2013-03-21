#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# test_utilities.py
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
Test module for utilities.py
"""

import unittest
from utilities import CycleQueue

elements = ['a','b','c','d']

class TestCycleQueue(unittest.TestCase):


    def test_lock(self):

        q = CycleQueue()
        for e in elements:
            q.put(e)

        q.lockstate()
        for i in xrange(len(elements)):
            self.assertTrue(
                q._backup[i] == q.queue[i]
            )

    def test_reinit(self):

        q = CycleQueue()
        for e in elements:
            q.put(e)

        q.lockstate()

        # unqueue some elements
        q.get(); q.task_done()
        q.get(); q.task_done()

        # get back to initial state
        q.reinit()

        for i in xrange(len(elements)):
            self.assertTrue(
                q._backup[i] == elements[i]
            )


if __name__=='__main__':
    unittest.main()
