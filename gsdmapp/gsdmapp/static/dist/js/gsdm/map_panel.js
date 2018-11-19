    var soilLayer, aoi, selected_shp, pointdata, draw_control, uploadedLayer;
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: osmAttrib }),
        map = new L.Map('map', { center: new L.LatLng(-0.284200, 36.078709), zoom: 6 }),
        drawnItems = L.featureGroup().addTo(map);

     var myGadm = L.geoJSON().addTo(map);

    var satellite = L.tileLayer('http://www.google.com/maps/vt?lyrs=s,h&x={x}&y={y}&z={z}', {
        //http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}
            attribution: 'google'
        });

    satellite.addTo(map);
	
	var soc_layer = L.tileLayer.wms('http://data.isric.org/geoserver/sg250m/wms', {
              layers: 'sg250m:ORCDRC_M_sl4_250m',
              transparent: true,
              format: 'image/png'
          }); //.addTo(map);
	
	
    
    L.control.layers({
        'Satellite': satellite.addTo(map)
            }, { 'Area of Interest': drawnItems, 'Soil Organic Carbon': soc_layer }, { position: 'bottomright', collapsed: false }).addTo(map);
    


    // draw polygon tool


    function drawPolygon(){
            var polygonDrawer = new L.Draw.Polygon(map);
            polygonDrawer.enable();
        }


     function drawRectangle(){
            var rectangleDrawer = new L.Draw.Rectangle(map);
            rectangleDrawer.enable();
        }

    map.on(L.Draw.Event.CREATED, function (event) {
		// clear previous drawn aoi
		drawnItems.clearLayers();

        var layer = event.layer;

        drawnItems.addLayer(layer);

        aoi = layer.toGeoJSON();

        //console.log(JSON.stringify(aoi));
        
    });

    map.zoomControl.setPosition('topright');

    function setSoilRaster(soilmap) {

        if(soilmap == 'soc_reproj21.tif'){
          // add layer
          soilLayer = L.tileLayer.wms('http://45.33.28.192:8080/geoserver/wms', {
              layers: 'gsdm:soc',
              transparent: true,
              format: 'image/png'
          }).addTo(map);

          // set zoom
          map.setView([-0.284200, 36.078709], 6)

        } else {


          // remove layer
          if(soilLayer){
            map.removeLayer(soilLayer);
          }


        }


    }


    function addWMSlayer(layer_name){
        if(layer_name != 'no wms'){

            var layer_wms = 'gsdm:' + layer_name;

            uploadedLayer =  L.tileLayer.wms('http://localhost:8080/geoserver/wms', {
              layers: layer_wms,
              transparent: true,
              format: 'image/png'
          }).addTo(map);

        } else {


          // remove layer
          if(uploadedLayer){
            map.removeLayer(uploadedLayer);
          }


        }

    }

