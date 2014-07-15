# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import simple_audit
from util.models import BaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.encrypted import EncryptedCharField



class CloudStackOffering(BaseModel):
    serviceofferingid = models.CharField(verbose_name=_("Offering ID"),
                                         max_length=100,
                                         help_text="Cloud Stack Offering ID")
    name = models.CharField(verbose_name=_("Name"),
                                         max_length=100,
                                         help_text="Cloud Stack Offering name")
    weaker = models.BooleanField(verbose_name=_("Is the weaker offering"), default=False)


class CloudStackBundle(BaseModel):
        zoneid = models.CharField(verbose_name=_("Zone ID"),
                                                 max_length=100,
                                                 help_text="Cloud Stack Template ID")
        templateid = models.CharField(verbose_name=_("Template ID"),
                                                 max_length=100,
                                                 help_text="Cloud Stack Template ID")
        networkid = models.CharField(verbose_name=_("Network ID"),
                                 max_length=100,
                                 help_text="Cloud Stack Network ID")
        name = models.CharField(verbose_name=_("Name"),
                                                 max_length=100,
                                                 help_text="Cloud Stack Zone Name")


class HostAttr(BaseModel):

    vm_id = models.CharField(verbose_name=_("Cloud Stack vm id"), max_length=255, blank=True, null=True)
    vm_user = models.CharField(verbose_name=_("Cloud Stack virtual machine user"), max_length=255, blank=True, null=True)
    vm_password = EncryptedCharField(verbose_name=_("Cloud Stack virtual machine password"), max_length=255, blank=True, null=True)
    host = models.ForeignKey('physical.Host', related_name="cs_host_attributes")

    def __unicode__(self):
        return "Cloud Stack host Attributes (host=%s)" % (self.host)

    class Meta:
        permissions = (
            ("view_cshostattribute", "Can view cloud stack host attributes"),
        )
        verbose_name_plural = "CloudStack Custom Host Attributes"

class DatabaseInfraAttr(BaseModel):

    ip = models.CharField(verbose_name=_("Cloud Stack reserved ip"), max_length=255, blank=True, null=True)
    dns = models.CharField(verbose_name=_("DNS"), max_length=255, blank=True, null=True)
    cs_ip_id = models.CharField(verbose_name=_("Cloud Stack id"), max_length=255, blank=True, null=True)
    is_write = models.BooleanField(verbose_name=_("Is write ip"), default=False)
    databaseinfra = models.ForeignKey('physical.DatabaseInfra', related_name="cs_dbinfra_attributes")

    def __unicode__(self):
        return "Cloud Stack reserved ip for %s" % (self.databaseinfra)

    class Meta:
        permissions = (
            ("view_csdatabaseinfraattribute", "Can view cloud stack databaseinfra attributes"),
        )
        verbose_name_plural = "CloudStack Custom DatabaseInfra Attributes"

class PlanAttr(BaseModel):

    serviceofferingid = models.ManyToManyField(CloudStackOffering)


    bundle = models.ManyToManyField(CloudStackBundle)

    userdata = models.TextField(verbose_name=_("User Data"),
                                help_text="Script to create config files")

    def __unicode__(self):
        return "Cloud Stack plan custom Attributes (plan=%s)" % (self.plan)

    class Meta:
        permissions = (
            ("view_csplanattribute", "Can view cloud stack plan custom attributes"),
        )
        verbose_name_plural = "CloudStack Custom Plan Attributes"


simple_audit.register(PlanAttr)
simple_audit.register(HostAttr)
simple_audit.register(DatabaseInfraAttr)
simple_audit.register(CloudStackBundle)
simple_audit.register(CloudStackOffering)
