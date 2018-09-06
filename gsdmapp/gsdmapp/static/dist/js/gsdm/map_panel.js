    // ============
    // Esri-Leaflet
    // ============

    var map = L.map('map', {zoomControl: false}).setView([-0.062119, 38.941891], 6),
      layer = L.esri.basemapLayer('Imagery').addTo(map),
      layerLabels = L.esri.basemapLayer('ImageryLabels').addTo(map);
      //layerLabels = null,
      worldTransportation = L.esri.basemapLayer('ImageryTransportation');   

    var soilLayer;   

    function setBasemap(basemap) {
      if (layer) {
        map.removeLayer(layer);
      }
      if (basemap === 'OpenStreetMap') {
        layer = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
      }
      else {
        layer = L.esri.basemapLayer(basemap);
      }
      map.addLayer(layer);
      if (layerLabels) {
        map.removeLayer(layerLabels);
      }

      if (basemap === 'ShadedRelief' || basemap === 'Oceans' || basemap === 'Gray' || basemap === 'DarkGray' || basemap === 'Imagery' || basemap === 'Terrain') {
        layerLabels = L.esri.basemapLayer(basemap + 'Labels');
        map.addLayer(layerLabels);
      }
        
      // add world transportation service to Imagery basemap
      if (basemap === 'Imagery') {
        worldTransportation.addTo(map);            
      } else if (map.hasLayer(worldTransportation)) {
        // remove world transportation if Imagery basemap is not selected    
        map.removeLayer(worldTransportation);
      }
    }

    L.control.zoom({
      position:'topright'
    }).addTo(map);

    //var searchControl = L.esri.Geocoding.Controls.geosearch({expanded: true, collapseAfterResult: false, zoomToResult: false}).addTo(map);
    var searchControl = L.esri.Geocoding.geosearch({expanded: true, collapseAfterResult: false, zoomToResult: false}).addTo(map);
    
    searchControl.on('results', function(data){ 
      if (data.results.length > 0) {
        var popup = L.popup()
          .setLatLng(data.results[0].latlng)
          .setContent(data.results[0].text)
          .openOn(map);
        map.setView(data.results[0].latlng)
      }
    })

    // create a feature group for Leaflet Draw to hook into for delete functionality
    var drawnItems = L.featureGroup();
    map.addLayer(drawnItems);

    // create a new Leaflet Draw control
    var drawControl = new L.Control.Draw({
         edit: {
             featureGroup: drawnItems
         }
     });

    // add our drawing controls to the map
    map.addControl(drawControl);

    map.on('draw:created', function(e) {
      var type = e.layerType,
        layer = e.layer;

      if (type === 'marker') {
        layer.bindPopup('A popup!');
      }

      drawnItems.addLayer(layer);
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

  