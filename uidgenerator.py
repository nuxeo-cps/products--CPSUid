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
"""Unique identifier generator

Generators hold rules to build identifiers given parameters and also hold
counters.
"""

from logging import getLogger
from DateTime import DateTime

from zope.interface import implements

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.Folder import Folder

from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import getEngine

from Products.CPSUtil.PropertiesPostProcessor import PropertiesPostProcessor
from Products.CPSUtil.id import generateId

from Products.CPSUid.interfaces import IUidGenerator
from Products.CPSUid.uidcounter import UidCounter

class UidGenerator(PropertiesPostProcessor, Folder):
    """Uid Generator

    XXX set persistent right now so that it can hold expressions and counters
    in the ZODB
    """

    implements(IUidGenerator)

    meta_type = 'Uid Generator'

    security = ClassSecurityInfo()

    _propertiesBaseClass = Folder
    _properties = (
        {'id': 'generation_expression', 'type': 'string', 'mode': 'w',
         'label': 'Generation expression'},
        {'id': 'generation_criteria', 'type': 'tokens', 'mode': 'w',
         'label': 'Generation criteria'},
        {'id': 'generation_keywords', 'type': 'tokens', 'mode': 'w',
         'label': 'Generation keywords'},
        {'id': 'counter_start', 'type': 'int', 'mode': 'w',
         'label': 'Counter start value'},
        )
    _properties_post_process_tales = (
        ('generation_expression', 'generation_expression_c'),
        )
    generation_expression = ''
    generation_expression_c = None
    generation_criteria = ()
    # XXX generation criteria are generation keywords by default
    generation_keywords = ()
    counter_start = 0

    manage_options = Folder.manage_options

    logger = getLogger("CPSUid.UidGenerator")

    #
    # API
    #

    def __init__(self, id, **kw):
        """Initialization
        """
        self.id = id
        self.manage_changeProperties(**kw)


    security.declareProtected(View, 'getUid')
    def getUid(self, **kw):
        """Get unique identifier value
        """
        if self.generation_expression_c:
            expr = self._createGenerationExpressionContext(**kw)
            uid = self.generation_expression_c(expr)
        else:
            uid = None
        return uid


    security.declarePrivate('_createGenerationExpressionContext')
    def _createGenerationExpressionContext(self, **kw):
        """Create an expression context for generation evaluation.
        """
        # mapping is filled in reverse order so that most important keywords
        # are not overloaded
        mapping = {}
        # generation additional keywords
        for keyword in self.generation_keywords:
            mapping[keyword] = kw.get(keyword)
        mapping['DateTime'] = DateTime
        # counter
        criteria = {}
        # generation criteria
        for keyword in self.generation_criteria:
            criteria[keyword] = kw.get(keyword)
        counter = self._getCounter(**criteria)
        mapping.update(criteria)
        mapping['number'] = counter.hit()
        mapping['portal'] = getToolByName(self, 'portal_url').getPortalObject()
        self.logger.debug(mapping)
        return getEngine().getContext(mapping)


    security.declarePrivate('_getCounter')
    def _getCounter(self, **criteria):
        """Get counter for given keyword criteria
        """
        winner = None
        for counter in self.objectValues():
            if criteria == counter.getCriteria():
                winner = counter
                break
        if winner is None:
            # create it
            counter = self._createCounter(**criteria)
        return counter


    security.declarePrivate('_createCounter')
    def _createCounter(self, **criteria):
        """Create a counter using given keyword criteria
        """
        # create an id from criteria
        if not criteria:
            raise ValueError("cannot create counter with empty criteria")
        counter_id_list = []
        for key, value in criteria.items():
            counter_id_list.append("%s-%s"%(key, value))
        counter_id = '_'.join(counter_id_list)
        counter_id = generateId(counter_id, max_chars=100)
        counter = UidCounter(counter_id, self.counter_start, criteria)
        self._setObject(counter_id, counter)
        return self._getOb(counter_id)


InitializeClass(UidGenerator)
