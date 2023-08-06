"""
Tests for models
"""
import uuid

import ddt
import pytest
from django.conf import settings
from django.contrib.sites.models import Site
from organizations.models import Organization

from tahoe_sites import api
from tahoe_sites.models import TahoeSite
from tahoe_sites.tests.fatories import UserFactory
from tahoe_sites.tests.test_models import DefaultsForTestsMixin
from tahoe_sites.tests.utils import create_organization_mapping


@ddt.ddt
class TestAPIHelpers(DefaultsForTestsMixin):
    """
    Tests for API helpers
    """
    def setUp(self):
        super().setUp()
        self.org1 = None
        self.org2 = None
        self.mapping = None
        self.user2 = None

    def _prepare_mapping_data(self):
        """
        mapping:
            default_org --> default_user
            Org1        --> default_user  -----> self.mapping points here
            Org1        --> user2
            Org2        --> user2
            Org3        --> None
        """
        self.org1 = self.create_organization(name='Org1', short_name='O1')
        create_organization_mapping(user=self.default_user, organization=self.default_org)
        self.mapping = create_organization_mapping(user=self.default_user, organization=self.org1)

        self.org2 = self.create_organization(name='Org2', short_name='O2')
        self.user2 = UserFactory.create()
        create_organization_mapping(user=self.user2, organization=self.org1)
        create_organization_mapping(user=self.user2, organization=self.org2)

        self.create_organization(name='Org3', short_name='O3')

        # We have four organizations
        assert Organization.objects.count() == 4

    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_get_organization_by_uuid_without_org(self):
        """
        Test get_organization_by_uuid helper when edx-organizations customization is off
        """
        assert api.get_organization_by_uuid(self.default_tahoe_site.site_uuid) == self.default_org

    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_get_uuid_by_organization_without_org(self):
        """
        Test get_uuid_by_organization helper when edx-organizations customization is off
        """
        assert api.get_uuid_by_organization(self.default_org) == self.default_tahoe_site.site_uuid

    @pytest.mark.skipif(not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is on')
    def test_get_organization_by_uuid_with_org(self):
        """
        Test get_organization_by_uuid helper when edx-organizations customization is on
        """
        assert api.get_organization_by_uuid(self.default_org.edx_uuid) == self.default_org

    @pytest.mark.skipif(not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is on')
    def test_get_uuid_by_organization_with_org(self):
        """
        Test get_uuid_by_organization helper when edx-organizations customization is on
        """
        assert api.get_uuid_by_organization(self.default_org) == self.default_org.edx_uuid

    def test_get_organizations_for_user_default(self):
        """
        Verify that get_active_organizations_for_user helper returns only related to active user
        """
        self._prepare_mapping_data()

        # default_user is mapped to 2 of them
        assert list(api.get_organizations_for_user(self.default_user)) == [self.default_org, self.org1]

        # user2 is mapped to two of them, one shared with default_user
        assert list(api.get_organizations_for_user(self.user2)) == [self.org1, self.org2]

        # records with inactive user will not be returned
        self.mapping.is_active = False
        self.mapping.save()
        assert list(api.get_organizations_for_user(self.default_user)) == [self.default_org]

    def test_get_organizations_for_user_with_inactive_users(self):
        """
        Verify that get_active_organizations_for_user helper can return all organization related to a user
        including organizations having that user deactivated
        """
        self._prepare_mapping_data()

        self.mapping.is_active = False
        self.mapping.save()
        assert list(api.get_organizations_for_user(self.default_user, with_inactive_users=True)) == [
            self.default_org,
            self.org1
        ]

    def test_get_organizations_for_user_without_admins(self):
        """
        Verify that get_active_organizations_for_user helper can return all organization related to a user
        excluding organizations having that user as an admin
        """
        self._prepare_mapping_data()

        self.mapping.is_admin = True
        self.mapping.save()
        assert list(api.get_organizations_for_user(self.default_user, without_admins=True)) == [self.default_org]

    def test_get_users_of_organization(self):
        """
        Verify that get_users_of_organization returns all active users related to an organization
        """
        self._prepare_mapping_data()

        # default_org is mapped to default_user
        assert list(api.get_users_of_organization(self.default_org)) == [self.default_user]

        # Org1 is mapped to two users
        assert list(api.get_users_of_organization(self.org1)) == [self.default_user, self.user2]

        # inactive users will not be returned
        self.mapping.is_active = False
        self.mapping.save()
        assert list(api.get_users_of_organization(self.org1)) == [self.user2]

    def test_get_users_of_organization_with_inactive_users(self):
        """
        Verify that get_users_of_organization helper can return all user related to an organization
        including deactivated users
        """
        self._prepare_mapping_data()

        self.mapping.is_active = False
        self.mapping.save()
        assert list(api.get_users_of_organization(self.org1, with_inactive_users=True)) == [
            self.default_user,
            self.user2
        ]

    def test_get_users_of_organization_without_admins(self):
        """
        Verify that get_users_of_organization helper can return all user related to an organization
        excluding admin users
        """
        self._prepare_mapping_data()

        self.mapping.is_admin = True
        self.mapping.save()
        assert list(api.get_users_of_organization(self.org1, without_admins=True)) == [self.user2]

    def test_is_active_admin_on_organization(self):
        """
        Verify that is_active_admin_on_organization helper returns True if the given user
        is an admin on the given organization
        """
        self._prepare_mapping_data()

        assert not api.is_active_admin_on_organization(user=self.default_user, organization=self.org1)

        self.mapping.is_admin = True
        self.mapping.save()
        assert api.is_active_admin_on_organization(user=self.default_user, organization=self.org1)

    @pytest.mark.skipif(not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is on')
    def test_create_tahoe_site_by_link_with_org(self):
        """
        Verify that create_tahoe_site_by_link creates a TahoeSite with the given organization and site
        when edx-organizations customization is on
        """
        org = self.create_organization('dummy', 'DO')
        site = self.create_django_site('dummy.org')
        count = TahoeSite.objects.count()
        assert org.sites.count() == 0

        tahoe_site = api.create_tahoe_site_by_link(organization=org, site=site)
        assert tahoe_site is None
        assert TahoeSite.objects.count() == count
        assert org.sites.count() == 1
        assert org.sites.first() == site

    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    def test_create_tahoe_site_by_link_without_org(self):
        """
        Verify that create_tahoe_site_by_link creates a TahoeSite with the given organization and site
        when edx-organizations customization is off
        """
        org = self.create_organization('dummy', 'DO')
        site = self.create_django_site('dummy.org')
        count = TahoeSite.objects.count()

        tahoe_site = api.create_tahoe_site_by_link(organization=org, site=site)
        assert TahoeSite.objects.count() == count + 1
        assert tahoe_site.organization == org
        assert tahoe_site.site == site

    @pytest.mark.skipif(not settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is on')
    @ddt.data(uuid.uuid4(), None)
    def test_create_tahoe_site_with_org(self, given_uuid):
        """
        Verify that create_tahoe_site creates a TahoeSite with the given organization/site information
        when edx-organizations customization is on
        """
        organization_count = Organization.objects.count()
        site_count = Site.objects.count()

        data = api.create_tahoe_site(domain='dummydomain.org', short_name='DDOMAIN', uuid=given_uuid)
        assert Organization.objects.count() == organization_count + 1
        assert Site.objects.count() == site_count + 1

        site = Site.objects.get(domain='dummydomain.org')
        organization = Organization.objects.get(short_name='DDOMAIN')
        self.assertDictEqual(data, {
            'site_uuid': given_uuid if given_uuid else organization.edx_uuid,
            'site': site,
            'organization': organization,
        })

        assert organization.sites.get() == site
        assert organization.name == 'DDOMAIN'
        assert organization.description == 'Organization of dummydomain.org (automatic)'

    @pytest.mark.skipif(settings.FEATURES['TAHOE_SITES_USE_ORGS_MODELS'],
                        reason='Runs only when TAHOE_SITES_USE_ORGS_MODELS is off')
    @ddt.data(uuid.uuid4(), None)
    def test_create_tahoe_site_without_org(self, given_uuid):
        """
        Verify that create_tahoe_site creates a TahoeSite with the given organization/site information
        when edx-organizations customization is off
        """
        tahoe_site_count = TahoeSite.objects.count()
        organization_count = Organization.objects.count()
        site_count = Site.objects.count()

        data = api.create_tahoe_site(domain='dummydomain.org', short_name='DDOMAIN', uuid=given_uuid)
        assert TahoeSite.objects.count() == tahoe_site_count + 1
        assert Organization.objects.count() == organization_count + 1
        assert Site.objects.count() == site_count + 1

        tahoe_site = TahoeSite.objects.get(organization__short_name='DDOMAIN')
        self.assertDictEqual(data, {
            'site_uuid': given_uuid if given_uuid else tahoe_site.site_uuid,
            'site': tahoe_site.site,
            'organization': tahoe_site.organization,
        })

        assert tahoe_site.organization.name == 'DDOMAIN'
        assert tahoe_site.organization.description == 'Organization of dummydomain.org (automatic)'

    def test_get_site_by_organization(self):
        """
        Verify that get_site_by_organization returns the related Organization of the given Site
        """
        assert api.get_site_by_organization(organization=self.default_org) == self.default_django_site

    def test_get_organization_by_site(self):
        """
        Verify that get_organization_by_site returns the related Site of the given Organization
        """
        assert api.get_organization_by_site(site=self.default_django_site) == self.default_org

    def test_get_organization_by_site_exception(self):
        """
        When a site is not linked with any organization; an Organization.DoesNotExist exception should
        be raised rather that TahoeSite.DoesNotExist
        """
        dummy_site = Site.objects.create(domain='dummy.org')
        with self.assertRaisesMessage(
            expected_exception=Organization.DoesNotExist,
            expected_message='Organization matching query does not exist'
        ):
            api.get_organization_by_site(site=dummy_site)

    def test_get_site_by_uuid(self):
        """
        Verify that get_site_by_uuid returns the related Site of the given UUID
        """
        assert api.get_site_by_uuid(
            site_uuid=api.get_uuid_by_organization(self.default_org)
        ) == self.default_django_site

    def test_get_uuid_by_site(self):
        """
        Verify that get_uuid_by_site returns the related UUID of the given Site
        """
        assert api.get_uuid_by_site(site=self.default_django_site) == api.get_uuid_by_organization(self.default_org)
