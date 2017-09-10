# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

#reference to django user model
User = get_user_model()

class Game(models.Model):
    name = models.CharField(max_length=100)
    winPoints = models.IntegerField()
    user = models.ManyToManyField(User, blank=True)
    tileServer= models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game)
    email = models.CharField(max_length=100)
    color = models.CharField(max_length=10)
    lon = models.DecimalField(max_digits=6, decimal_places=3)
    lat = models.DecimalField(max_digits=6, decimal_places=3)
    owner = models.ForeignKey(User, null=True, default=None, blank=True)
    
    def __str__(self):
        return self.name
    
class FieldType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UnitType(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    fieldTypes = models.ManyToManyField(FieldType)

    def __str__(self):
        return self.name

class Field(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(FieldType)
    game = models.ForeignKey(Game)
    lon = models.DecimalField(max_digits=6, decimal_places=3)
    lat = models.DecimalField(max_digits=6, decimal_places=3)
    home = models.ForeignKey(Country, null=True, default=None, blank=True)
    isCity = models.BooleanField(default=False)
    points = models.IntegerField()
    next = models.ManyToManyField('self', blank=True)
    
    def __str__(self):
        return self.name

class Turn(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game)
    addingUnits = models.BooleanField(default=False)
    open = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class City(models.Model):
    turn = models.ForeignKey(Turn)
    field = models.ForeignKey(Field)
    country = models.ForeignKey(Country, null=True, default=None, blank=True)
    
    def __str__(self):
        return "[" + self.turn.name + "." + self.country.name + "." + self.field.name + "]"

class Unit(models.Model):
    turn = models.ForeignKey(Turn)
    country = models.ForeignKey(Country)
    unitType = models.ForeignKey(UnitType)
    field = models.ForeignKey(Field, null=True, default=None, blank=True)
    
    def __str__(self):
        return "[" + self.turn.name + "." + self.country.name + "." + self.unitType + "." + self.field.name + "]"

class MoveType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Move(models.Model):
    turn = models.ForeignKey(Turn)
    unit = models.ForeignKey(Unit)
    moveType = models.ForeignKey(MoveType)
    
    def __str__(self):
        return "[" + self.turn.name + "." + self.unit.country.name + "." + self.unit.field.name + "." + self.moveType.name + "]"

class Target(models.Model):
    move = models.ForeignKey(Move)
    seq = models.IntegerField()
    field = models.ForeignKey(Field)
    
    def __str__(self):
        return "[" + seq + "." + field.name + "]";
