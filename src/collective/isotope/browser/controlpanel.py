# -*- coding: utf-8 -*-
from ..interfaces import ICollectiveIsotopeSettings
from collective.isotope import _
from collective.z3cform.datagridfield import DataGridFieldFactory
from plone.app.registry.browser import controlpanel


class IsotopeSettingsControlpanelForm(controlpanel.RegistryEditForm):

    schema = ICollectiveIsotopeSettings
    label = _(u'Isotope View Settings')
    description = _(
        u'Site-wide settings to control the Isotope View for '
        u'collections and folders'
    )

    def updateFields(self):
        super(IsotopeSettingsControlpanelForm, self).updateFields()
        for field in ['available_filters', 'available_sorts']:
            self.fields[field].widgetFactory = DataGridFieldFactory
            self.fields[field].allow_insert = True


class IsotopeSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = IsotopeSettingsControlpanelForm
