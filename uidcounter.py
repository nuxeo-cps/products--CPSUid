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
"""Unique identifier counter

A counter holds criteria and an integer counter applying to these criteria
"""

from zope.interface import implements

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import SimpleItemWithProperties

from Products.CPSUid.interfaces import IUidCounter

class UidCounter(SimpleItemWithProperties):
    """Uid Counter

    XXX set persistent right now so that it can hold criteria and counters in
    the ZODB
    """

    implements(IUidCounter)

    meta_type = 'Uid Counter'

    security = ClassSecurityInfo()

    _properties = (
        {'id': 'counter_start', 'type': 'int', 'mode': 'w',
         'label': 'Counter start value'},
        {'id': 'counter_current', 'type': 'int', 'mode': 'w',
         'label': 'Counter current value'},
        # one criteria per line, following the format "key value", for
        # instance:
        # portal_type Workspace
        # type CPS
        {'id': 'criteria', 'type': 'lines', 'mode': 'w',
         'label': 'Criteria mapping'},
        )

    #
    # API
    #

    def __init__(self, id, counter_start=0, criteria={}):
        """Initialization
        """
        self.id = id
        self._setPropValue('counter_start', counter_start)
        self._setPropValue('counter_current', counter_start)
        criteria_lines = list(['%s %s'%(key, value)
                               for key, value in criteria.items()])
        self._setPropValue('criteria', criteria_lines)


    security.declarePrivate('hit')
    def hit(self):
        """Hit the counter: return current counter and increment its value

        XXXXXX GR. Currently the conflict resolving system breaks the
        counter unicity because two conflicting threads will get the same
        value and the transaction will be replayed.
        We should make an independent micro-transaction here with its own
        ZODB connection and implement a replay system like the publisher's.
        """
        # XXX AT: this is were conflict issues should be handled (?)
        counter_value = self.counter_current
        self.counter_current = counter_value + 1
        return counter_value


    security.declarePrivate('reset')
    def reset(self):
        """Reset the counter
        """
        self.counter_current = self.counter_start


    security.declarePrivate('getCriteria')
    def getCriteria(self):
        """Get the counter criteria
        """
        criteria_dict = {}
        for mapping in self.criteria:
            sep_index = mapping.find(' ')
            if sep_index != -1:
                key = mapping[:sep_index]
                value = mapping[sep_index+1:]
                criteria_dict[key] = value
        return criteria_dict

    # avoid conflicts on counter current value
    def _p_resolveConflict(self, oldState, savedState, newState):
        """Avoid conflicts when changing the counter value
        """
        # XXX GR: this does resolve conflicts, but the two callers got the same
        # number, hence really need to randomize the uid to enforce unicity
        bigger_counter = max(savedState['counter_current'],
                             newState['counter_current'])
        newState['counter_current'] = bigger_counter + 1
        return newState


InitializeClass(UidCounter)
