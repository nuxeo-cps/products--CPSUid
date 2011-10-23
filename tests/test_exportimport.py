# (C) Copyright 2006 Nuxeo SAS <http://nuxeo.com>
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
"""Tests for the CPScore export/import mechanism
"""

import os
import unittest
from Testing import ZopeTestCase

from Products.CPSUtil.testing.genericsetup import ExportImportTestCase

ZopeTestCase.installProduct('CPSUid')

TEST_PROFILES_PATH = os.path.join(os.path.split(__file__)[0], 'profiles')

class ExportImportTest(ExportImportTestCase):

    def beforeTearDown(self):
        ExportImportTestCase.beforeTearDown(self)
        self.clearProfileRegistry()


    def test_default_import(self):
        self.registerProfile('default', "CPS Uid", "Default profile",
                             'profiles/default', 'CPSUid')
        self.assertEquals('portal_uid' in self.folder.objectIds(),
                          False)
        self.importProfile('CPSUid:default')

        # check portal_uid
        self.assertEquals('portal_uid' in self.folder.objectIds(),
                          True)


    def test_default_export(self):
        self.registerProfile('default', "CPS Uid", "Default profile",
                             'profiles/default', 'CPSUid')
        self.importProfile('CPSUid:default')
        toc_list = [
            'export_steps.xml',
            'import_steps.xml',
            'uidgenerators.xml',
            ]
        self._checkExportProfile(os.path.join(TEST_PROFILES_PATH,
                                              'default_export'), toc_list)


    def test_basic_import(self):
        self.registerProfile('basic', "CPS Uid", "Basic profile",
                             'tests/profiles/basic', 'CPSUid')
        self.assertEquals('portal_uid' in self.folder.objectIds(), False)
        self.importProfile('CPSUid:basic')
        self.assertEquals('portal_uid' in self.folder.objectIds(), True)
        uidtool = self.folder.portal_uid
        self.assertEquals(uidtool.meta_type, 'CPS Uid Tool')
        self.assertEquals(list(uidtool.objectIds()), ['generator'])
        generator = uidtool.generator
        self.assertEqual(generator.meta_type, "Uid Generator")
        self.assertEqual(generator.getId(), 'generator')
        self.assertEqual(generator.generation_criteria,
                         ('source',),)
        self.assertEqual(generator.generation_keywords,
                         ('portal_type',))
        # FIXME: import should not keep the extra leadin \n character
        expr = "\npython:str(portal_type)+'-'+str(source)+'-'+DateTime().strftime('%y')+'-'+'%#03d'%number"
        self.assertEqual(generator.generation_expression, expr)
        self.assertNotEqual(generator.generation_expression_c, None)
        self.assertEqual(generator.counter_start, 1)


    def test_basic_export(self):
        self.registerProfile('basic', "CPS Uid", "Basic profile",
                             'tests/profiles/basic', 'CPSUid')
        self.importProfile('CPSUid:basic')
        toc_list = [
            'export_steps.xml',
            'import_steps.xml',
            'uidgenerators.xml',
            'uidgenerators/generator.xml',
           ]
        self._checkExportProfile(os.path.join(TEST_PROFILES_PATH, 'basic'),
                                 toc_list)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ExportImportTest),
        ))

