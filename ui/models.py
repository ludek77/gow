# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

#reference to django user model
User = get_user_model()

class FieldType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UnitType(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    fieldTypes = models.ManyToManyField(FieldType)
    unitPoints = models.IntegerField(default=1) #price of this unit

    def __str__(self):
        return str(self.pk) + '.' + self.name

class CommandType(models.Model):
    name = models.CharField(max_length=100)
    unitType = models.ManyToManyField(UnitType, blank=True)
    template = models.CharField(max_length=200)
    # command arguments
    attackPower = models.IntegerField(default=0) # my own attack power or support power if support
    defencePower = models.IntegerField(default=1) # my own defence power, plus if support and attackPower is 0, it's also supporting defence
    cancelByAttack = models.BooleanField(default=False)
    support = models.BooleanField(default=False)
    move = models.BooleanField(default=False)
    transport = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User, blank=True)
    tileServer= models.CharField(max_length = 100)
    winPoints = models.IntegerField(default=50) #win points needed to win the game
    defaultCommandType = models.ForeignKey(CommandType, on_delete=models.PROTECT)
    turnMinutes = models.IntegerField(default=5)
    
    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    color = models.CharField(max_length=10)
    lat = models.DecimalField(max_digits=5, decimal_places=2)
    lng = models.DecimalField(max_digits=5, decimal_places=2)
    owner = models.ForeignKey(User, null=True, default=None, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.pk) + '.' + self.game.name + '.'+ self.name

class Field(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(FieldType, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    lat = models.DecimalField(max_digits=5, decimal_places=2)
    lng = models.DecimalField(max_digits=5, decimal_places=2)
    home = models.ForeignKey(Country, null=True, default=None, blank=True, on_delete=models.PROTECT)
    isCity = models.BooleanField(default=False)
    defaultPriority = models.IntegerField(null=True, default=None, blank=True)
    defaultUnitType = models.ForeignKey(UnitType, null=True, default=None, blank=True, on_delete=models.PROTECT)
    unitPoints = models.IntegerField(default=0) #unit points for this field
    winPoints = models.IntegerField(default=0) #wictory points for this field
    next = models.ManyToManyField('self', blank=True)
    
    def __str__(self):
        return self.game.name + '.' + self.name + '.' + str(self.pk)

class Turn(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    newUnits = models.BooleanField(default=False)
    open = models.BooleanField(default=True)
    deadline = models.DateTimeField(null=True, blank=True)
    previous = models.ForeignKey('self', null=True, default=None, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.pk) + '.' + self.name

class City(models.Model):
    turn = models.ForeignKey(Turn, on_delete=models.PROTECT)
    field = models.ForeignKey(Field, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, null=True, default=None, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return "[" + str(self.country.pk) + '.' + self.country.name + "," + self.turn.name + "," + str(self.field.pk) + '.' + self.field.name + "]"

class CityCommand(models.Model):
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    priority = models.IntegerField()
    newUnitType = models.ForeignKey(UnitType, on_delete=models.PROTECT)
    result = models.CharField(max_length=50, null=True, default=None, blank=True)
    
    def __str__(self):
        return "["+str(self.city.turn.name)+"."+self.city.country.name+"."+str(self.priority)+"."+self.city.field.name+"."+self.newUnitType.name+"]"

class Unit(models.Model):
    turn = models.ForeignKey(Turn, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    unitType = models.ForeignKey(UnitType, on_delete=models.PROTECT)
    field = models.ForeignKey(Field, null=True, default=None, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return "[" + self.turn.name + "." + self.country.name + "." + self.unitType.name + "." + self.field.name + "]"

class Command(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    commandType = models.ForeignKey(CommandType, on_delete=models.PROTECT)
    args = models.CharField(max_length=100, default='',blank=True)
    escape = models.CharField(max_length=100, default='',blank=True)
    removePriority = models.IntegerField(default=0)
    result = models.CharField(max_length=50, null=True, default=None, blank=True)
    
    def __str__(self):
        return "[" + self.unit.country.name + "." + self.unit.field.name + "." + self.commandType.name + "]"
