# -*- coding: utf-8 -*-
"""Interfaces: control panel settings, browser layers &c."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope import schema

from collective.isotope import _


class ICollectiveIsotopeLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICollectiveIsotopeSettings(Interface):
    """this is an interface defining control panel settings

    Settings control options for the Isotope Library
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
