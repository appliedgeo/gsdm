    var soilLayer, aoi;   
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: osmAttrib }),
        map = new L.Map('map', { center: new L.LatLng(-0.062119, 38.941891), zoom: 6 }),
        drawnItems = L.featureGroup().addTo(map);

    var satellite = L.tileLayer('http://www.google.com/maps/vt?lyrs=s,h&x={x}&y={y}&z={z}', {
        //http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}
            attribution: 'google'
        });

    L.control.layers({
        'Satellite': satellite.addTo(map)
            }, { 'AOI': drawnItems }, { position: 'bottomright', collapsed: false }).addTo(map);

    map.addControl(new L.Control.Draw({
        position: 'topright',
        edit: {
            featureGroup: drawnItems,
            poly: {
                allowIntersection: true
            }
        },
        draw: {
            polygon: {
                allowIntersection: true,
                showArea: true
            },
            marker: false,
            circlemarker: false
        }
    }));

    map.on(L.Draw.Event.CREATED, function (event) {
        var layer = event.layer;

        drawnItems.addLayer(layer);

        aoi = layer.toGeoJSON();

        //console.log(JSON.stringify(aoi));
        
    });


    function setSoilRaster(soilmap) {

        if(soilmap == 'select'){
          // remove layer
          map.removeLayer(soilLayer);

        } else {

            soilLayer = L.tileLayer.wms('http://45.33.28.192:8080/geoserver/wms', {
              layers: 'gsdm:soc',
              transparent: true,
              format: 'image/png'
          }).addTo(map);

        }

         
        

    }