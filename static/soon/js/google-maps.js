// google maps

// 2014 snazzymaps, customized by ex-nihilo
//
// When the window has finished loading create our google map below
        google.maps.event.addDomListener(window, 'load', init);

        function init() {
        // Basic options for a simple Google Map
        // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
        var mapOptions = {
            // How zoomed in you want the map to start at (always required)
            zoom: 5,
            disableDefaultUI: true,
            draggable: false,
            streetViewControl: false,
            scrollwheel: false,
            // The latitude and longitude to center the map (always required)
			
			// YOUR POSITION 1
            center: new google.maps.LatLng(23.2500, 77.4170), // EDIT THIS PART
			
            // How you would like to style the map. 
            // This is where you would paste any style found on Snazzy Maps.
            styles: [{
                "stylers": [{
                    "visibility": "off"
                }]
            }, {
                "featureType": "landscape",
                "elementType": "geometry",
                "stylers": [{
                    "visibility": "on"
                }, {
                    "hue": "#ffffff"
                }, {
                    "saturation": -100
                }, {
                    "lightness": 100
                }]
            }, {
                "featureType": "water",
                "stylers": [{
                    "visibility": "on"
                }, {
                    "lightness": -35
                }, {
                    "saturation": -85
                }]
            }, {
                "featureType": "administrative.province",
                "elementType": "geometry",
                "stylers": [{
                    "visibility": "on"
                }]
            }, {
                "featureType": "administrative.country",
                "elementType": "geometry",
                "stylers": [{
                    "visibility": "on"
                }]
            }, {
                "featureType": "water",
                "elementType": "labels",
                "stylers": [{
                    "visibility": "off"
                }]
            }, {
                "featureType": "road.local",
                "elementType": "geometry.fill",
                "stylers": [{
                    "visibility": "off"
                }, {
                    "color": "#000000"
                }, {
                    "lightness": 90
                }]
            }]
        };
        // Get the HTML DOM element that will contain your map 
        // We are using a div with id="map" seen below in the <body>
        var mapElement = document.getElementById('map');
        // Create the Google Map using our element and options defined above
        var map = new google.maps.Map(mapElement, mapOptions);
        // var image = 'map-location.png';
        var circle = {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: 'blue',
			fillOpacity: 1.0,
			scale: 1,
            strokeColor: 'blue',
			strokeOpacity: 1.0,
            strokeWeight: 1
        };
        // Let's also add a marker while we're at it
        var marker = new google.maps.Marker({
			
			// YOUR POSITION 1-1
            position: new google.maps.LatLng(23.2500, 77.4170), // EDIT THIS PART
			
            map: map,
            // icon: image,
            icon: circle,
            title: 'Oxlip'
        });
    }