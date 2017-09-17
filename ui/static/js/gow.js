var unitTypes = 'empty';
var selectedField=null;
var commandArgs=[];

function login() {
	$.post('login/', $('#login-form').serialize())
		.done(function(data){location.reload();})
		.fail(function(data,status,error){$('#login-form')[0].reset();$('#login-error').html(error);});
}

function logout() {
	$.get("logout", function( data ) {
		location.reload();
	});
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
		$('#field-dialog .country').text(json.country);
		$('#field-dialog .unitType').text(json.type);
		$('#field-dialog .field').text(json.field);
		commandArgs = [];
		if(json.cmds && json.cmd) {
			for(var i = 0; i < json.cmd[2].length; i++) {
				commandArgs[i] = json.cmd[2][i][0];
			}
			$('#field-dialog .unit-owner-only').show();
			setOptions($('#unit-command'), json.cmds);
			$('#unit-command').val(json.cmd[0]);
			setupUnitDialog(json.cmd[1],json.cmd[2]);
		} else {
			$('#field-dialog .unit-owner-only').hide();
			$('#unit-command').html('');
		}
		if(json.fcmd) {
			$('#field-dialog .field-owner-only').show();
			setOptions($('#add-unit-command'), json.fcmds);
			$('#add-unit-command').val(json.fcmd);
		} else {
			$('#field-dialog .field-owner-only').hide();
		}
	});
}

function appendTarget(index,text,param,arg) {
	if(arg == null) arg = [null,'Select'];
	$('#unit-command-targets')
		.append('<div class="unit-param">')
		.append('<span class="label">'+text+'</span>')
		.append('<span id="target-'+index+'" class="clickable" onclick="selectTarget('+index+')">'+arg[1]+'</span>')
		.append('</div>');
}

var selectedTarget = null;
function selectTarget(param) {
	$('#target-'+param).text('Pick target field');
	selectedTarget = param;
	fieldClickHandler = clickTarget;
}

function clickTarget(e,pk) {
	commandArgs[selectedTarget] = pk;
	var ct = $('#unit-command').val();
	$.get('unit_command/?f='+selectedField+'&ct='+ct+'&args='+commandArgs, function(data) {
		var json = $.parseJSON(data);
		renderFieldDialog(json);
	});
	fieldClickHandler = defaultClickField;
}

function setupUnitDialog(template,args) {
	$('#unit-command-targets').html('');
	for(var i = 0; i < template.length; i++) {
		if(template[i] != '') {
			var arg = null;
			if(args.length >= i) arg = args[i];
			appendTarget(i,template[i][0],template[i][1],arg);
		}
	}
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
		
		$.get('country_setup/',function(data){
			var json= $.parseJSON(data);
			var units = json.units;
			for(var i in units) {
				appendUnitCommand(units[i]);
			}
		});
	});
}

function appendUnitCommand(unit) {
	var type = unitTypes[unit[1]];
	var ll = unit[4];
	$('#commands-content').append('<div><span class="clickable" onclick="focusLatLng('+ll[0]+','+ll[1]+');onClickField('+unit[0]+','+unit[2]+')">'+unit[3]+'</span><span>'+type[4]+'</span></div>');
}
