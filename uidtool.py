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
"""Tool for uid management
"""

from logging import getLogger

from zope.interface import implements

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder

from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import View, ManagePortal

from Products.CPSUid.interfaces import IUidHandler
from Products.CPSUid.uidgenerator import UidGenerator

_marker = []


class UidTool(UniqueObject, Folder):
    """Uid tool to manage document uids
    """

    id = 'portal_uid'
    meta_type = 'CPS Uid Tool'

    implements(IUidHandler)

    security = ClassSecurityInfo()

    logger = getLogger('UidTool')

    # XXX uid setting is done at the field (in schema) level for now

    security.declareProtected(View, 'getUid')
    def getUid(self, generator_id, default=_marker, **kw):
        """Get uid using given generator_id according to keywords
        """
        generator = self._getOb(generator_id, default=None)
        if generator is not None:
            uid = generator.getUid(**kw)
        else:
            if default is _marker:
                raise AttributeError, generator_id
            else:
                uid = default
        return uid


    security.declareProtected(View, '__getitem__')
    def __getitem__(self, uid, default=_marker):
        """Get object with given uid

        Present the most relevant document if several objects are found.
        """
        # check the uid index exists
        ctool = getToolByName(self, 'portal_catalog')
        try:
            ctool.getIndex('uid')
        except KeyError:
            self.logger.info("uid index is not set")
            if default is _marker:
                raise AttributeError, uid
        res = default
        brains = ctool.searchResults(uid=uid)
        if brains:
            # XXX take first result for now
            res = brains[0]
        elif default is _marker:
            raise AttributeError, uid
        return res

    # ZMI

    security.declareProtected(ManagePortal, 'manage_addUidGenerator')
    def manage_addUidGenerator(self, id, generation_criteria,
                               generation_keywords, generation_expression,
                               REQUEST=None):
        """Add a uid generator TTW"""
        generator = UidGenerator(id, generation_criteria=generation_criteria,
                                 generation_keywords=generation_keywords,
                                 generation_expression=generation_expression)
        self._setObject(id, generator)
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url()+'/manage_main'
                                      '?manage_tabs_message=Generator Added.')

InitializeClass(UidTool)
