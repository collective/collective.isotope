# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.isotope.testing import (
    COLLECTIVE_ISOTOPE_INTEGRATION_TESTING,  # noqa
)
from Products.CMFPlone.utils import get_installer
try:
    import unittest
except ImportError:
    import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that collective.isotope is properly installed."""

    layer = COLLECTIVE_ISOTOPE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if collective.isotope is installed with portal_quickinstaller."""
        self.assertTrue(
            self.installer.is_product_installed('collective.isotope')
        )

    def test_browserlayer(self):
        """Test that ICollectiveIsotopeLayer is registered."""
        from collective.isotope.interfaces import ICollectiveIsotopeLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveIsotopeLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_ISOTOPE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)
        self.installer.uninstall_product('collective.isotope')

    def test_product_uninstalled(self):
        """Test if collective.isotope is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed('collective.isotope')
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveIsotopeLayer is removed."""
        from collective.isotope.interfaces import ICollectiveIsotopeLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveIsotopeLayer, utils.registered_layers())
