# -*- coding: utf-8 -*-
"""Interfaces: control panel settings, browser layers &c."""
from collective.isotope import _
from collective.z3cform.datagridfield.interfaces import AttributeNotFoundError
from collective.z3cform.datagridfield.registry import DictRow
from plone.registry import field
from z3c.form.interfaces import NO_VALUE
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveIsotopeLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IValueConverter(Interface):
    """Utility registration interface for Value Converters

    A value converter is responsible for converting the value stored in a
    metadata column into a human readable value suitable for presentation in a
    UI.
    """

    def convert(value):
        """Convert a give value into a human readable value

        This method must return a utf-8 encoded byte string
        """


# A DictRow is an IDict for import/export purposes
@implementer(schema.interfaces.IDict)
class ImportableTextDictRow(DictRow, schema.MinMaxLen):

    # We treat all values as text for simplicity of import/export.
    # Unfortunately, non-text values will result in duplicates when
    # purge="False"
    key_type = value_type = schema.TextLine()

    def _validate(self, value):
        if value is NO_VALUE:
            return
        errors = []
        for field_name, field_ in schema.getFields(self.schema).items():
            if field_name not in value and field_.required:
                errors.append(AttributeNotFoundError(field_name, self.schema))
            ftype = getattr(field_, '_type', None)
            fvalue = value.get(field_name, NO_VALUE)
            if isinstance(ftype, tuple):
                ftype = ftype[0]
            # Perform a naive type coercion
            if (
                fvalue is not NO_VALUE and
                ftype is not None and
                not isinstance(fvalue, ftype)
            ):
                if ftype is bool and fvalue.lower() == 'false':
                    fvalue = False
                try:
                    value[field_name] = ftype(fvalue)
                except (ValueError, TypeError):
                    pass
            if fvalue is not NO_VALUE:
                field_.validate(fvalue)

        if errors:
            raise schema.interfaces.WrongContainedType(errors, self.__name__)


class IFilterSchema(Interface):
    column_name = field.Choice(
        title=_(u'Column Name'),
        description=_(u'Enter the name of a catalog metadata column'),
        vocabulary='collective.isotope.vocabularies.friendly_columns',
        required=False,
        missing_value=u'',
    )
    label = field.TextLine(
        title=_(u'Label'),
        description=_(
            u'If desired, enter the human-readable label for this column'
        ),
        required=False,
        missing_value=u'',
    )


class ICollectiveIsotopeFilterSettings(Interface):
    """Settings to control filtering options"""

    available_filters = schema.List(
        title=_(u'Available Filters'),
        description=_(
            u'List the filters that will be available for Istotope '
            u'views throughout your site.'
        ),
        value_type=ImportableTextDictRow(
            title=_(u'Filter'), schema=IFilterSchema
        ),
    )

    available_sorts = schema.List(
        title=_(u'Available Sorts'),
        description=_(
            u'List the sortable attributes that will be available '
            u'for Istotope views throughout your site.'
        ),
        value_type=ImportableTextDictRow(
            title=_(u'Sort'), schema=IFilterSchema
        ),
    )


class ICollectiveIsotopeLayoutSettings(Interface):
    """Settings for the options that control the javascript Isotope library
    """

    layoutMode = schema.Choice(
        title=_(u'Layout Mode'),
        description=_(
            u'Select the default layout mode to be used on all '
            u'isotope views throughout your website'
        ),
        values=[u'masonry', u'fitRows', u'vertical'],
        default=u'masonry',
    )

    percentPosition = schema.Bool(
        title=_(u'Use percentPosition'),
        description=_(
            u'Set the horizontal position of items by percent '
            u'rather than pixel size. This works best with items '
            u'that are sized by percentage. On by default'
        ),
        default=True,
    )


class ICollectiveIsotopeSettings(
    ICollectiveIsotopeLayoutSettings, ICollectiveIsotopeFilterSettings
):
    """Aggregated settings for the Isotope control panel"""


class ICollectiveIsotopeViewSettings(Interface):
    """Settings for configuration of individual views"""

    filter = schema.List(
        title=_(u'Filtering'),
        description=_(
            u'Select the ttributes on which users will be able to '
            u'filter the items listed in this view. If no values '
            u'are selected, user filtering will be disabled'
        ),
        required=False,
        value_type=schema.Choice(
            vocabulary='collective.isotope.vocabularies.available_filters'
        ),
    )

    sort = schema.List(
        title=_(u'Sorting'),
        description=_(
            u'Select the attributes on which users will be able to '
            u'sort the items listed in this view. If no value is '
            u'selected, user sorting will be disabled.'
        ),
        required=False,
        value_type=schema.Choice(
            vocabulary='collective.isotope.vocabularies.available_sorts'
        ),
    )
