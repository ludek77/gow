# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Game, Country, Field, FieldType, UnitType, Unit, Turn, CommandType, Command, Target, City

admin.site.register(Game)
admin.site.register(Country)
admin.site.register(FieldType)
admin.site.register(UnitType)
admin.site.register(Field)
admin.site.register(Unit)
admin.site.register(Turn)
admin.site.register(CommandType)
admin.site.register(Command)
admin.site.register(Target)
admin.site.register(City)
