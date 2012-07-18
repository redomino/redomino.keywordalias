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

from zope import interface
from zope.component import getMultiAdapter

from z3c.form import field
from z3c.form.interfaces import DISPLAY_MODE

from plone.memoize.view import memoize
from plone.z3cform.crud import crud
from plone.app.z3cform import layout
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from Products.CMFCore.utils import getToolByName

from redomino.keywordalias import keywordaliasMessageFactory as _
from redomino.keywordalias.interfaces import IKeywordAlias
from redomino.keywordalias.utils import get_storage
from redomino.keywordalias.browser.widgets import KeywordLangKey


class KeywordAlias(object):
    """ Dummy object used for keyword settings storage in crud form """
    interface.implements(IKeywordAlias)

    def __init__(self, keyword, keywords=[]):
        self._keyword = keyword
        self._keywords = keywords

    @apply
    def keyword():
        def getter(self):
            # Example: u'david\xe8'
            return self._keyword
        def setter(self, value):
            pass
        return property(getter, setter)

    @apply
    def keywords():
        def getter(self):
            # Example: [u'david\xe8']
            keyword = self.keyword
            keyword_settings = get_storage() 
            keyword_storage = keyword_settings.keyword_storage
            return keyword_storage[keyword]
        def setter(self, value):
            keyword_settings = get_storage() 
            keyword_storage = keyword_settings.keyword_storage
            keyword_storage[self.keyword] = value or []
            keyword_settings.keyword_storage = keyword_storage
        return property(getter, setter)

    def __repr__(self):
        return "<KeywordAlias %s with keywords=%s>" % (self.keyword, str(self.keywords))

class KeywordAliasEditSubForm(crud.EditSubForm):

    def updateWidgets(self):
        super(KeywordAliasEditSubForm, self).updateWidgets()
        name = self.widgets.items()[0][1].name
        for widget in self.widgets.values():
            name = widget.name
            widget_id = widget.id
            value = widget.value
            widget.__dict__['name'] = name.decode('utf-8')
            widget.__dict__['id'] = widget_id.decode('utf-8')
            if isinstance(value, tuple):
                results = []
                for item in value:
                    results.append(item.decode('utf-8'))
                results = tuple(results)
                widget.__dict__['value'] = results #value.decode('utf-8')

#    def _select_field(self):
#        select_field = field.Field(
#               schema.Bool(__name__='select',
#               required=False,
#               title=_(u'select')))
#        from z3c.form.interfaces import INPUT_MODE
#        from plone.z3cform.widget import singlecheckboxwidget_factory
#        select_field.widgetFactory[INPUT_MODE] = singlecheckboxwidget_factory
#        return select_field

 
class KeywordAliasEditForm(crud.EditForm):
    """ Crud edit form """
    label = _(u'keyword_management_edit_label', default=u'Edit keyword translations')

    #exposes the edit sub form for your own derivatives
    editsubform_factory = KeywordAliasEditSubForm



    def updateActions(self):
        # We don't need a delete button
        self.handle_delete.button.condition = lambda form: False
        # label change for apply changes button
        self.handle_edit.button.title = _(u'edit_apply_changes', default=u'Save')
        super(KeywordAliasEditForm, self).updateActions()


