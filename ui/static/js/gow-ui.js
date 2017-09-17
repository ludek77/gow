var map = null;
var emptyColor = 'gray';

function openDialog(url, title, handler) {
	$.get(url, function(data) {
		$('#dialog').html(data);
		if(handler != null) handler();
		$('#dialog').dialog('option', 'title', title);
		$('#dialog').dialog();
	});
}

function closeDialog() {
	$('#dialog').dialog('close');
}

function renderPathElement(lat1,lng1,lat2,lng2, pk1, pk2) {
	L.polyline([[lat1,lng1],[lat2,lng2]], {color: emptyColor, opacity:0.5, className: 'p-id-'+pk1+'-'+pk2}).addTo(map);
}

function renderPathElements(lat1, lng1, lat2, lng2, pk1, pk2) {
	if(lng2 - lng1 > 180) renderPathElement(lat1, lng1, lat2, lng2-360, pk1, pk2);
	else renderPathElement(lat1, lng1, lat2, lng2, pk1, pk2);
}

function renderPath(lat1, lng1, lat2, lng2, pk1, pk2) {
	var tmp = null;
	if(lng2 < lng1) {
		tmp = lat1; lat1 = lat2; lat2 = tmp;
		tmp = lng1; lng1 = lng2; lng2 = tmp;
	}
	renderPathElements(lat1, lng1, lat2, lng2, pk1, pk2);
	if(lng2 > 180) renderPathElements(lat1, lng1-360, lat2, lng2-360, pk1, pk2);
	if(lng1 < 180) renderPathElements(lat1, lng1+360, lat2, lng2+360, pk1, pk2);
}

function renderFieldElement(lat ,lng ,pk) {
	L.circle([lat,lng], 50000, {color: emptyColor, className: 'f-id-'+pk}).on('click', function(e){
		onClickField(e,pk);
	}).addTo(map);
}

function renderField(lat, lng, pk) {
	renderFieldElement(lat, lng, pk);
	if(lng > 180) renderFieldElement(lat, lng-360, pk);
	if(lng < 180) renderFieldElement(lat, lng+360, pk);
}

function renderCityElement(lat, lng, fpk, clr) {
	L.rectangle([[lat-1.5,lng-2],[lat+1.5,lng+2]], {
		color: clr,
		fillColor: clr,
		fillOpacity: 0.5,
		className: 'c-id-'+fpk
	}).on('click', function(e){
		onClickField(e,fpk);
	}).addTo(map);
}

function renderCity(lat, lng, fpk, clr) {
	renderCityElement(lat, lng, fpk, clr);
	if(lng > 180) renderCityElement(lat, lng-360, fpk, clr);
	if(lng < 180) renderCityElement(lat, lng+360, fpk, clr);
}

function renderUnitElement(lat, lng, upk, fpk, clr, markerIcon) {
	L.marker([lat,lng], {icon: markerIcon}).on('click', function(e){
		onClickField(e,fpk)
	}).addTo(map);
	L.rectangle([[lat+2,lng-1],[lat-2,lng+1]], 
		{color: clr,fillOpacity:1}).addTo(map);
}

function renderUnit(lat, lng, upk, fpk, clr, uType) {
	var markerIcon = L.icon({
	    iconUrl: unitTypes[uType][1],
	    iconAnchor: [unitTypes[uType][2]/2, unitTypes[uType][3]/2],
	    className: 'u-id-'+uType
	});
	renderUnitElement(lat, lng, upk, fpk, clr, markerIcon);
	if(lng > 180) renderUnitElement(lat, lng-360, upk, fpk, clr, markerIcon);
	if(lng < 180) renderUnitElement(lat, lng+360, upk, fpk, clr, markerIcon);
}

function focusLatLng(lat, lng) {
	map.setView([lat,lng], map.getZoom());
}

function centerMap() {
    var c = map.getCenter();
    if(c.lng < 0) c.lng += 360;
   	if(c.lng > 360) c.lng -= 360;
   	if(c.lng != map.getCenter().lng) {
   		focusLatLng(c.lat, c.lng);
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