# Copyright (c) 2006 Nuxeo SAS <http://nuxeo.com>
# Authors:
# - Anahide Tchertchian <at@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
"""Tests for the uid counter module

$Id$
"""

import unittest

from zope.interface.verify import verifyClass

from Products.CPSUid.interfaces import IUidCounter
from Products.CPSUid.uidcounter import UidCounter

class TestUidCounter(unittest.TestCase):

    # fixture

    def setUp(self):
        # add a test counter
        self.criteria = {
            "source": "CPS",
            "doument_type": "Common type",
            }
        self.criteria_lines = (
            "source CPS",
            "doument_type Common type",
            )
        self.counter = UidCounter("counter", 1, self.criteria)

    # tests

    def test_interface(self):
        verifyClass(IUidCounter, UidCounter)

    def test_creation(self):
        criteria = {
            "source": "CPS",
            "doument_type": "Common type",
            }
        counter = UidCounter("counter", 1, criteria)
        self.assertEqual(counter.meta_type, "Uid Counter")
        self.assertEqual(counter.getId(), "counter")
        self.assertEqual(counter.counter_start, 1)
        self.assertEqual(counter.counter_current, 1)
        self.assertEqual(counter.getCriteria(), criteria)

    def test_test_case_counter(self):
        self.assertEqual(self.counter.meta_type, "Uid Counter")
        self.assertEqual(self.counter.getId(), "counter")
        self.assertEqual(self.counter.counter_start, 1)
        self.assertEqual(self.counter.counter_current, 1)
        self.assertEqual(self.counter.criteria, self.criteria_lines)

    def test_hit(self):
        self.assertEqual(self.counter.counter_current, 1)
        self.assertEqual(self.counter.hit(), 1)
        self.assertEqual(self.counter.counter_current, 2)
        self.assertEqual(self.counter.hit(), 2)
        self.assertEqual(self.counter.counter_current, 3)

    def test_reset(self):
        self.assertEqual(self.counter.counter_current, 1)
        self.counter.counter_current = 3
        self.assertEqual(self.counter.counter_current, 3)
        self.counter.reset()
        self.assertEqual(self.counter.counter_current, 1)

    def test__getCriteria(self):
        self.assertEqual(self.counter.getCriteria(), self.criteria)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUidCounter))
    return suite
