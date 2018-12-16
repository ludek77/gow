var unitTypes = 'empty';
var selectedField=null;
var commandArgs=[];

function login() {
	$.post('login/', $('#login-form').serialize())
		.done(function(data){location.reload();})
		.fail(function(data,status,error){$('#login-form')[0].reset();$('#login-error').html(error);});
}

function logout() {
	$.get("logout/", function(data) {location.reload()});
}

function previousTurn() {
	$.get('/ui/turn_previous/', function(data) {location.reload()});
}

function nextTurn() {
	$.get('/ui/turn_next/', function(data) {location.reload()});
}

var mapClickHandler = null;
function onMapClick(e) {
	if(mapClickHandler != null) mapClickHandler(e);
}

var fieldClickHandler = defaultClickField;
function onClickField(e,pk) {
	if(fieldClickHandler != null) fieldClickHandler(e,pk);
}

function defaultClickField(e,pk) {
	selectedField=pk;
	$.get('unit_get?f='+pk, function(data) {
		var json = $.parseJSON(data);
		renderFieldDialog(json);
	});
}

function renderFieldDialog(json) {
	openDialog('/ui/field_dialog/', 'Field', function() {
		setDialogTitle(json.field.name + ': ' + json.field.type);
		if(json.field.owner) {
			$('#field-dialog .country').show();
			$('#field-dialog .country-name').text(json.field.owner.country);
			$('#field-dialog .country-color').css('background-color',json.field.owner.color).css('color',json.field.owner.textColor);
		} else {
			$('#field-dialog .country').hide();
		}
		if(json.field.home) {
			$('#field-dialog .home').show();
			$('#field-dialog .home-name').text(json.field.home.name);
			$('#field-dialog .home-color').css('background-color',json.field.home.color).css('color',json.field.home.textColor);
		} else {
			$('#field-dialog .home').hide();
		}
		if(json.unit) {
			$('#field-dialog .unit').show();
			$('#field-dialog .unit-country').text(json.unit.country);
			$('#field-dialog .unit-type').text(json.unit.type);
		    $('#field-dialog .unit-color').css('background-color',json.unit.color).css('color',json.unit.textColor);
		} else {
			$('#field-dialog .unit').hide();
		}
		commandArgs = [];
		if(json.cmds && json.command) {
			if(json.command.args) {
				for(var i = 0; i < json.command.args.length; i++) {
					commandArgs[i] = json.command.args[i].pk;
				}
			}
			$('#field-dialog .unit-owner-only').show();
			setOptions($('#unit-command'), json.cmds);
			$('#unit-command').val(json.command.pk).prop('disabled',!json.open);
			$('#unit-command-result').html(json.command.result);
			firstEmpty = setupArguments(json.command.template,json.command.args,json.open);
			if(firstEmpty != null) {
				selectTarget(firstEmpty);
			}
		} else {
			$('#field-dialog .unit-owner-only').hide();
			$('#unit-command').html('');
		}
		if(json.command && json.command.escape) {
			$('#field-dialog .escape').show();
			$('#field-dialog .escape-field').text(json.command.escape.name);
			if(json.open) {
				$('#field-dialog .escape-field').addClass('clickable').click(function(){selectEscape()});
			}
		} else {
			$('#field-dialog .escape').hide();
			$('#field-dialog .escape-field').html('');
		}
		if(json.message) {
			$('#unit-command-result').html(json.message);
		}
		if(json.citycommand) {
			$('#field-dialog .field-owner-only').show();
			setOptions($('#field-command'), json.citycommand.fcmds);
			$('#field-command').val(json.citycommand.pk).prop('disabled',!json.open);
			$('#field-command-result').html(json.citycommand.result);
		} else {
			$('#field-dialog .field-owner-only').hide();
		}
	});
}

function setupArguments(template,args,enabled) {
	$('#unit-command-targets').html('');
	var firstEmpty = null;
	for(var i = 0; i < template.length; i++) {
		if(template[i] != '') {
			var arg = null;
			if(args && args.length >= i) arg = args[i];
			empty = appendTarget(i,template[i][0],template[i][1],arg,enabled);
			if(empty && firstEmpty == null) {
				firstEmpty = i;
			}
		}
	}
	return firstEmpty;
}