class KeywordAliasForm(crud.CrudForm):
    """ Crud control panel

        >>> class DummyKeywordSettings(object):
        ...     def __init__(self, keyword_storage):
        ...         self.keyword_storage = keyword_storage
        >>> keyword_settings = DummyKeywordSettings({})

        >>> class DummyKeywordAliasForm(KeywordAliasForm):
        ...     def __init__(self, context, request):
        ...         self.context= context
        ...         self.request = request
        ...     @property
        ...     def _keyword_settings(self):
        ...         return keyword_settings
        ...     @property
        ...     def _unique_keyword_values(self):
        ...         return ['wood']
        ...     @property
        ...     def _portal_languages(self):
        ...         return ['it', 'en']

        >>> view = DummyKeywordAliasForm(None, None)
        >>> len(view.get_items())
        0

        After update storage...
        >>> view.update_storage()
        >>> len(view.get_items())
        3

        Ok, the storage initialization works fine...
    """
    label = _(u'keyword_management_label', default=u'Manage keywords')
    description = _(u'keyword_management_form', default=u'Manage keywords form')

    update_schema = field.Fields(IKeywordAlias).select(*['keywords'])
    view_schema = field.Fields(IKeywordAlias).select(*['keyword'])
    view_schema['keyword'].widgetFactory[DISPLAY_MODE] = KeywordLangKey
    addform_factory = crud.NullForm
    editform_factory = KeywordAliasEditForm
    batch_size = 25

    @memoize
    def default_charset(self):
        context = self.getContent()
        return getMultiAdapter((context, self.request), name=u'plone').site_encoding()

    @property
    def _keyword_settings(self):
        """ Return the keywor settings storage """
        keyword_settings = get_storage() 
        return keyword_settings

    @property
    def _unique_keyword_values(self):
        """ Return the indexed keywords available on portal catalog """
        context = self.getContent()
        catalog = getMultiAdapter((context, self.request), name=u'plone_tools').catalog()
        return catalog.uniqueValuesFor('Subject')

    @property
    def _portal_languages(self):
        """ Return the list of language codes available """
        context = self.getContent()
        portal_languages = getToolByName(context, 'portal_languages')
        return portal_languages.getSupportedLanguages()

    def _keyword_split(self, keyword):
        """ We store in the keyword storage something like this:
                {
                 'keyword' : [],
                 'keyword|lang1': [],
                 'keyword|lang2': [],
                }

            For a given key we return a tuple with the base keyword and the lang, example:
                'keyword|lang1' -> ('keyword', 'lang1')
            or
                'keyword' -> ('keyword', '')
        """
        separator_index = keyword.rfind('|')
        lang = ''
        if separator_index != -1:
            keyword_base = keyword[0:separator_index]
            lang = keyword[separator_index+1:]
        else:
            keyword_base = keyword
        return keyword_base, lang

    def get_items(self):
        """ Standard crud's get_items. We return just existing indexed keywords.
            Old non-existing keywords settings are not shown (but they still exist
            on the storage)
        """
        keyword_settings = self._keyword_settings
        keyword_storage = keyword_settings.keyword_storage
        items = keyword_storage.items()
        catalog_entries = self._unique_keyword_values
        languages = self._portal_languages
        charset = self.default_charset()

        results = []

        for item in items:
            keyword = item[0]
            if keyword.encode(charset) in catalog_entries:
                results.append(item)
            else:
                splitted_keyword = self._keyword_split(keyword)
                lang = splitted_keyword[1]
                if lang and lang in languages and splitted_keyword[0].encode(charset) in catalog_entries:
                    results.append(item)
        # Example: return [(u'david\xe8'.encode('utf-8'), KeywordAlias(u'david\xe8', [u'david\xe8']))]
        return sorted([(item[0].encode(charset), KeywordAlias(item[0], item[1])) for item in results], key=lambda x: x[0])

    def add(self, data):
        """ It is not possible to add new keywords, they are automatically added
            by the 'update' method
        """
        keyword_settings = self._keyword_settings
        keyword_storage = keyword_settings.keyword_storage
        charset = self.default_charset()

        key = unicode(data['keyword'], charset)
        value = [unicode(item, charset) for item in data['keywords']]
        keyword_storage[key] = value
        keyword_settings.keyword_storage = keyword_storage

        return KeywordAlias(key, value)

    def remove(self, (id, item)):
        """ This method is working but it shouldn't be possible to delete
            keyword settings
        """
        keyword_storage = self._keyword_settings
        del keyword_storage[id]

    def update_storage(self):
        """ This methos performs an initialization based on what is currently
            indexed on the portal_catalog
        """
        keyword_settings = self._keyword_settings
        keyword_storage = keyword_settings.keyword_storage
        storage_entries = keyword_storage.keys()
        catalog_entries = self._unique_keyword_values
        languages = self._portal_languages
        charset = self.default_charset()

        for item in catalog_entries:
            if item.decode(charset) not in storage_entries:
                self.add(dict(keyword=item, keywords=[]))
            for lang in languages:
                lang_item = "%s|%s" % (item, lang)
                if lang_item.decode(charset) not in storage_entries:
                    self.add(dict(keyword=lang_item, keywords=[]))

    def update(self):
        """ This methos performs an initialization based on what is currently
            indexed on the portal_catalog
        """
        self.update_storage()
        super(KeywordAliasForm, self).update()

    def link(self, item, field):
        """Return a URL for this item's field or None.
        """
        content = self.getContent()
        portal_url = getMultiAdapter((content, self.request), name=u'plone_portal_state').portal_url()
        keyword = self._keyword_split(item.keyword)[0]
        return "%s/search?Subject=%s" % (portal_url, keyword)

KeywordAliasView = layout.wrap_form(KeywordAliasForm, ControlPanelFormWrapper)
