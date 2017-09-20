from ui.models import Field, Unit, UnitType
import json

class CommandValidator:
    
    def getError(self, key):
        return {
            'invalid.empty': 'No {0} defined',
            'invalid.not_next': 'Unreachable {0}',
            'invalid.not_reachable': 'Unit cannot go to {0}',
            'invalid.missing_unit': 'Missing unit on {0}',
            'invalid.not_unit': '{1} not found on {0}',
            'invalid.not_field': '{1} not on {0}',
        }[key]
    
    def getResult(self, command):
        #print command.result
        # get error key
        index = command.result.find(':')
        key = command.result[:index]
        # get parameter from template
        data = self.parseTemplate(command.commandType.template)
        parIndex = command.result.find('par_')
        par = int(command.result[parIndex+4:])
        parText = str(data['T'][par][0]).lower()
        # get type
        type = command.result[index+1:parIndex-1]
        # format result
        return self.getError(key).format(parText, type)
        
    def isReachable(self, unitType, field):
        unitTypes = UnitType.objects.filter(pk=unitType.pk, fieldTypes=field.type)
        return len(unitTypes) == 1
    
    def validatePar(self, command, template, field, nextField, turn):
        #print('validate:'+str(field)+'-'+str(nextField)+':'+str(template))
        for condition in template:
            # handle both next (=must be also reachable) and next-any (=just next)
            if condition.startswith('next'):
                if not self.isNext(field, nextField):
                    return 'invalid.not_next:'
                if condition == 'next' and not self.isReachable(command.unit.unitType, nextField):
                    return 'invalid.not_reachable:'
            if condition.startswith('unit_'):
                unitType = condition[5:]
                #print unitType
                if unitType == 'any':
                    if not self.isUnit(nextField, turn):
                        return 'invalid.missing_unit:'
                else:
                    if not self.isUnitType(nextField, unitType, turn):
                        return 'invalid.not_unit:'+unitType+'.'
            if condition.startswith('field_'):
                fieldType = condition[6:]
                if not self.isFieldType(nextField, fieldType):
                    return 'invalid.not_field:'+fieldType+'.'
        return None
    
    def isNext(self, field, nextField):
        nf = field.next.filter(pk=nextField.pk)
        return len(nf) == 1
    
    def isUnit(self, field, turn):
        units = Unit.objects.filter(turn=turn, field=field)
        return len(units) == 1
    
    def isUnitType(self, field, type, turn):
        units = Unit.objects.filter(turn=turn, field=field)
        return len(units) == 1 and units[0].unitType.name == type
    
    def isFieldType(self, field, type):
        return field.type.name == type
    
    def isMandatory(self, template):
        for condition in template:
            if condition == 'opt':
                return False
        return True
    
    def parseTemplate(self, template):
        return json.loads('{"T":['+template+"]}")
    
    def validateArgs(self, command, firstField):
        turn = command.turn
        template = command.commandType.template
        args = command.args
        #print('template:'+str(template))
        #print('args:'+str(args))
        if template != '[]':
            data = self.parseTemplate(template)
            args = args.split(',')
            index = 0
            field = firstField
            for par in data['T']:
                parName = par[0]
                parTemplate = par[1]
                #print('par:'+str(parName)+'='+str(parTemplate))
                if index < len(args) and args[index] != '' and args[index] != '0':
                    arg = args[index]
                    #print('arg:'+str(arg))
                    nextField = Field.objects.get(pk=arg)
                    result = self.validatePar(command, parTemplate, field, nextField, turn)
                    if result is not None:
                        return result + 'par_' + str(index)
                    field = nextField
                else:
                    if self.isMandatory(parTemplate):
                        return 'invalid.empty:par_'+str(index)
                index += 1
    
    def validateCommand(self, command):
        result = self.validateArgs(command, command.unit.field)
        command.result = result

