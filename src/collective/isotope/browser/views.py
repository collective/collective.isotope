# -*- coding: utf-8 -*-
"""Browser views"""
import json
# from plone import api
from plone.app.contenttypes.browser.collection import CollectionView
from plone.app.contenttypes.browser.folder import FolderView
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.registry.interfaces import IRegistry
from plone.z3cform.layout import wrap_form
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import form, field, button
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.cachedescriptors.method import cachedIn
from zope.component import getUtility, queryUtility

from ..interfaces import ICollectiveIsotopeSettings
from ..interfaces import ICollectiveIsotopeLayoutSettings
from ..interfaces import ICollectiveIsotopeViewSettings
from collective.isotope import _


ISOTOPE_CONFIGURATION_KEY = 'collective.isotope.configuration'
_marker = object()


class IsotopeViewConfigurationForm(form.Form):
    fields = field.Fields(ICollectiveIsotopeViewSettings)
    label = _(u"Isotope View Configuration")
    description = _(u"Configuration of layout, filters, and sorting for this view")

    def getContent(self):
        annotations = IAnnotations(self.context)
        current_config = annotations.get(ISOTOPE_CONFIGURATION_KEY, {})
        return current_config

    @button.buttonAndHandler(_(u'Save Configuration'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        assert IAttributeAnnotatable.providedBy(self.context)
        annotations = IAnnotations(self.context)
        annotations[ISOTOPE_CONFIGURATION_KEY] = data

        self.request.response.redirect(self.context.absolute_url())
        messages = IStatusMessage(self.request)
        messages.add(_(u"Your configuration has been saved"), type=u"info")

IsotopeConfigurationView = wrap_form(IsotopeViewConfigurationForm)


def call_or_attr(obj, attrname):
    attr = getattr(obj, attrname, None)
    if callable(attr):
        attr = attr()
    return attr


class IsotopeViewMixin(object):
    """shared browser view functionality for all isotope views"""

    @lazy_property
    def settings_dict(self):
        registry = getUtility(IRegistry)
        isotope_settings = registry.forInterface(ICollectiveIsotopeSettings)
        settings = {
            'itemSelector': '.isotope-item',
        }
        names = ICollectiveIsotopeLayoutSettings.names()
        for name in names:
            value = getattr(isotope_settings, name, _marker)
            if value is not _marker:
                settings.setdefault(name, value)
        return settings

    @lazy_property
    def configuration(self):
        annotations = IAnnotations(self.context)
        return annotations.get(ISOTOPE_CONFIGURATION_KEY, {})

    @lazy_property
    def normalizer(self):
        return queryUtility(IIDNormalizer)

    def options(self):
        """return the layout options as configured for this site/view"""
        options = self.settings_dict
        return json.dumps(options)

    def filters(self):
        """return the list of filters to use in this view

        This method is dependent on their being a `results` method on the view
        class to which this mixin is added.
        """
        filters = self.configuration.get('filter', [])
        results = {}
        for filter in filters:
            results[filter] = set([call_or_attr(r, filter) for r in self.results()])
        return results

    def filters_for_item(self, result):
        filt_vals = []
        for filter in self.filters():
            val = call_or_attr(result, filter)
            if val:
                filt_vals.append(self.normalizer.normalize(val))
        return ' '.join(filt_vals)

    def sorts(self):
        """return the list of sorts to use in this view"""
        return self.configuration.get('sort', [])

    def layout_class(self):
        klass = 'horizontal'
        if self.settings_dict.get('layoutMode') == 'vertical':
            klass = 'vertical'
        return klass


class IsotopeCollectionView(IsotopeViewMixin, CollectionView):
    """View class for p.a.contenttypes collections"""

    @cachedIn('_v_cached_results')
    def results(self, **kwargs):
        # disable batching
        kwargs['batch'] = False
        return super(IsotopeCollectionView, self).results(**kwargs)


class IsotopeFolderView(IsotopeViewMixin, FolderView):
    """View class for p.a.contenttypes Folders"""

    @cachedIn('_v_cached_results')
    def results(self, **kwargs):
        # disable batching
        kwargs['batch'] = False
        return super(IsotopeFolderView, self).results(**kwargs)
