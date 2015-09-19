# -*- coding: utf-8 -*-
"""Browser views"""
import json
from plone.app.contenttypes.browser.collection import CollectionView
from plone.app.contenttypes.browser.folder import FolderView
from plone.registry.interfaces import IRegistry
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import getUtility


class IsotopeCollectionView(CollectionView):

    def results(self, **kwargs):
        # disable batching
        kwargs['batch'] = False
        return super(IsotopeCollectionView, self).results(**kwargs)


class IsotopeFolderView(IsotopeViewMixin, FolderView):

    def results(self, **kwargs):
        # disable batching
        kwargs['batch'] = False
        return super(IsotopeFolderView, self).results(**kwargs)
