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
"""Init

$Id$
"""
from Products.CMFCore.utils import ContentInit, ToolInit
from Products.CMFCore.permissions import AddPortalContent, ManagePortal

from Products.GenericSetup import profile_registry
from Products.GenericSetup import EXTENSION
from Products.CPSCore.interfaces import ICPSSite

from Products.CPSUid.uidtool import UidTool
from Products.CPSUid.uidgenerator import UidGenerator

def initialize(registrar):

    ToolInit(
        'CPS Tools',
        tools=(UidTool,),
        icon='tool.png',
        ).initialize(registrar)

    registrar.registerClass(
        UidGenerator,
        permission=ManagePortal,
        constructors=(UidTool.manage_addUidGenerator,),
        )

    profile_registry.registerProfile(
        'default',
        'CPS Uid',
        "Ujnique identifier product for CPS.",
        'profiles/default',
        'CPSUid',
        EXTENSION,
        for_=ICPSSite)
