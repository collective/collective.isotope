# -*- coding: utf-8 -*-
"""Interfaces: control panel settings, browser layers &c."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
# from zope import schema


class ICollectiveIsotopeLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICollectiveIsotopeSettings(Interface):
    """this is an interface defining control panel settings

    Settings control options for the Isotope Library
    """
