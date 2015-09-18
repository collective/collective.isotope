from plone.app.registry.browser import controlpanel

from ..interfaces import ICollectiveIsotopeSettings


class IsotopeSettingsControlpanelForm(controlpanel.RegistryEditForm):

    schema = ICollectiveIsotopeSettings
    label = u'Isotope View Settings'
    description = u"""Site-wide settings to control the Isotope View for collections and folders"""


class IsotopeSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = IsotopeSettingsControlpanelForm
