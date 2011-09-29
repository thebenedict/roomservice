from .models import Order
from .errors import GluttonError, MenuError, RoomNumberError
from django.contrib import admin

admin.site.register(Order)
admin.site.register(GluttonError)
admin.site.register(MenuError)
admin.site.register(RoomNumberError)
