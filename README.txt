redomino.keywordalias
=====================

This product aims to let keyword managers to add one or more keyword aliases and different versions depending on the user language.
It may help you managing multilingual websites.

It provides:

* a customized keywords viewlet

* a keyword alias configuration panel

* a couple of views that let you personalize your 'search' and 'search_form' views.
  Note well: you have to customize your search and search_form manually! These two templates may depend on the Plone version you are using

Tested on Plone 4.1.5 and Plone 4.2.

How it works?
-------------
This product provides a customized keywords viewlet that shows keyword aliases instead of standard keywords depending on a configuration panel.
The keyword alias configuration panel let you assign keyword aliases for each keyword indexed in the plone's catalog and for each enabled language.

The keyword alias configuration panel stores a dictionary similar to the following one:

    {
     'wood': ['Wood',],    # the fallback version for each language
     'wood|en': ['Wood',],
     'wood|it': ['Legno', 'Materiale legnoso'],
    }

The registry accepts a list: will be used the first item as a keyword translation, otherwise the default one or the plain keyword itself. The other list values
could be used by third party packages as aliases or keyword synonims.

If you want you may customize the 'search' and 'search_form' views, see next section-

Customize the search and search_form views
------------------------------------------

How to customize the 'search' view:

    <tal:replace replace="structure context/@@multiselectkeywords" />


How to customize the 'search_form' view (where result may be an object or a catalog brain):

    <tal:replace replace="structure result/@@filedunder" />

Similar products
----------------

See http://pypi.python.org/pypi/archetypes.linguakeywordwidget written by JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>.

This package achieve the same goal but in a different way. With keyword alias
your keywords are translated in backoffice. With linguakeywords you have
just different keywords.


Authors
-------

* Davide Moro <davide.moro@redomino.com>, idea and main author

