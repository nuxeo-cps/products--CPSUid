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
"""CPSUid interfaces

$Id$
"""

from zope.interface import Interface

class IUidHandler(Interface):
    """Unique identifier handler
    """

    def getGenerator(**kw):
        """Get generator for given counter criteria

        If the generator does not exist yet, it is created
        """


class IUidGenerator(Interface):
    """Unique identifier generator
    """

    def getUid():
        """
        """

    def _getCounter(**criteria):
        """Get counter for given keywords
        """

    def _createCounter(**criteria):
        """Create a counter using given keyword criteria
        """


class IUidCounter(Interface):
    """Unique identifier counter
    """

    def getCriteria():
        """Get the counter criteria
        """

    def hit():
        """Hit the counter, increment its value
        """

    def reset():
        """Reset the counter
        """
