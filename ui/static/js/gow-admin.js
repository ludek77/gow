function addFieldToMap(e) {
	var lat = e.latlng.lat.toFixed(2);
	var lng = e.latlng.lng.toFixed(2);
	openDialog('/ui/field_dialog', function() {
		$('#field-save').click(function(){
			var type = $('#field-type').val();
			var name = $('#field-name').val();
			var isCity = $('#field-iscity').is(':checked');
			saveFieldToMap(lat,lng,type,name,isCity);
		});
	});
}
function saveFieldToMap(lat,lng,type,name,isCity) {
	$.get('field_add?lat='+lat+'&lng='+lng+'&type='+type+'&name='+name+'&isCity='+isCity, function(data) {
		var json = $.parseJSON(data);
		if(json.isCity) {
			addCity([json.lat,json.lng],json.pk,'gray');
		} else {
			addField([json.lat,json.lng],json.pk);
		}
	});
	closeDialog();
}
function deleteFieldFromMap(e,pk) {
	$.get('field_delete?pk='+pk, function(data) {
		$('.f-id-'+pk).hide();
	});
}
var lastField = null;
function addPathToMap(e,pk) {
	if(lastField == null) lastField = pk;
	else {
		$.get('path_add?f1='+lastField+'&f2='+pk, function(data) {
			var json = $.parseJSON(data);
			addPath(json.ll1,json.ll2,json.pk1,json.pk2);
		});
		lastField = null;
	}
}
function deletePathFromMap(e,pk) {
	if(lastField == null) lastField = pk;
	else {
		if(pk > lastField) {
			tmp = pk;
			pk = lastField;
			lastField = tmp;
		}
		$.get('path_delete?f1='+lastField+'&f2='+pk, function(data) {
			alert(data);
			var json = $.parseJSON(data);
			$('path.p-id-'+json.pk1+'-'+json.pk2).hide();
		});
		lastField = null;
	}
}
function configureAddFields()    {mapClickHandler = addFieldToMap;fieldClickHandler = null;}
function configureDeleteFields() {mapClickHandler = null;fieldClickHandler = deleteFieldFromMap;}
function configureAddPaths()     {mapClickHandler = null;fieldClickHandler = addPathToMap;currentField = null;}
function configureDeletePaths()  {mapClickHandler = null;fieldClickHandler = deletePathFromMap;currentField = null;}