function appendTarget(index,text,param,arg,enabled) {
	var empty = true;
	if(arg == null || arg[0] == 0) {
		arg = [null,'Select'];
	} else {
		empty = false;
	}
	var target = '<span id="target-'+index+'">'+arg.name+'</span>';;
	if(enabled) target = '<span id="target-'+index+'" class="clickable" onclick="selectTarget('+index+')">'+arg.name+'</span>';    
	$('#unit-command-targets')
		.append('<div class="unit-param">')
		.append('<span class="label">'+text+'</span>')
		.append(target)
		.append('</div>');
	return empty;
}

var selectedTarget = null;
function selectTargetFunction(tid, param, clickFunction) {
	$(tid).text('Select Target');
	$(tid).addClass('active');
	selectedTarget = param;
	fieldClickHandler = clickFunction;
}

function selectTarget(param) {
	selectTargetFunction('#target-'+param, param, clickTarget);	
}

function selectEscape() {
	selectTargetFunction('#escape-0', null, clickEscape);
}

function clickTarget(e,pk) {
	commandArgs[selectedTarget] = pk;
	for(var i = 0; i < commandArgs.length; i++) {
		if(commandArgs[i] == null) commandArgs[i] = 0;
	}
	var ct = $('#unit-command').val();
	$.get('/ui/unit_command/?f='+selectedField+'&ct='+ct+'&args='+commandArgs, function(data) {
		var json = $.parseJSON(data);
		renderFieldDialog(json);
		renderCountryDialog();
		hideCommand(selectedField);
		if(json.field && json.command.args && json.command.res != 'invalid') {
			if(json.command.args[0]) {
				renderCommand(json.field.ll[0],json.field.ll[1],json.command.args[0].ll[0],json.command.args[0].ll[1],json.unit.color,json.command.name,selectedField);
				if(json.command.args[1]) {
					renderCommand(json.command.args[0].ll[0],json.command.args[0].ll[1],json.command.args[1].ll[0],json.command.args[1].ll[1],json.unit.color,json.command.name,selectedField);
				}
			}
		}
	});
	fieldClickHandler = defaultClickField;
}

function clickEscape(e,pk) {
	$.get('/ui/unit_command/?f='+selectedField+'&ct=esc&args='+pk, function(data) {
		var json = $.parseJSON(data);
		renderFieldDialog(json);
		renderCountryDialog();
	});
	fieldClickHandler = defaultClickField;
}

function setupGameList(selectedGame) {
	$.get('/ui/game_list/',function(data){
		var json = $.parseJSON(data);
		for(var i in json) {
		     var id = json[i].id;
		     var name = json[i].name;
		     $('#select-game').append(option(id,name));
		}
		$('#select-game').val(selectedGame);
	});
}

function setupGame() {
	$.get('/ui/game_setup/',function(data){
		var json = $.parseJSON(data);
		unitTypes = {};
		for(var i in json.unitTypes) {
			unitTypes[json.unitTypes[i][0]] = json.unitTypes[i];
		}
		for(var i in json.units) {
			var unit = json.units[i];
			renderUnit(unit.latlng[0],unit.latlng[1], unit.id, unit.fid, unit.clr, unit.type);
			if(unit.tgt && unit.res != 'invalid') {
				renderCommand(unit.latlng[0],unit.latlng[1],unit.tgt[0][0],unit.tgt[0][1],unit.clr,unit.cmd,unit.fid);
				if(unit.tgt[1]) {
					renderCommand(unit.tgt[0][0],unit.tgt[0][1],unit.tgt[1][0],unit.tgt[1][1],unit.clr,unit.cmd+'1',unit.fid);
				}
			}
		}
		for(var i in json.paths) {
			var ll1 = json.paths[i][0];
			var ll2 = json.paths[i][1];
			var pk1 = json.paths[i][2];
			var pk2 = json.paths[i][3];
			renderPath(ll1[0],ll1[1],ll2[0],ll2[1], pk1, pk2);
		}
		for(var i in json.fields) {
			var field = json.fields[i];
			if(field.color != '') {
				if(field.color == '-') field.color = emptyColor;
				renderCity(field.latlng[0],field.latlng[1], field.id, field.color, field.home);
			} else {
		    	renderField(field.latlng[0],field.latlng[1], field.id);
		    }
		}
		
		renderCountryDialog();
	});
}

