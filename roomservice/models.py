from django.db import models
from datetime import datetime
from error_framework.models import RapidError

class Order(models.Model):
    """
    What a client wants for dinner.
    Highly simplified model for demoing a contrib error app.
    """

    room_number = models.IntegerField(max_length=3, blank=True, null=True)
    food_item = models.CharField(max_length=20, blank=True, null=True)
    needs_followup = models.BooleanField()
    datetime_created = models.DateTimeField()

    @property
    def haserrors(self):
        return (self.gluttonerror_set.all().exists() | \
                self.menuerror_set.all().exists() | \
                self.roomnumbererror_set.all().exists())

    def save(self, *args, **kwargs):
        if not self.datetime_created:
            self.datetime_created = datetime.today()
        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.room_number and self.food_item:
            return "%s (%s)" % (self.food_item, self.room_number)
        else:
            return "Needs followup"

class RoomNumberError(RapidError):
    order = models.ForeignKey(Order)
    
class MenuError(RapidError):
    order = models.ForeignKey(Order)

class GluttonError(RapidError):
    order = models.ForeignKey(Order)
    extra = models.CharField(max_length=100)

    @property
    def response_string(self):
        return(" Please order %s separately" % self.extra)
        

