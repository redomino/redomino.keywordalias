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

from zope.interface import implements

from Products.Five import BrowserView

from redomino.keywordalias.utils import get_storage
from redomino.keywordalias.browser.interfaces import IKeywordTranslator

class KeywordTranslator(BrowserView):
    """ This view let you get the translated version of a keyword for
        a given language, if available with this order:

        1 - the keyword lang version
        2 - the default alias
        3 - the keyword itself

        >>> class DummyKeywordTranslator(KeywordTranslator):
        ...     def _get_storage(self):
        ...         return {
        ...                 'wood': ['Wood',],    # the fallback version for each language
        ...                 'wood|en': ['Wood',],
        ...                 'wood|it': ['Legno', 'Materiale legnoso'],
        ...                }

        >>> view = DummyKeywordTranslator(None, {'LANGUAGE':'it'})
        >>> view.translate('wood')
        'Legno'

        >>> view = DummyKeywordTranslator(None, {'LANGUAGE':'it', 'keyword':'wood'})
        >>> view()
        'Legno'

        >>> view = DummyKeywordTranslator(None, {'LANGUAGE':'en'})
        >>> view.translate('wood')
        'Wood'

        >>> view = DummyKeywordTranslator(None, {})
        >>> view.translate('wood')
        'Wood'

    """
    implements(IKeywordTranslator)

    def __call__(self):
        request = self.request
        keyword = request.get('keyword')
        if keyword:
            return self.translate(keyword)

    def translate(self, keyword=None):
        request = self.request
        keyword = keyword or request.get('keyword')
        language = request.get('LANGUAGE')
        keyword_storage = self._get_storage()
        alias = keyword_storage.get('%s|%s' % (keyword, language))
        if not alias:
            alias = keyword_storage.get(keyword) or [keyword]
        return alias[0]

    def _get_storage(self):
        keyword_settings = get_storage()
        keyword_storage = keyword_settings.keyword_storage
        return keyword_storage


