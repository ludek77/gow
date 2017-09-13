var map = null;
var unitTypes = 'empty';
var emptyColor = 'gray';
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

function openDialog(url, handler) {
	$.get(url, function(data) {
		$('#dialog').html(data);
		if(handler != null) handler();
		$('#dialog').dialog();
	});
}

function closeDialog() {
	$('#dialog').dialog('close');
}

function renderPath(lat1,lng1,lat2,lng2, pk1, pk2) {
	L.polyline([[lat1,lng1],[lat2,lng2]], {color: emptyColor, opacity:0.5, className: 'p-id-'+pk1+'-'+pk2}).addTo(map);
	L.polyline([[lat1,lng1+360],[lat2,lng2+360]], {color: emptyColor, opacity:0.5, className: 'p-id-'+pk1+'-'+pk2}).addTo(map);
}

function renderField(lat, lng, pk) {
	L.circle([lat,lng], 50000, {color: emptyColor, className: 'f-id-'+pk}).on('click', function(e){
		onClickField(e,pk);
	}).addTo(map);
	L.circle([lat,lng+360], 50000, {color: emptyColor, className: 'f-id-'+pk}).on('click', function(e){
		onClickField(e,pk);
	}).addTo(map);
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

function renderCity(lat, lng, fpk, clr) {
	L.rectangle([[lat-1.5,lng-2],[lat+1.5,lng+2]], {
		color: clr,
		fillColor: clr,
		fillOpacity: 0.5,
		className: 'c-id-'+fpk
	}).on('click', function(e){
		onClickField(e,fpk);
	}).addTo(map);
	L.rectangle([[lat-1.5,lng-2+360],[lat+1.5,lng+2+360]], {
		color: clr,
		fillColor: clr,
		fillOpacity: 0.5,
		className: 'c-id-'+fpk
	}).on('click', function(e){
		onClickField(e,fpk);
	}).addTo(map);
}

function centerMap() {
	var b = map.getBounds();
    var minll = b.getWest();
    var c = map.getCenter();
    if(minll < -180) c.lng += 360;
   	if(minll > 180) c.lng -= 360;
   	if(c.lng != map.getCenter().lng) {
   		map.setView(c, map.getZoom());
   	}
}

function resizeIcons() {
	var currentZoom = map.getZoom();
	var multip = 2;
	for(var i = 5; i > currentZoom; i--) {
		multip /= 2;
	}
	$('.leaflet-marker-icon').each(function(index,item){
		var width = 0;
		var height = 0;
		var classList = item.className.split(/\s+/);
		for(var i = 0; i < classList.length; i++) {
			if(classList[i].startsWith('u-id-')) {
				var id = classList[i].substring(5);
				width = unitTypes[id][2];
				height = unitTypes[id][3];
				break;
			}
		}
		$(item).css('width', width*multip).css('margin-left',-(width*multip/2)).css('margin-top',-height*multip/2);
	});
}

function renderUnit(lat, lng, upk, fpk, clr, uType) {
	var markerIcon = L.icon({
	    iconUrl: unitTypes[uType][1],
	    iconAnchor: [unitTypes[uType][2]/2, unitTypes[uType][3]/2],
	    className: 'u-id-'+uType
	});
	L.marker([lat,lng], {icon: markerIcon}).on('click', function(e){
		onClickField(e,fpk)
	}).addTo(map);
	L.rectangle([[lat+2,lng-1],[lat-2,lng+1]], 
		{color: clr,fillOpacity:1}).addTo(map);
	L.marker([lat,lng+360], {icon: markerIcon}).on('click', function(e){
		onClickField(e,fpk)
	}).addTo(map);
	L.rectangle([[lat+2,lng-1+360],[lat-2,lng+1+360]], 
		{color: clr,fillOpacity:1}).addTo(map);
}

function option(id, text) {
	return '<option value='+id+'>'+text+'</option>';
}

function setOptions(obj, list) {
	obj.html('');
	for(var i in list) {
		obj.append(option(list[i][0],list[i][1]));
	}
}

function renderFieldDialog(json) {
	openDialog('/ui/field_dialog', function() {
		$('#unit-dialog .country').text(json.country);
		$('#unit-dialog .unitType').text(json.type);
		$('#unit-dialog .field').text(json.field);
		commandArgs = [];
		if(json.cmds && json.cmd) {
			for(var i = 0; i < json.cmd[2].length; i++) {
				commandArgs[i] = json.cmd[2][i][0];
			}
			$('#unit-dialog .owner-only').show();
			setOptions($('#unit-command'), json.cmds);
			$('#unit-command').val(json.cmd[0]);
			setupUnitDialog(json.cmd[1],json.cmd[2]);
		} else {
			$('#unit-dialog .owner-only').hide();
			$('#unit-command').html('');
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
		
		$.get('country_setup',function(data){
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
	$('#commands-content').append('<div><span class="clickable" onclick="onClickField('+unit[0]+','+unit[2]+')">'+unit[3]+'</span><span>'+type[4]+'</span></div>');
}
