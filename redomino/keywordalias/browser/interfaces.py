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

class IRedominoKeywordAliasLayer(Interface):
    """ Layer interface """

class IKeywordTranslator(Interface):
    """ This view let you get the translated version of a keyword for
        a given language, if available with this order:

        1 - the keyword lang version
        2 - the default alias
        3 - the keyword itself

    """

    def __call__():
        """ Calling this component it tries to fetch from the request
            a keyword to translate.
        """

    def translate(keyword=None):
        """ Try to translate the given keyword.
            If no keyword is given it tries to fetch the keyword to
            translate from the request.
        """
