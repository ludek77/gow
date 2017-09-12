var map = null;
var unitTypes = 'empty';
var emptyColor = 'gray';
var iconWidth = 24;

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

function addPath(lat, lng) {
	L.polyline([lat,lng], {color: emptyColor, opacity:0.5}).addTo(map);
}

function addField(latlng, pk) {
	L.circle(latlng, 50000, {color: emptyColor}).on('click', function(e){onClickField(e,pk)}).addTo(map);
}

var fieldClickHandler = null;
function onClickField(e,pk) {
	if(fieldClickHandler != null) fieldClickHandler(e,pk);
}

function addCity(latlng, pk, clr) {
	L.circle(latlng, 150000, {
		color: clr,
		fillColor: clr,
		fillOpacity: 0.5
	}).on('click', function(e){onClickCity(e,pk)}).addTo(map);
}

function displayCity(e,pk) {
	$.get('city_get?c='+pk, function(data) {
		var json = $.parseJSON(data);
		openDialog('/ui/city_dialog', function() {
			$('#city-dialog .country').text(json.country);
			$('#city-dialog .field').text(json.field);
		});
	});
}

var cityClickHandler = displayCity;
function onClickCity(e,pk) {
	if(cityClickHandler != null) cityClickHandler(e,pk);
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
			if(classList[i].startsWith('id-')) {
				var id = classList[i].substring(3);
				width = unitTypes[id][2];
				height = unitTypes[id][3];
				break;
			}
		}
		$(item).css('width', width*multip).css('margin-left',-(width*multip/2)).css('margin-top',-height*multip);
	});
}

function addUnit(latlng, pk, clr, uType) {
	var markerIcon = L.icon({
	    iconUrl: unitTypes[uType][1],
	    iconAnchor: [unitTypes[uType][2]/2, unitTypes[uType][3]],
	    className: 'id-'+uType
	});
	L.marker(latlng, {icon: markerIcon}).on('click', function(e){onClickUnit(e,pk)}).addTo(map);
	L.rectangle([[latlng[0]+4,latlng[1]-1],[latlng[0],latlng[1]+1]], 
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

var selectedUnit=null;

function onClickUnit(e,pk) {
	selectedUnit=pk;
	$.get('unit_get?u='+pk, function(data) {
		var json = $.parseJSON(data);
		openDialog('/ui/unit_dialog', function() {
			$('#unit-dialog .country').text(json.country);
			$('#unit-dialog .unitType').text(json.type);
			$('#unit-dialog .field').text(json.field);
			if(json.cmds) {
				$('#unit-dialog .owner-only').show();
				setOptions($('#unit-dialog #unitCommand'), json.cmds);
				$('#unit-dialog #unitCommand').val(json.cmd);
			} else {
				$('#unit-dialog .owner-only').hide();
				$('#unit-dialog #unitCommand').html('');
			}
		});
	});
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

function setupCommandList() {
	$.get('country_setup',function(data){
		var json= $.parseJSON(data);
		var units = json.units;
		for(var i in units) {
			$('#commands').append(units[i][0]+'.'+unitTypes[units[i][1]]);
		}
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
			addPath(ll1, ll2);
		}
		for(var i in json.fields) {
			var pk = json.fields[i][0];
		    var latlng = json.fields[i][1];
		    var clr = json.fields[i][2];
			if(clr != '') {
				if(clr == '-') clr = 'gray';
				addCity(latlng, pk, clr);
			} else {
		    	addField(latlng, pk);
		    }
		}
		for(var i in json.units) {
			var pk = json.units[i][0];
			var latlng = json.units[i][1];
			var clr = json.units[i][2];
			var type = json.units[i][3];
			addUnit(latlng, pk, clr, type);
		}
		
		setupCommandList();
	});
}