# -*- coding: utf-8 -*-
"""Interfaces: control panel settings, browser layers &c."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope import schema

from collective.isotope import _


class ICollectiveIsotopeLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICollectiveIsotopeFilterSettings(Interface):
    """Settings to control filtering options"""
    filter_whitelist = schema.Set(
        title=_(u'Filter Whitelist'),
        description=_(u'Select the list of stored values by which items may '
                      u'be filtered. Individual views will configure one or '
                      u'more filters from this list'),
        value_type=schema.Choice(
            vocabulary='collective.isotope.vocabularies.filter_columns',
        )
    )
    sorting_whitelist = schema.Set(
        title=_(u'Sorting Whitelist'),
        description=_(u'Select the list of stored values by which items may '
                      u'be sorted. Individual views will configure one or '
                      u'more sortings from this list'),
        value_type=schema.Choice(
            vocabulary='collective.isotope.vocabularies.sort_columns',
        )
    )


class ICollectiveIsotopeLayoutSettings(Interface):
    """Settings for the options that control the javascript Isotope library
    """
    layoutMode = schema.Choice(
        title=_(u'Layout Mode'),
        description=_(u'Select the default layout mode to be used on all '
                      u'isotope views throughout your website'),
        values=[u'masonry', u'fitRows', u'vertical'],
        default=u'masonry'
    )

    percentPosition = schema.Bool(
        title=_(u'Use percentPosition'),
        description=_(u'Set the horizontal position of items by percent '
                      u'rather than pixel size. This works best with items '
                      u'that are sized by percentage. On by default'),
        default=True
    )


class ICollectiveIsotopeSettings(
    ICollectiveIsotopeLayoutSettings, ICollectiveIsotopeFilterSettings
):
    """Aggregated settings for the Isotope control panel"""


class ICollectiveIsotopeViewSettings(Interface):
    """Settings for configuration of individual views"""
    filter = schema.List(
        title=_(u'Filtering'),
        description=_(u'Select the ttributes on which users will be able to '
                      u'filter the items listed in this view. If no values '
                      u'are selected, user filtering will be disabled'),
        required=False,
        value_type=schema.Choice(
            vocabulary='collective.isotope.vocabularies.available_filters',
        )
    )

    sort = schema.List(
        title=_(u'Sorting'),
        description=_(u'Select the attributes on which users will be able to '
                      u'sort the items listed in this view. If no value is '
                      u'selected, user sorting will be disabled.'),
        required=False,
        value_type=schema.Choice(
            vocabulary='collective.isotope.vocabularies.available_sorts'
        )
    )
