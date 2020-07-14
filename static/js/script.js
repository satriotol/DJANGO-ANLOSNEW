if(!!navigator.geolocation) {
	    	
  var map;
  var geocoder;
  var polygonArray = [];
	var mapOptions = {
		    		zoom: 15,
		    		mapTypeId: google.maps.MapTypeId.ROADMAP
		    	};
	map = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
	navigator.geolocation.getCurrentPosition(function(position) {
	    		
		    		var geolocate = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
		    		
		    		var infowindow = new google.maps.InfoWindow({
		    			map: map,
		    			position: geolocate,
		    			content:
		    				'<h4>Location pinned from HTML5 Geolocation!</h4>' +
		    				'<p>Latitude: ' + position.coords.latitude + '</p>' +
		    				'<p>Longitude: ' + position.coords.longitude + '</p>'
		    		});
		    		
		    		map.setCenter(geolocate);
		    		
	    		});
	    		
} 
else{
  document.getElementById('map_canvas').innerHTML = 'No Geolocation Support.';
}

function initializeDrawer() {
    var drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.POLYGON,
        drawingControl: true,
        drawingControlOptions: {
            position: google.maps.ControlPosition.TOP_CENTER,
            drawingModes: [
            google.maps.drawing.OverlayType.MARKER,
            google.maps.drawing.OverlayType.CIRCLE,
            google.maps.drawing.OverlayType.POLYGON,
            google.maps.drawing.OverlayType.POLYLINE,
            google.maps.drawing.OverlayType.RECTANGLE]
        },
        markerOptions: {
            icon: 'images/car-icon.png'
        },
        circleOptions: {
            fillColor: '#ffff00',
            fillOpacity: 1,
            strokeWeight: 5,
            clickable: false,
            editable: true,
            zIndex: 1
        },
        polygonOptions: {
            fillColor: '#BCDCF9',
            fillOpacity: 0.5,
            strokeWeight: 2,
            strokeColor: '#57ACF9',
            clickable: false,
            editable: false,
            zIndex: 1
        }
    });
    console.log(drawingManager)
    drawingManager.setMap(map)

    google.maps.event.addListener(drawingManager, 'polygoncomplete', function (polygon) {
        document.getElementById('info').innerHTML;
        let vert = polygon.getPath();
        let pos = {
            latitude: [

            ],
            longitude: [

            ]
        }
        for (var i = 0; i < polygon.getPath().getLength(); i++) {
            let xy = vert.getAt(i)
            pos.latitude.push(xy.lat());
            pos.longitude.push(xy.lng());
            document.getElementById('info').innerHTML += JSON.stringify(pos);
        }
        polygonArray.push(polygon);
    });

}

// Initialize the drawer tool
google.maps.event.addDomListener(window, "load", initializeDrawer);