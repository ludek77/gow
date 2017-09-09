# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Game, Country, Field, FieldType, UnitType, UnitFieldRef, Unit, Turn, MoveType, Move

admin.site.register(Game)
admin.site.register(Country)
admin.site.register(FieldType)
admin.site.register(UnitType)
admin.site.register(UnitFieldRef)
admin.site.register(Field)
admin.site.register(Unit)
admin.site.register(Turn)
admin.site.register(MoveType)
admin.site.register(Move)
