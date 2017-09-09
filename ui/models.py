# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    game = models.ForeignKey(Game)
    
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

    def __str__(self):
        return self.name

class UnitFieldRef(models.Model):
    unit = models.ForeignKey(UnitType)
    fieldType = models.ForeignKey(FieldType)
    
    def __str__(self):
        return "[" + self.unit.__str__() + ":" + self.fieldType.__str__() + "]"
  
class Field(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(FieldType)
    home = models.ForeignKey(Country, null=True, default=None)
    
    def __str__(self):
        return self.name

class Unit(models.Model):
    unitType = models.ForeignKey(UnitType)
    country = models.ForeignKey(Country)
    field = models.ForeignKey(Field, null=True, default=None)
    
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
