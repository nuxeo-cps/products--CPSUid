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
"""Upgrades

$Id$
"""

from logging import getLogger
from Products.CMFCore.utils import getToolByName

def checkUidCounters(self):
    upgrade = 0
    uidtool = getToolByName(self, 'portal_uid', None)
    if uidtool is not None:
        for generator in uidtool.objectValues('Uid Generator'):
            for counter in generator.objectValues('Uid Counter'):
                if isinstance(counter.criteria, dict):
                    upgrade = 1
                    break
    return upgrade


def upgradeUidCounters(self):
    """Upgrade uid counters, turning their criteria property into lines
    """
    logger = getLogger('upgradeUidCounters')
    nchanged = 0
    uidtool = getToolByName(self, 'portal_uid', None)
    if uidtool is not None:
        for generator in uidtool.objectValues('Uid Generator'):
            for counter in generator.objectValues('Uid Counter'):
                criteria = counter.criteria
                if isinstance(criteria, dict):
                    logger.debug("upgrading %s" % counter.absolute_url())
                    criteria_lines = list(['%s %s'%(key, value)
                                           for key, value in criteria.items()])
                    counter._setPropValue('criteria', criteria_lines)
                    nchanged += 1
    logger.debug("%s objects upgraded" % nchanged)
    return '%s objects upgraded' % nchanged


def upgrade(self):
    if checkRootWorkflows(self):
        upgradeRootWorkflows(self)
