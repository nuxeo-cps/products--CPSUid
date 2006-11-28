# (C) Copyright 2006 Nuxeo SAS <http://nuxeo.com>
# Authors:
# - Anahide Tchertchian <at@nuxeo.com>
# - Florent Guillaume <fg@nuxeo.com>
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
import logging

from zope.interface import implements
from transaction import TransactionManager

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from ZODB.POSException import ConflictError

from Products.CMFCore.utils import SimpleItemWithProperties

from Products.CPSUid.interfaces import IUidCounter

logger = logging.getLogger('CPSUid.uidcounter')

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

    max_tries = 5

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
        """Hit the counter: return current counter and increment its value.

        Fires a dedicated micro transaction to diminish risks of conflicts
        because we definitely *don't* want to resolve them (that breaks
        returned values' unicity).

        """
        db = self._p_jar.db()

        retries = self.max_tries
        while retries:
            try:
                logger.debug(
                    "Hitting on counter %s, trying %d times", self, retries)
                tm = TransactionManager()

                cnx = db.open(transaction_manager=tm)
                tm.begin()
                ob = cnx.get(self._p_oid)

                v = ob.counter_current
                ob.counter_current = v + 1

                tm.commit()
                cnx.close()
            except ConflictError:
                logger.debug('ConflictError')
                tm.abort()
                cnx.close()
                retries -= 1
            else:
                break
        else:
            # exhausted all tries
            raise ConflictError
        return v

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
            if ' ' in mapping:
                key, value = mapping.split(' ', 1)
                criteria_dict[key] = value
        return criteria_dict

InitializeClass(UidCounter)
