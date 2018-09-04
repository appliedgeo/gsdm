    // ============
    // Esri-Leaflet
    // ============

    var map = L.map('map', {zoomControl: false}).setView([-0.062119, 38.941891], 6),
      layer = L.esri.basemapLayer('Imagery').addTo(map),
      layerLabels = L.esri.basemapLayer('ImageryLabels').addTo(map);
      //layerLabels = null,
      worldTransportation = L.esri.basemapLayer('ImageryTransportation');      

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

function setSoilRaster(soilmap) {

     var soilLayer = L.tileLayer.wms('http://localhost:8080/geoserver/wms', {
        layers: 'gsdm:soc',
        transparent: true,
        format: 'image/png'
    }).addTo(map);
    

}

  