# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

#reference to django user model
User = get_user_model()

class Game(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User, blank=True)
    
    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game)
    owner = models.ForeignKey(User, null=True, default=None, blank=True)
    
    def __str__(self):
        return self.name
    
class FieldType(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game)

    def __str__(self):
        return self.name

class UnitType(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game)
    fieldTypes = models.ManyToManyField(FieldType)

    def __str__(self):
        return self.name

class Field(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(FieldType)
    home = models.ForeignKey(Country, null=True, default=None, blank=True)
    lon = models.DecimalField(max_digits=6, decimal_places=3)
    lat = models.DecimalField(max_digits=6, decimal_places=3)
    next = models.ManyToManyField('self', blank=True)
    
    def __str__(self):
        return self.name

class Unit(models.Model):
    unitType = models.ForeignKey(UnitType)
    country = models.ForeignKey(Country)
    field = models.ForeignKey(Field, null=True, default=None, blank=True)
    
    def __str__(self):
        return "[" + self.unitType + ":" + self.field + "]"

class Turn(models.Model):
    name = models.CharField(max_length=100)
    addingUnits = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class MoveType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Move(models.Model):
    moveType = models.ForeignKey(MoveType)
    turn = models.ForeignKey(Turn)
    unit = models.ForeignKey(Unit)
    
    def __str__(self):
        return "[" + self.turn.name + "." + self.unit.country.name + ":" + self.unit.field.name + "-" + self.moveType.name + "]"

class Target(models.Model):
    move = models.ForeignKey(Move)
    seq = models.IntegerField()
    field = models.ForeignKey(Field)
    
    def __str__(self):
        return field.name;
