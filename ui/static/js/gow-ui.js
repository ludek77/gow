var map = null;
var emptyColor = 'gray';

function openDialog(url, title, handler) {
	$.get(url, function(data) {
		$('#dialog').html(data);
		$('#dialog').attr('title', title);
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

function option(id, text) {
	return '<option value='+id+'>'+text+'</option>';
}

function setOptions(obj, list) {
	obj.html('');
	for(var i in list) {
		obj.append(option(list[i][0],list[i][1]));
	}
}
