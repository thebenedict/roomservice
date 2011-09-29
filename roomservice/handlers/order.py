#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from rapidsms.contrib.handlers.handlers.keyword import KeywordHandler
from rapidsms.models import Contact
from roomservice.models import Order
from roomservice.models import RoomNumberError, MenuError, GluttonError

menu = ["burger", "pizza"]

class OrderHandler(KeywordHandler):
    """
    A highly simplfied handler for hotel room service ordering it expects:
        order (3 digit room number) (menu item)
    For example:
        order 101 pizza
    If this format isn't followed it creates errors with a a foreign key to
    an order object marked for hotel staff followup. Possible Errors:
    
    MenuError: A valid menu item wasn't found in the order
    RoomError: A valid room number (i.e. 3 digits) wasn't found
    GluttonError: Order contained more than one food item
    """
    keyword = "o|order"

    def help(self):
        self.respond("Use \"order item room number\" to place an order. e.g."
                     "order burger 214")
        
    def handle(self, input):
        args = input.split(" ")
        new_order = Order()
        new_order.save()
        new_order.room_number = self._get_room_number(args)
        if not new_order.room_number:
            er = RoomNumberError(msg=self.msg.db_message, order=new_order)
            er.save()
        food_item = self._get_food_item(args)
        if food_item is None:
            em = MenuError(msg=self.msg.db_message, order=new_order)
            em.save()
        if food_item and args:
            extra = ", ".join(a for a in args if a.isalpha())
            eg = GluttonError(msg=self.msg.db_message, order=new_order, extra=extra)
            eg.save()
        new_order.food_item=food_item
        needs_followup = not (new_order.food_item and new_order.room_number)
        new_order.save()
        resp = "Thanks for your order."
        if new_order.haserrors:
            resp += " A manager will give you a call."
        if new_order.gluttonerror_set.all().exists():
            resp += eg.response_string
        self.respond(resp)

    def _get_room_number(self, args):
        for a in args:
            if len(a) == 3 and a.isdigit():
                args.remove(a)
                return int(a)
        return 0

    def _get_food_item(self, args):
        for a in args:
            if a.lower() in menu:
                args.remove(a)
                return a.lower()
        return None
