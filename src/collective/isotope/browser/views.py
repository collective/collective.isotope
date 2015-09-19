# -*- coding: utf-8 -*-
"""Browser views"""
import json
# from plone import api
from plone.app.contenttypes.browser.collection import CollectionView
from plone.app.contenttypes.browser.folder import FolderView
from plone.registry.interfaces import IRegistry
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import getUtility

from ..interfaces import ICollectiveIsotopeSettings


_marker = object()


class IsotopeViewMixin(object):
    """shared browser view functionality for all isotope views"""

    @lazy_property
    def settings_dict(self):
        registry = getUtility(IRegistry)
        isotope_settings = registry.forInterface(ICollectiveIsotopeSettings)
        settings = {
            'itemSelector': '.isotope-item',
        }
        names = ICollectiveIsotopeSettings.names()
        for name in names:
            value = getattr(isotope_settings, name, _marker)
            if value and value is not _marker:
                settings.setdefault(name, value)
        return settings

    def options(self):
        options = self.settings_dict
        return json.dumps(options)

    def layout_class(self):
        klass = 'horizontal'
        if self.settings_dict.get('layoutMode') == 'vertical':
            klass = 'vertical'
        return klass


class IsotopeCollectionView(IsotopeViewMixin, CollectionView):

    def results(self, **kwargs):
        # disable batching
        kwargs['batch'] = False
        return super(IsotopeCollectionView, self).results(**kwargs)


class IsotopeFolderView(IsotopeViewMixin, FolderView):

    def results(self, **kwargs):
        # disable batching
        kwargs['batch'] = False
        return super(IsotopeFolderView, self).results(**kwargs)
