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
"""CPSUid XML adapters

$Id$
"""

from zope.component import adapts
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import ObjectManagerHelpers

from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.interfaces import ISetupEnviron

from Products.CPSUtil.PropertiesPostProcessor import \
     PostProcessingPropertyManagerHelpers

from Products.CPSUid.interfaces import IUidHandler
from Products.CPSUid.interfaces import IUidGenerator


UID_TOOL = 'portal_uid'
UID_NAME = 'uidgenerators'


def exportUidTool(context):
    """Export uid tool as a set of XML files.
    """
    site = context.getSite()
    tool = getToolByName(site, UID_TOOL, None)
    if tool is None:
        logger = context.getLogger(UID_NAME)
        logger.info("Nothing to export.")
        return
    exportObjects(tool, '', context)


def importUidTool(context):
    """Import uid tool from a set of XML
    files.
    """
    site = context.getSite()
    tool = getToolByName(site, UID_TOOL)
    importObjects(tool, '', context)


class UidToolXMLAdapter(XMLAdapterBase, ObjectManagerHelpers):
    """XML importer and exporter for Uid tool.
    """
    adapts(IUidHandler, ISetupEnviron)
    implements(IBody)

    _LOGGER_ID = UID_NAME
    name = UID_NAME

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        node.appendChild(self._extractObjects())
        self._logger.info("Uid tool exported.")
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeObjects()
        self._initObjects(node)
        self._logger.info("Uid tool imported.")


class UidGeneratorXMLAdapter(XMLAdapterBase,
                             PostProcessingPropertyManagerHelpers):
    """XML importer and exporter for a uid generator.
    """
    adapts(IUidGenerator, ISetupEnviron)
    implements(IBody)

    _LOGGER_ID = UID_NAME

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        node.appendChild(self._extractProperties())
        self._logger.info("%s uid generator exported." % self.context.getId())
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeProperties()
        self._initProperties(node)
        self._logger.info("%s uid generator imported." % self.context.getId())
