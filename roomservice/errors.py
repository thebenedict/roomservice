#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from django.db import models
from error_framework.models import RapidError
import roomservice

class RoomNumberError(RapidError):
    order = models.ForeignKey(roomservice.models.Order)

class MenuError(RapidError):
    order = models.ForeignKey(roomservice.models.Order)

class GluttonError(RapidError):
    order = models.ForeignKey(roomservice.models.Order)
    extra = models.CharField(max_length=100)

    @property
    def response_string(self):
        return("Please order %s separately" % extra)

