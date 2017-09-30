var unitTypes = 'empty';
var selectedField=null;
var commandArgs=[];

function login() {
	$.post('login/', $('#login-form').serialize())
		.done(function(data){location.reload();})
		.fail(function(data,status,error){$('#login-form')[0].reset();$('#login-error').html(error);});
}

function logout() {
	$.get("logout", function(data) {location.reload()});
}

function previousTurn() {
	$.get('turn_previous', function(data) {location.reload()});
}

function nextTurn() {
	$.get('turn_next', function(data) {location.reload()});
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
			$('#field-dialog .countryName').text(json.country);
		} else {
			$('#field-dialog .country').hide();
		}
		if(json.unitType) {
			$('#field-dialog .unit').show();
			$('#field-dialog .unitCountry').text(json.unitCountry);
			$('#field-dialog .unitType').text(json.unitType);
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
function selectTarget(param) {
	$('#target-'+param).text('Pick target field');
	selectedTarget = param;
	fieldClickHandler = clickTarget;
}

function clickTarget(e,pk) {
	commandArgs[selectedTarget] = pk;
	for(var i = 0; i < commandArgs.length; i++) {
		if(commandArgs[i] == null) commandArgs[i] = 0;
	}
	var ct = $('#unit-command').val();
	$.get('unit_command/?f='+selectedField+'&ct='+ct+'&args='+commandArgs, function(data) {
		var json = $.parseJSON(data);
		renderFieldDialog(json);
		renderCountryDialog();
	});
	fieldClickHandler = defaultClickField;
}

function setupGameList(selectedGame) {
	$.get('game_list',function(data){
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
	$.get('game_setup',function(data){
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
			var pk = json.fields[i][0];
		    var latlng = json.fields[i][1];
		    var clr = json.fields[i][2];
			if(clr != '') {
				if(clr == '-') clr = emptyColor;
				renderCity(latlng[0],latlng[1], pk, clr);
			} else {
		    	renderField(latlng[0],latlng[1], pk);
		    }
		}
		for(var i in json.units) {
			var pk = json.units[i][0];
			var fpk = json.units[i][1];
			var latlng = json.units[i][2];
			var clr = json.units[i][3];
			var type = json.units[i][4];
			renderUnit(latlng[0],latlng[1], pk, fpk, clr, type);
		}
		
		renderCountryDialog();
	});
}

function renderCountryDialog() {
	$.get('country_setup/',function(data){
		$('#commands-content').html('');
		var json= $.parseJSON(data);
		for(var c in json.countries) {
			country = json.countries[c];
			$('#commands-content').append('<div class="country">'+country.name+'</div>');
			for(var i in country.units) {
				appendUnitCommand(country.units[i]);
			}
			for(var i in country.cities) {
				appendCityCommand(country.cities[i]);
			}
		}
	});
}

function appendUnitCommand(unit) {
	var unitType = unitTypes[unit.type][4];
	content  = '<div>';
	content += '<span class="clickable" onclick="focusLatLng('+unit.latlng[0]+','+unit.latlng[1]+');onClickField('+unit.id+','+unit.fieldId+')">'+unit.field+'</span>';
	content += '<span>'+unitType+'</span>';
	content += '<span>'+unit.command+'</span>';
	for(var i in unit.args) {
		content += '<span>'+unit.args[i]+'</span>'
	}
	content += '</div>';
	$('#commands-content').append(content);
}

function appendCityCommand(city) {
	content =  '<div>';
	content += '<span class="clickable" onclick="focusLatLng('+city.latlng[0]+','+city.latlng[0]+');onClickField('+city.id+','+city.fieldId+')">'+city.field+'</span>';
	content += '<span>add '+city.field+'</span>';
	content += '</div>';
	$('#commands-content').append(content);
}
