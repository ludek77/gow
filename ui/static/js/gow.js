var map = null;
var unitTypes = 'empty';
var emptyColor = 'gray';

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

//clicking on map
/*var popup = L.popup();
function onClickMap(e) {
	popup.setLatLng(e.latlng)
		.setContent("Map clicked [" + e.latlng.toString() + "]")
		.openOn(map);
}
map.on('click', onClickMap);*/

function openDialog(title, text) {
	$('#dialog').html(text).prop('title', title).dialog();
}

function addPath(lat, lng) {
	L.polyline([lat,lng], {color: emptyColor, opacity:0.5}).addTo(map);
}

function addField(latlng, pk) {
	L.circle(latlng, 50000, {color: emptyColor}).on('click', function(e){onClickField(e,pk)}).addTo(map);
}

function onClickField(e,pk) {
	openDialog('Field ', pk+' clicked');
}

function addCity(latlng, pk, clr) {
	L.circle(latlng, 150000, {
		color: clr,
		fillColor: clr,
		fillOpacity: 0.5
	}).on('click', function(e){onClickCity(e,pk)}).addTo(map);
}

function onClickCity(e,pk) {
	openDialog('City ', pk+' clicked');
}

function addUnit(latlng, pk, clr, uType) {
	var markerIcon = L.icon({
	    iconUrl: unitTypes[uType],
	    iconAnchor: [12, 63]
	});
	L.marker(latlng, {icon: markerIcon}).on('click', function(e){onClickUnit(e,pk)}).addTo(map);
	L.rectangle([[latlng[0]+4,latlng[1]-1],[latlng[0],latlng[1]+1]], 
		{color: clr,fillOpacity:1}).addTo(map);
}

function onClickUnit(e,pk) {
	openDialog('Unit ', pk+' clicked');
}

function setupGameList(selectedGame) {
	$.get('game_list',function(data){
		var json = $.parseJSON(data);
		for(var i in json) {
		     var id = json[i].id;
		     var name = json[i].name;
		     $('#select-game').append('<option value='+id+'>'+name+'</option>');
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
			unitTypes[json.unitTypes[i][0]] = json.unitTypes[i][1];
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