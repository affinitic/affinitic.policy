# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from affinitic.policy.testing import AFFINITIC_POLICY_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that affinitic.policy is properly installed."""

    layer = AFFINITIC_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if affinitic.policy is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'affinitic.policy'))

    def test_browserlayer(self):
        """Test that IAffiniticPolicyLayer is registered."""
        from affinitic.policy.interfaces import (
            IAffiniticPolicyLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IAffiniticPolicyLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = AFFINITIC_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['affinitic.policy'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if affinitic.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'affinitic.policy'))

    def test_browserlayer_removed(self):
        """Test that IAffiniticPolicyLayer is removed."""
        from affinitic.policy.interfaces import \
            IAffiniticPolicyLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IAffiniticPolicyLayer,
            utils.registered_layers())
