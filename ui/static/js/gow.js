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
	openDialog('/ui/field_dialog', 'Field', function() {
		setDialogTitle(json.field + ': ' + json.type);
		if(json.country) {
			$('#field-dialog .country').show();
			$('#field-dialog .country-name').text(json.country);
			$('#field-dialog .country-color').css('background-color',json.fieldColor).css('color',json.fieldTextColor);
		} else {
			$('#field-dialog .country').hide();
		}
		if(json.home) {
			$('#field-dialog .home').show();
			$('#field-dialog .home-name').text(json.home);
			$('#field-dialog .home-color').css('background-color',json.homeColor).css('color',json.homeTextColor);
		} else {
			$('#field-dialog .home').hide();
		}
		if(json.unitType) {
			$('#field-dialog .unit').show();
			$('#field-dialog .unit-country').text(json.unitCountry);
			$('#field-dialog .unit-type').text(json.unitType);
		    $('#field-dialog .unit-color').css('background-color',json.unitColor).css('color',json.unitTextColor);
		} else {
			$('#field-dialog .unit').hide();
		}
		commandArgs = [];
		if(json.cmds && json.cmd) {
			for(var i = 0; i < json.cmd[2].length; i++) {
				commandArgs[i] = json.cmd[2][i][0];
			}
			$('#field-dialog .unit-owner-only').show();
			setOptions($('#unit-command'), json.cmds);
			$('#unit-command').val(json.cmd[0]).prop('disabled',!json.open);
			$('#unit-command-result').html(json.cmd[3]);
			firstEmpty = setupArguments(json.cmd[1],json.cmd[2],json.open);
			if(firstEmpty != null) {
				selectTarget(firstEmpty);
			}
		} else {
			$('#field-dialog .unit-owner-only').hide();
			$('#unit-command').html('');
		}
		if(json.esc) {
			$('#field-dialog .escape').show();
			$('#field-dialog .escape-field').text(json.esc[1]);
		} else {
			$('#field-dialog .escape').hide();
			$('#field-dialog .escape-field').html('');
		}
		if(json.message) {
			$('#unit-command-result').html(json.message);
		}
		if(json.fcmd) {
			$('#field-dialog .field-owner-only').show();
			setOptions($('#field-command'), json.fcmds);
			$('#field-command').val(json.fcmd).prop('disabled',!json.open);
			$('#field-command-result').html(json.fresult);
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
			if(args.length >= i) arg = args[i];
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
	var target = '<span id="target-'+index+'">'+arg[1]+'</span>';;
	if(enabled) target = '<span id="target-'+index+'" class="clickable" onclick="selectTarget('+index+')">'+arg[1]+'</span>';    
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
	});
	fieldClickHandler = defaultClickField;
}

function clickEscape(e,pk) {
	$.get('unit_command/?f='+selectedField+'&ct=esc&args='+pk, function(data) {
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
		for(var i in json.units) {
			var unit = json.units[i];
			renderUnit(unit.latlng[0],unit.latlng[1], unit.id, unit.fid, unit.clr, unit.type);
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
