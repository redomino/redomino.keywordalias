# Copyright (c) 2012 Redomino srl (http://redomino.com)
# Authors: Davide Moro <davide.moro@redomino.com> and contributors
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

from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from redomino.keywordalias.interfaces import IKeywords

def get_storage():
    """ Get the keyword settings storage """
    registry = getUtility(IRegistry)
    keyword_settings = registry.forInterface(IKeywords)
    return keyword_settings

