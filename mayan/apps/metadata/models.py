from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import Document, DocumentType

from .managers import MetadataSetManager, MetadataTypeManager


class MetadataType(models.Model):
    """
    Define a type of metadata
    """
    name = models.CharField(unique=True, max_length=48, verbose_name=_(u'name'), help_text=_(u'Do not use python reserved words, or spaces.'))
    title = models.CharField(max_length=48, verbose_name=_(u'title'), blank=True, null=True)
    default = models.CharField(max_length=128, blank=True, null=True,
        verbose_name=_(u'default'),
        help_text=_(u'Enter a string to be evaluated.'))
    # TODO: Add enable_lookup boolean to allow users to switch the lookup on and
    # off without losing the lookup expression
    lookup = models.TextField(blank=True, null=True,
        verbose_name=_(u'lookup'),
        help_text=_(u'Enter a string to be evaluated that returns an iterable.'))
    # TODO: Add datatype choice: Date, Time, String, Number
    # TODO: Find a different way to let users know what models and functions are
    # available now that we removed these from the help_text
    objects = MetadataTypeManager()

    def __unicode__(self):
        return self.title if self.title else self.name

    def natural_key(self):
        return (self.name,)

    class Meta:
        ordering = ('title',)
        verbose_name = _(u'metadata type')
        verbose_name_plural = _(u'metadata types')


class MetadataSet(models.Model):
    """
    Define a group of metadata types
    """
    title = models.CharField(max_length=48, verbose_name=_(u'title'), unique=True)

    objects = MetadataSetManager()

    def __unicode__(self):
        return self.title

    def natural_key(self):
        return (self.title,)

    class Meta:
        ordering = ('title',)
        verbose_name = _(u'metadata set')
        verbose_name_plural = _(u'metadata set')


class MetadataSetItem(models.Model):
    """
    Define the set of metadata that relates to a set or group of
    metadata fields
    """
    # TODO: is the metadata set model really necessary?
    metadata_set = models.ForeignKey(MetadataSet, verbose_name=_(u'metadata set'))
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'metadata type'))

    def __unicode__(self):
        return unicode(self.metadata_type)

    class Meta:
        verbose_name = _(u'metadata set item')
        verbose_name_plural = _(u'metadata set items')


class DocumentMetadata(models.Model):
    """
    Link a document to a specific instance of a metadata type with it's
    current value
    """
    document = models.ForeignKey(Document, verbose_name=_(u'document'), related_name='metadata')
    metadata_type = models.ForeignKey(MetadataType, verbose_name=_(u'type'))
    value = models.CharField(max_length=255, blank=True, verbose_name=_(u'value'), db_index=True)

    def __unicode__(self):
        return unicode(self.metadata_type)

    class Meta:
        verbose_name = _(u'document metadata')
        verbose_name_plural = _(u'document metadata')


class DocumentTypeDefaults(models.Model):
    """
    Default preselected metadata types and metadata set per document
    type
    """
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    default_metadata_sets = models.ManyToManyField(MetadataSet, blank=True, verbose_name=_(u'default metadata sets'))
    default_metadata = models.ManyToManyField(MetadataType, blank=True, verbose_name=_(u'default metadata'))

    def __unicode__(self):
        return unicode(self.document_type)

    class Meta:
        verbose_name = _(u'document type defaults')
        verbose_name_plural = _(u'document types defaults')
