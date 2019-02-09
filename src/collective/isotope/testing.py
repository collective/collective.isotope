# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.isotope


class CollectiveIsotopeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.isotope)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.isotope:default')


COLLECTIVE_ISOTOPE_FIXTURE = CollectiveIsotopeLayer()


COLLECTIVE_ISOTOPE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_ISOTOPE_FIXTURE,),
    name='CollectiveIsotopeLayer:IntegrationTesting',
)


COLLECTIVE_ISOTOPE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_ISOTOPE_FIXTURE,),
    name='CollectiveIsotopeLayer:FunctionalTesting',
)


COLLECTIVE_ISOTOPE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_ISOTOPE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveIsotopeLayer:AcceptanceTesting',
)
