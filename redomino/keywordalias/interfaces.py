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

from zope.interface import Interface
from zope import schema

from redomino.keywordalias import keywordaliasMessageFactory as _


class IKeywordAlias(Interface):

    keyword = schema.TextLine(title=_(u'keyword_label', default=u"Keyword"))
    keywords = schema.List(title=_(u'aliases_label', default=u"Aliases"), value_type=schema.TextLine(title=_(u'alias_label', default=u"Alias")), required=False)

class IKeywords(Interface):
    keyword_storage = schema.Dict(title=_(u'keywords_label', default=u'Keywords'),
                           key_type=schema.TextLine(title=_(u'keywordkeytype_label', default=u"Keyword")),
                           value_type=schema.List(title=_(u'values_label', default=u"Values"), value_type=schema.TextLine(title=_(u'value_label', default=u"Value"))))

