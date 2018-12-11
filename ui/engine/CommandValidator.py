from ui.models import Field, Unit, UnitType, Command
import json

class CommandValidator:
    
    def getError(self, key):
        if key is None:
            return None
        return {
            'ok': 'Success',
            'escaped': 'Under attack, escaping',
            'destroyed': 'Unable to escape, destroyed',
            'removed': 'Not enough cities, removed',
            'not-used': 'Not used',
            'fail.cannot-place': 'Unit can not be placed here',
            'fail.not-strongest': 'Not strongest attack to target',
            'fail.not-stronger-than-opposite': 'Not stronger than counter attack',
            'fail.defence-stronger': 'Attack not stronger than defence',
            'fail.canceled-by-attack': 'Canceled by attack',
            'fail.target-not-empty': '{0} is not empty',
            'fail.more-moves-to-target': 'More moves to {0}',
            'fail.target-attacked': '{0} under attack',
            'fail.transport-missing': 'Transport missing',
            'fail.transport-canceled': 'Transport under attack',
            'fail.canceled-by-invasion': 'Canceled by invasion',
            'fail.unit-attacking-elsewhere': 'Supported unit attacks different target',
            'fail.unit-not-attacking': 'Supported unit does not attack',
            'fail.not-reachable-for-escape': 'Not reachable for escape',
            'fail.turn-closed': 'Turn closed, please refresh',
            'invalid.empty': 'No {0} defined',
            'invalid.not_next': 'Unreachable {0}',
            'invalid.not_reachable': 'Unit cannot go to {0}',
            'invalid.missing_unit': 'Missing unit on {0}',
            'invalid.not_unit': '{1} not found on {0}',
            'invalid.not_field': '{1} not on {0}',
        }[key]
    
    def getResult(self, command):
        keys = command.result.split(',')
        result = ''
        separator = ''
        for key in keys:
            if type(command) is Command:
                result += separator+self.getResultFromKey(key, command.commandType.template)
            #else:
            #    result += separator+self.getError(key)
            separator = '<br/>'
        return result
             
    def getResultFromKey(self, resultKey, template):
        if ':' in resultKey:
            # get error key
            index = resultKey.find(':')
            key = resultKey[:index]
            # get parameter from template
            data = self.parseTemplate(template)
            parIndex = resultKey.find('par_')
            par = int(resultKey[parIndex+4:])
            parText = str(data['T'][par][0]).lower()
            # get type
            type = resultKey[index+1:parIndex-1]
            # format result
            return self.getError(key).format(parText, type)
        else:
            return self.getError(resultKey)
        
    def isReachable(self, unitType, field):
        unitTypes = UnitType.objects.filter(pk=unitType.pk, fieldTypes=field.type)
        return len(unitTypes) == 1
    
    def validatePar(self, command, template, field, nextField, turn):
        #print('validate:'+str(field)+'-'+str(nextField)+':'+str(template))
        for condition in template:
            # if optional and not defined, return 'ok' and dont continue validation
            if condition == 'opt' and field is None:
                return None
            # verify availability on map if required
            if condition.startswith('next'):
                isNext = self.isNext(field, nextField)
                isReachable = self.isReachable(command.unit.unitType, nextField)
                if condition == 'next-or-self':
                    if field != nextField and not isNext:
                        return 'invalid.not_next:'
                else:
                    if not isNext:
                        return 'invalid.not_next:'
                if condition != 'next-any' and not isReachable:
                    return 'invalid.not_reachable:'
            # validate unit type
            if condition.startswith('unit_'):
                unitType = condition[5:]
                #print unitType
                if unitType == 'any':
                    if not self.isUnit(nextField, turn):
                        return 'invalid.missing_unit:'
                else:
                    if not self.isUnitType(nextField, unitType, turn):
                        return 'invalid.not_unit:'+unitType+'.'
            # validate field type
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
        turn = command.unit.turn
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
                    result = None
                    if arg != '0':
                        nextField = Field.objects.get(pk=arg)
                        result = self.validatePar(command, parTemplate, field, nextField, turn)
                    else:
                        nextField = field
                        result = self.validatePar(command, parTemplate, field, None, turn)
                    field = nextField
                    if result is not None:
                        return result + 'par_' + str(index)
                else:
                    if self.isMandatory(parTemplate):
                        return 'invalid.empty:par_'+str(index)
                index += 1
            if len(args) > len(data['T']):
                return 'invalid.too-many-parameters'
        else:
            if args != None and args != '':
                return 'invalid.too-many-parameters'
    
    def validateCommand(self, command):
        if not command.unit.unitType in command.commandType.unitType.all():
            return 'invalid.not-command-for-unit'
        result = self.validateArgs(command, command.unit.field)
        command.result = result
        return result

    def validateCityCommand(self, command):
        result = None
        if not self.isReachable(command.newUnitType, command.city.field):
            result = 'fail.cannot-place'
        return result
