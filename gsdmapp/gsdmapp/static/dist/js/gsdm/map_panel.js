    var soilLayer, aoi, selected_shp, pointdata, draw_control, uploadedLayer, geojsonLayer, toc, aoi_area;
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: osmAttrib }),
        map = new L.Map('map', { center: new L.LatLng(-0.284200, 36.078709), zoom: 4 }),
        drawnItems = L.featureGroup().addTo(map);

     var myGadm = L.geoJSON().addTo(map);

    var satellite = L.tileLayer('http://www.google.com/maps/vt?lyrs=s,h&x={x}&y={y}&z={z}', {
        //http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}
            attribution: 'google'
        });

    satellite.addTo(map);


     var soc_layer = L.tileLayer.wms('http://45.33.28.192:8080/geoserver/wms', {
              layers: 'gsdm:Soil_Carbon_0_30_250m_4326',
              transparent: true,
              format: 'image/png'
          }); //.addTo(map);
	

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

        aoi_area = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
        var _strat_size = Math.sqrt(aoi_area)/10;
        _strat_size = Math.trunc(_strat_size);
        $('#samplingStratsize').val(_strat_size);

        aoi = layer.toGeoJSON();

        //console.log(layer);
        $( "#samplingMethod" ).prop( "disabled", false );
        
    });

    map.zoomControl.setPosition('topright');

    function setSoilRaster(soilmap) {

        if(soilmap == 'Soil_Carbon_0_30_250m_3857.tif'){
          // add layer
          
          soc_layer.addTo(map);

          // set zoom
          map.setView([-0.284200, 36.078709], 4);

          if(!toc){
            toc = L.control.layers({
            'Satellite': satellite.addTo(map)}, 
            { 'Soil Organic Carbon': soc_layer }, 
            { position: 'bottomright', collapsed: false }).addTo(map);

          }
    			// enable sampling options
    			//$( "#samplingMethod" ).prop( "disabled", false );
    			$( "#aoiRadios1" ).prop( "disabled", false );
    			$( "#aoiRadios2" ).prop( "disabled", false );
    			$( "#aoiRadios3" ).prop( "disabled", false );

    			$( "#polygon" ).prop( "disabled", false );
    			$( "#rectangle" ).prop( "disabled", false );

          

          //console.log(toc._map);



        } else {


          // remove layer
          if(soilLayer){
            map.removeLayer(soc_layer);
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

     function addGeolayer(layer_name){
        if(layer_name != 'no wms'){

            var layer_url = '/outputs/' + layer_name;

            $.getJSON(layer_url,function(data){
                // L.geoJson function is used to parse geojson file and load on to map
                geojsonLayer = L.geoJson(data).addTo(map);
                map.fitBounds(geojsonLayer.getBounds());
            });



        } else {


          // remove layer
          if(geojsonLayer){
            map.removeLayer(geojsonLayer);
          }


        }

    }

	 function addGeo_aoilayer(layer_name){
        if(layer_name != 'no wms'){

            var layer_url = '/outputs/' + layer_name;

            $.getJSON(layer_url,function(data){
                // L.geoJson function is used to parse geojson file and load on to map
                geojsonLayer = L.geoJson(data).addTo(map);
                map.fitBounds(geojsonLayer.getBounds());

				// aoi area
				//console.log(data.features[0].geometry.coordinates);
				var aoi_geo = L.polygon(data.features[0].geometry.coordinates);
				aoi_area = L.GeometryUtil.geodesicArea(aoi_geo.getLatLngs()[0]);
        		var _strat_size = Math.sqrt(aoi_area)/10;
        		_strat_size = Math.trunc(_strat_size);
        		$('#samplingStratsize').val(_strat_size);
				
            });



        } else {


          // remove layer
          if(geojsonLayer){
            map.removeLayer(geojsonLayer);
          }


        }

    }

