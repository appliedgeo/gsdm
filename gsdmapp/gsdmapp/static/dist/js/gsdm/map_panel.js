    var soilLayer, aoi, selected_shp, pointdata, draw_control, uploadedLayer, geojsonLayer, pointsoutLayer, strataoutLayer, toc, aoi_area, soilmap_wms, soilmap_layer, _strat_size, req;
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        osmAttrib = '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        osm = L.tileLayer(osmUrl, { maxZoom: 18, attribution: osmAttrib }),
        map = new L.Map('map', { center: new L.LatLng(-0.284200, 36.078709), zoom: 4 }),
        drawnItems = L.featureGroup().addTo(map);

     var myGadm = L.geoJSON().addTo(map);

     //console.log(geoserver_link);
     var geoserver_wms = geoserver_link + '/wms';

    var satellite = L.tileLayer('http://www.google.com/maps/vt?lyrs=s,h&x={x}&y={y}&z={z}', {
        //http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}
            attribution: 'google'
        });

    satellite.addTo(map);

    var baseMap = {
        "Google Satellite": satellite
    };

    var overlayMaps = {
    };

    // add layer control

     toc = L.control.layers(baseMap, overlayMaps, { position: 'bottomright', collapsed: false }).addTo(map);


     function abortRun(){
            req.abort();
            waitingDialog.hide();
      }

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

		// update layer control
		toc.removeLayer(drawnItems);
		if(geojsonLayer){
			toc.removeLayer(geojsonLayer);
		}
		toc.addOverlay(drawnItems, "Area of Interest");

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

        if(soilmap != 'select'){

            var _soilmap_label = soilmap.replace(/_/g, ' ');
            _soilmap_label = _soilmap_label.replace('.tif','');
            _soilmap_label = _soilmap_label.charAt(0).toUpperCase() + _soilmap_label.slice(1);


            if(soilmap_layer){
                map.removeLayer(soilmap_layer);
                toc.removeLayer(soilmap_layer);
              }


          // add layer
          soilmap_wms = 'gsdm:' + soilmap;
          soilmap_layer = L.tileLayer.wms(geoserver_wms, {
              layers: soilmap_wms,
              transparent: true,
              format: 'image/png'
          }).addTo(map);


          // set zoom
          map.setView([-0.284200, 36.078709], 4);

           // add toc
          toc.addOverlay(soilmap_layer, _soilmap_label);

    			// enable sampling options
    			//$( "#samplingMethod" ).prop( "disabled", false );
    			$( "#aoiRadios1" ).prop( "disabled", false );
    			$( "#aoiRadios2" ).prop( "disabled", false );
    			$( "#aoiRadios3" ).prop( "disabled", false );

    			$( "#polygon" ).prop( "disabled", false );
    			$( "#rectangle" ).prop( "disabled", false );

				// enable adaptation options
				 $( "#pointfile" ).prop( "disabled", false );
				 $( "#adaptUpload" ).prop( "disabled", false );


          

          //console.log(toc._map);



        } else {


          // remove layer
          if(soilmap_layer){
            map.removeLayer(soilmap_layer);
            toc.removeLayer(soilmap_layer);
          }


        }


    }


    function addWMSlayer(layer_name){
        if(layer_name != 'no wms'){

            var layer_wms = 'gsdm:' + layer_name;

            uploadedLayer =  L.tileLayer.wms(geoserver_wms, {
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
                adaptLayer = L.geoJson(data).addTo(map);
                map.fitBounds(adaptLayer.getBounds());
            });

			if(adaptLayer){
					toc.removeLayer(adaptLayer);
				}
			toc.addOverlay(adaptLayer, "Sample Points");



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
				
				// update layer control
				toc.removeLayer(drawnItems);
				
				if(geojsonLayer){
					toc.removeLayer(geojsonLayer);
				}
				toc.addOverlay(geojsonLayer, "Area of Interest");

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


	function pointsOutgeo(layer_name){
        if(layer_name != 'no wms'){

            var layer_url = '/outputs/vault/' + layer_name;

            $.getJSON(layer_url,function(data){
                // L.geoJson function is used to parse geojson file and load on to map
                pointsoutLayer = L.geoJson(data).addTo(map);
                map.fitBounds(pointsoutLayer.getBounds());
				
				// update layer control
				//toc.removeLayer(drawnItems);
				
				if(pointsoutLayer){
					toc.removeLayer(pointsoutLayer);
				}
				toc.addOverlay(pointsoutLayer, "Output Points");

				
				
            });



        } else {


          // remove layer
          if(pointsoutLayer){
            map.removeLayer(pointsoutLayer);
          }


        }

    }


	function strataOutgeo(layer_name){
        if(layer_name != 'no wms'){

            var layer_url = '/outputs/vault/' + layer_name;

            $.getJSON(layer_url,function(data){
                // L.geoJson function is used to parse geojson file and load on to map
                strataoutLayer = L.geoJson(data).addTo(map);
                map.fitBounds(strataoutLayer.getBounds());
				
				// update layer control
				//toc.removeLayer(drawnItems);
				
				if(strataoutLayer){
					toc.removeLayer(strataoutLayer);
				}
				toc.addOverlay(strataoutLayer, "Output Strata");

				
				
            });



        } else {


          // remove layer
          if(strataoutLayer){
            map.removeLayer(strataoutLayer);
          }


        }

    }

