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
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.component import adapter
from zope.schema.interfaces import IField

from z3c.form.browser.text import TextWidget
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IFieldWidget

class IKeywordLangKey(Interface):
    """ Marker interface for Display keyword lang key """

@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def KeywordLangKey(field, request):
    field_widget = TextWidget(request)
    alsoProvides(field_widget, IKeywordLangKey)
    return FieldWidget(field, field_widget)

