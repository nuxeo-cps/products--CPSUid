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
"""Tests for the uid generator module

$Id$
"""

import unittest

from OFS.Folder import Folder

from zope.interface.verify import verifyClass

from Products.CPSUid.interfaces import IUidGenerator
from Products.CPSUid.uidgenerator import UidGenerator


class FakeUrlTool(Folder):

    def getPortalObject(self):
        return self.aq_inner.aq_parent

class TestUidGenerator(unittest.TestCase):

    # fixture

    def setUp(self):
        # add a test generator
        self.generation_criteria = ('source',)
        self.generation_keywords = ('portal_type',)
        # TAL expression to build the id as D-S-YY-NNN with D as document type,
        # S as source,YY as the current yea and NNN an incremented number
        self.expression = "python:str(portal_type)+'-'+str(source)+'-'+DateTime().strftime('%y')+'-'+'%#03d'%number"
        folder = Folder('folder')
        generator = UidGenerator(
            'generator',
            generation_criteria=self.generation_criteria,
            generation_keywords=self.generation_keywords,
            generation_expression=self.expression)
        folder._setObject('generator', generator)
        self.generator = folder.generator

        # add a fake url tool
        folder._setObject('portal_url', FakeUrlTool())

    # tests

    def test_interface(self):
        verifyClass(IUidGenerator, UidGenerator)

    def test_creation(self):
        expression = "python:str(foo)+'_'+str(bar)"
        generator = UidGenerator('generator', generation_criteria=('foo'),
                                 generation_keywords=('bar'),
                                 generation_expression=expression)
        self.assertEqual(generator.meta_type, "Uid Generator")
        self.assertEqual(generator.getId(), 'generator')
        self.assertEqual(generator.generation_criteria, ('foo',))
        self.assertEqual(generator.generation_keywords, ('bar',))
        self.assertEqual(generator.generation_expression, expression)
        self.assertNotEqual(generator.generation_expression_c, None)

    def test_test_case_generator(self):
        self.assertEqual(self.generator.meta_type, "Uid Generator")
        self.assertEqual(self.generator.getId(), 'generator')
        self.assertEqual(self.generator.generation_criteria,
                         self.generation_criteria)
        self.assertEqual(self.generator.generation_keywords,
                         self.generation_keywords)
        self.assertEqual(self.generator.generation_expression,
                         self.expression)
        self.assertNotEqual(self.generator.generation_expression_c, None)

    def test_getUid(self):
        kw = {
            'portal_type': 'file_document',
            'source': 'CPS',
            }
        uid = self.generator.getUid(**kw)
        self.assertEqual(uid, 'file_document-CPS-06-000')
        new_uid = self.generator.getUid(**kw)
        self.assertEqual(new_uid, 'file_document-CPS-06-001')
        # hit again
        newer_uid = self.generator.getUid(**kw)
        self.assertEqual(newer_uid, 'file_document-CPS-06-002')


    def test__getCounter(self):
        criteria = {
            'source': 'CPS',
            }
        criteria_lines = (
            'source CPS',
            )
        counter = self.generator._getCounter(**criteria)
        self.assertEqual(counter.getId(), 'source-cps')
        self.assertEqual(counter.counter_start, 0)
        self.assertEqual(counter.counter_current, 0)
        self.assertEqual(counter.criteria, criteria_lines)
        self.assertEqual(counter.getCriteria(), criteria)


    def test___createCounter(self):
        criteria = {
            'source': 'CPS',
            }
        counter = self.generator._createCounter(**criteria)
        self.assertEqual(counter.getId(), 'source-cps')
        self.assertEqual(counter.counter_start, 0)
        self.assertEqual(counter.counter_current, 0)
        self.assertEqual(counter.getCriteria(), criteria)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUidGenerator))
    return suite
