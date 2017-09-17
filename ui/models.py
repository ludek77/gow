# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

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
    template = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User, blank=True)
    tileServer= models.CharField(max_length = 100)
    winPoints = models.IntegerField(default=50) #win points needed to win the game
    defaultCommandType = models.ForeignKey(CommandType)
    
    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game)
    color = models.CharField(max_length=10)
    lat = models.DecimalField(max_digits=5, decimal_places=2)
    lng = models.DecimalField(max_digits=5, decimal_places=2)
    owner = models.ForeignKey(User, null=True, default=None, blank=True)
    
    def __str__(self):
        return str(self.pk) + '.' + self.game.name + '.'+ self.name

class Field(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(FieldType)
    game = models.ForeignKey(Game)
    lat = models.DecimalField(max_digits=5, decimal_places=2)
    lng = models.DecimalField(max_digits=5, decimal_places=2)
    home = models.ForeignKey(Country, null=True, default=None, blank=True)
    isCity = models.BooleanField(default=False)
    defaultPriority = models.IntegerField(null=True, default=None, blank=True)
    defaultUnitType = models.ForeignKey(UnitType, null=True, default=None, blank=True)
    unitPoints = models.IntegerField(default=0) #unit points for this field
    winPoints = models.IntegerField(default=0) #wictory points for this field
    next = models.ManyToManyField('self', blank=True)
    
    def __str__(self):
        return self.game.name + '.' + self.name + '.' + str(self.pk)

class Turn(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game)
    newUnits = models.BooleanField(default=False)
    open = models.BooleanField(default=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return str(self.pk) + '.' + self.name

class City(models.Model):
    turn = models.ForeignKey(Turn)
    field = models.ForeignKey(Field)
    country = models.ForeignKey(Country, null=True, default=None, blank=True)
    
    def __str__(self):
        return "[" + str(self.country.pk) + '.' + self.country.name + "," + self.turn.name + "," + str(self.field.pk) + '.' + self.field.name + "]"

class CityCommand(models.Model):
    city = models.ForeignKey(City)
    priority = models.IntegerField()
    newUnitType = models.ForeignKey(UnitType)
    result = models.CharField(max_length=50, null=True, default=None, blank=True)
    
    def __str__(self):
        return "["+str(self.priority)+"."+self.city.country.name+"."+self.newUnitType.name+"]"

class Unit(models.Model):
    turn = models.ForeignKey(Turn)
    country = models.ForeignKey(Country)
    unitType = models.ForeignKey(UnitType)
    field = models.ForeignKey(Field, null=True, default=None, blank=True)
    
    def __str__(self):
        return "[" + self.turn.name + "." + self.country.name + "." + self.unitType.name + "." + self.field.name + "]"

class Command(models.Model):
    turn = models.ForeignKey(Turn)
    unit = models.ForeignKey(Unit)
    commandType = models.ForeignKey(CommandType)
    args = models.CharField(max_length=100, default='',blank=True)
    result = models.CharField(max_length=50, null=True, default=None, blank=True)
    
    def __str__(self):
        return "[" + self.turn.name + "." + self.unit.country.name + "." + self.unit.field.name + "." + self.commandType.name + "]"

class Target(models.Model):
    command = models.ForeignKey(Command)
    seq = models.IntegerField()
    field = models.ForeignKey(Field)
    
    def __str__(self):
        return "[" + seq + "." + field.name + "]";
