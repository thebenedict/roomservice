#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.db import models
from rapidsms_httprouter.models import Message

class RapidError(models.Model):
    """
    A base class for RapidSMS messaging errors
    """
   
    msg = models.ForeignKey(Message)

    @property
    def response_string(self):
        return("")

    class Meta:
        abstract=True