function renderCountryDialog() {
	$.get('/ui/country_setup/',function(data){
		$('#commands-content').html('');
		var json= $.parseJSON(data);
		for(var c in json.countries) {
			country = json.countries[c];
			content = '<div id="country-'+country.pk+'" class="country" style="background-color:'+country.clr+';color:'+country.fgclr+'"><span>'+country.name+'</span>';
			content += '<div class="units">';
			for(var i in country.units) {
				content += appendUnitCommand(country.units[i],json.open, country.clr);
			}
			content += '</div><div class="cities">';
			for(var i in country.cities) {
				content += appendCityCommand(country.cities[i],json.open, country.clr);
			}
			content += '</div></div>';
			$('#commands-content').append(content);
		}
		
		$('#commands .unit-prio').click(function() {
			var eId = $(this).attr('id');
			var idx = eId.indexOf('_');
			var fId = eId.substring(0,idx);
			var direction = eId.substring(idx+1);
			$.get('unit_command/?f='+fId+'&ct=prio&args='+direction, function(data) {
				renderCountryDialog();
			});
		});
		$('#commands .city-prio').click(function() {
			var eId = $(this).attr('id');
			var idx = eId.indexOf('_');
			var fId = eId.substring(0,idx);
			var direction = eId.substring(idx+1);
			$.get('city_command/?f='+fId+'&ct=prio&args='+direction, function(data) {
				renderCountryDialog();
			});
		});
	});
}

function appendUnitCommand(unit,open,clr) {
	var unitType = unitTypes[unit.type][4];
	var cmdResult = '';
	if(unit.txt) {
		cmdResult = unit.txt;
	}
	content  = '<div class="units" style="background-color:'+clr+'" title="'+cmdResult+'">';
	if(open) {
		content += '<input class="unit-prio button-icon first" type="button" id="'+unit.fieldId+'_-9"/>'
		content += '<input class="unit-prio button-icon prev" type="button"  id="'+unit.fieldId+'_-1"/>'
		content += '<input class="unit-prio button-icon next" type="button"  id="'+unit.fieldId+'_+1"/>'
		content += '<input class="unit-prio button-icon last" type="button"  id="'+unit.fieldId+'_+9"/>'
	}
	content += '<span class="command-target" onclick="focusLatLng('+unit.latlng[0]+','+unit.latlng[1]+');onClickField('+unit.id+','+unit.fieldId+')">'+unit.field+'</span>';
	//content += '<span class="unit-type">'+unitType+'</span>';
	content += '<span class="command res_'+unit.res+'">'+unit.command+'</span>';
	for(var i in unit.args) {
		content += '<span class="unit-target">'+unit.args[i]+'</span>'
	}
	content += '</div>';
	return content;
}

function appendCityCommand(city,open,clr) {
	content =  '<div class="cities">';
	if(open) {
		content += '<input class="city-prio button-icon first" type="button" id="'+city.fieldId+'_-9"/>'
		content += '<input class="city-prio button-icon prev" type="button"  id="'+city.fieldId+'_-1"/>'
		content += '<input class="city-prio button-icon next" type="button"  id="'+city.fieldId+'_+1"/>'
		content += '<input class="city-prio button-icon last" type="button"  id="'+city.fieldId+'_+9"/>'
	}
	content += '<span class="command-target" onclick="focusLatLng('+city.latlng[0]+','+city.latlng[0]+');onClickField('+city.id+','+city.fieldId+')">'+city.field+'</span>';
	content += '<span class="command res_'+city.res+'">Add '+city.newUnit+'</span>';
	content += '</div>';
	return content;
}
