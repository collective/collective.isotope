# -*- coding: utf-8 -*-
"""Vocabularies to use with collective.isotope"""
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary


FILTER_COLUMN_BLACKLIST = set([
    'total_comments',
    'Title',
    'commentators',
    'exclude_from_nav',
    'id',
    'cmf_uid',
    'Description',
    'listCreators',
    'is_folderish',
    'sync_uid',
    'getId',
    'ExpirationDate',
    'getRemoteUrl',
    'location',
    'EffectiveDate',
    'portal_type',
    'expires',
    'last_comment_date',
    'getObjSize',
    'UID',
    'effective',
    'getIcon',
    'created',
    'modified',
    'meta_type',
    'in_response_to',
])

SORT_COLUMN_BLACKLIST = set([
    'total_comments',
    'commentators',
    'exclude_from_nav',
    'id',
    'cmf_uid',
    'Description',
    'listCreators',
    'is_folderish',
    'sync_uid',
    'getId',
    'ExpirationDate',
    'review_state',
    'getRemoteUrl',
    'location',
    'portal_type',
    'expires',
    'last_comment_date',
    'UID',
    'effective',
    'Creator',
    'getIcon',
    'created',
    'modified',
    'meta_type',
    'in_response_to',
    'Subject'
])


class MetadataColumnVocabulary(object):
    """parameterized vocabulary providing items from catalog metadata columns"""

    def __init__(self, blacklist):
        self.blacklist = blacklist

    def __call__(self, context):
        portal_catalog = api.portal.get_tool('portal_catalog')
        column_name_set = set(portal_catalog.schema())
        possible = column_name_set - self.blacklist
        items = sorted([(name.decode('utf8'), name) for name in possible])
        return SimpleVocabulary.fromItems(items)

FilterColumnVocabularyFactory = MetadataColumnVocabulary(FILTER_COLUMN_BLACKLIST)
SortColumnVocabularyFactory = MetadataColumnVocabulary(SORT_COLUMN_BLACKLIST)


class RegistryFieldVocabulary(object):
    """parameterized vocabulary providing items from a field in the configuration registry"""

    def __init__(self, registry_key):
        self.registry_key = registry_key

    def __call__(self, context):
        registry = getUtility(IRegistry)
        values = registry.get(self.registry_key, [])
        terms = []
        for value in values:
            terms.append(SimpleVocabulary.createTerm(value, str(value)))
        return SimpleVocabulary(terms)


FiltersVocabularyFactory = RegistryFieldVocabulary(
    'collective.isotope.interfaces.ICollectiveIsotopeSettings.filter_whitelist'
)
SortsVocabularyFactory = RegistryFieldVocabulary(
    'collective.isotope.interfaces.ICollectiveIsotopeSettings.sorting_whitelist'
)
