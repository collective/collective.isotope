# -*- coding: utf-8 -*-
"""Vocabularies to use with collective.isotope"""
import six
from binascii import b2a_qp
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary


COLUMN_BLACKLIST = set(
    [
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
        'getRemoteUrl',
        'location',
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
    ]
)


class MetadataColumnVocabulary(object):
    """Build terms from the list of catalog metadata columns

    The vocabulary can optionally take a 'blacklist' which will filter
    the terms available.
    """

    def __init__(self, blacklist=None):
        if blacklist is None:
            blacklist = set([])
        self.blacklist = blacklist

    def __call__(self, context):
        portal_catalog = api.portal.get_tool('portal_catalog')
        column_name_set = set(portal_catalog.schema())
        terms = []
        possible = column_name_set - self.blacklist
        items = sorted(list(possible))
        for item in items:
            if six.PY2 and isinstance(item, six.binary_type):
                item = item.decode('utf8')
            terms.append(SimpleVocabulary.createTerm(
                item, b2a_qp(item.encode('utf-8')), item
            ))

        return SimpleVocabulary(terms)


FriendlyColumnVocabularyFactory = MetadataColumnVocabulary(COLUMN_BLACKLIST)


class FilterFieldVocabulary(object):
    """Build terms from a datagrid field providing the filter schema"""

    def __init__(self, registry_key):
        self.registry_key = registry_key

    def __call__(self, context):
        registry = getUtility(IRegistry)
        rows = registry.get(self.registry_key, [])
        terms = []
        for row in rows:
            value = row.get('column_name')
            title = row.get('label')
            if not title:
                title = value
            if six.PY2:
                if isinstance(value, six.binary_type):
                    value = value.decode('utf8')
                if isinstance(title, six.binary_type):
                    title = title.decode('utf8')
            terms.append(
                SimpleVocabulary.createTerm(
                    value, b2a_qp(value.encode('utf-8')), title
                )
            )
        return SimpleVocabulary(terms)


FiltersVocabularyFactory = FilterFieldVocabulary(
    'collective.isotope.interfaces.ICollectiveIsotopeSettings.available_filters'
)
SortsVocabularyFactory = FilterFieldVocabulary(
    'collective.isotope.interfaces.ICollectiveIsotopeSettings.available_sorts'
)
