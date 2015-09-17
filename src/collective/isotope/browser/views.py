# -*- coding: utf-8 -*-
"""Browser views"""
import json
from plone.app.contenttypes.browser.collection import CollectionView


class IsotopeCollectionView(CollectionView):

    def results(self, **kwargs):
        # disable batching
        kwargs['batch'] = False
        return super(IsotopeCollectionView, self).results(**kwargs)

    def options(self):
        options = {
            'itemSelector': '.item',
            'layoutMode': 'fitRows',
        }
        return json.dumps(options)
