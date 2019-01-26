$(document).ready(function(){

     $('.glyphicon-question-sign').tooltip({trigger:'click',placement:'bottom'});

      // Basemap changed
      $("#selectStandardBasemap").on("change", function(e) {
        setBasemap($(this).val());
      });



	//$('#samplingStratsize').attr('title', 'Processing will take a very long time');
	//$('#samplingStratsize').tooltip('show'); 


      // load soil maps
      function loadSoilmaps(){
            $.ajax({
                  type: "GET",
                  contentType: "application/json",
                  url: '/soilmaps/',
                  //async: false,
                  dataType: "json",
                  success: function(data){

                       var soil_maps = data.soil_maps;

                       $.each(soil_maps, function (i, soilmap){

                            soilmap = soilmap.replace('gsdm:',''); 
                            var soilmap_label = soilmap.replace(/_/g, ' ');
                            soilmap_label = soilmap_label.replace('.tif','');

                            soilmap_label = soilmap_label.charAt(0).toUpperCase() + soilmap_label.slice(1);

                            $('#samplingSoil').append($('<option>', {
                                value: soilmap,
                                text: soilmap_label
                            }));



                        });




                  }
              });
      }   

      loadSoilmaps();

      // load gadm countries
      function loadGadm(){
            $.ajax({
                  type: "GET",
                  contentType: "application/json",
                  url: '/gadm/',
                  //async: false,
                  dataType: "json",
                  //data: JSON.stringify(samplingdata),
                  success: function(data){

                       var countries = data.countries;

                       $.each(countries, function (i, country){

                            $('#level0').append($('<option>', {
                                value: country,
                                text: country
                            }));



                        });




                  }
              });
      }

      loadGadm();

      // load gadm level 1 areas
      $("#level0").on("change", function(e) {
        var country = $(this).val();

        var _url = '/level1/' + country;

        waitingDialog.show('Loading Country boundary<img src="/static/dist/images/spinner.gif" height="96" width="96">');
		

            $.ajax({
                  type: "GET",
                  contentType: "application/json",
                  url: _url,
                  //async: false,
                  dataType: "json",
                  //data: JSON.stringify(samplingdata),
                  success: function(data){

                        waitingDialog.hide();

                       $('#level1').empty().append('<option selected value="select">Level 1</option>');
                       $('#level2').empty().append('<option selected value="select">Level 2</option>');

                       var level1 = data.level1;

                       $.each(level1, function (i, area){

                            $('#level1').append($('<option>', {
                                value: area,
                                text: area
                            }));


                        });

                        myGadm.clearLayers();

                        var boundary = data.boundary;
                        myGadm.addData(boundary);

                        map.fitBounds(myGadm.getBounds());

						// update layer control
						toc.removeLayer(drawnItems);
 						
						if(geojsonLayer){
							toc.removeLayer(geojsonLayer);
						}
 						toc.removeLayer(myGadm);
 						toc.addOverlay(myGadm, "Area of Interest");



                  }
              });



      });


          // load gadm level 2 areas
      $("#level1").on("change", function(e) {
        var level1 = $(this).val();

        var _url = '/level2/' + level1;

        waitingDialog.show('Loading Level 1 boundary<img src="/static/dist/images/spinner.gif" height="96" width="96">');

            $.ajax({
                  type: "GET",
                  contentType: "application/json",
                  url: _url,
                  //async: false,
                  dataType: "json",
                  //data: JSON.stringify(samplingdata),
                  success: function(data){

                        waitingDialog.hide();

                       $('#level2').empty().append('<option selected value="select">Level 2</option>');

                       var level2 = data.level2;

                       $.each(level2, function (i, area){

                            $('#level2').append($('<option>', {
                                value: area,
                                text: area
                            }));



                        });

                        myGadm.clearLayers();

                        var boundary = data.boundary;
                        myGadm.addData(boundary);

                        map.fitBounds(myGadm.getBounds());

						// update layer control
						toc.removeLayer(drawnItems);

						if(geojsonLayer){
                        	toc.removeLayer(geojsonLayer);
						}
                        toc.removeLayer(myGadm);
                        toc.addOverlay(myGadm, "Area of Interest");


                  }
              });



      });

                // load gadm level 2 geojson
      $("#level2").on("change", function(e) {
        var level2 = $(this).val();

        var _url = '/level3/' + level2;

            waitingDialog.show('Loading Level 2 boundary<img src="/static/dist/images/spinner.gif" height="96" width="96">');

            $.ajax({
                  type: "GET",
                  contentType: "application/json",
                  url: _url,
                  //async: false,
                  dataType: "json",
                  //data: JSON.stringify(samplingdata),
                  success: function(data){

                        waitingDialog.hide();

                        myGadm.clearLayers();

                        var boundary = data.boundary;
                        myGadm.addData(boundary);

                        map.fitBounds(myGadm.getBounds());

						// update layer control
						toc.removeLayer(drawnItems);
						
						if(geojsonLayer){
                        	toc.removeLayer(geojsonLayer);
						}
                        toc.removeLayer(myGadm);
                        toc.addOverlay(myGadm, "Area of Interest");
 
   						//console.log(boundary.coordinates[0]);
   						// aoi area
   						var aoi_geo = L.polygon(boundary.coordinates[0]);	
   						aoi_area = L.GeometryUtil.geodesicArea(aoi_geo.getLatLngs()[0]);
                    				
   						var _strat_size = Math.sqrt(aoi_area)/10;
 	              		_strat_size = Math.trunc(_strat_size);
                   		$('#samplingStratsize').val(_strat_size);


                        $( "#samplingMethod" ).prop( "disabled", false );
						
                  }
              });



      });

      // soil raster changed

      $("#samplingSoil").on("change", function(e) {
        setSoilRaster($(this).val());
        
      });

      $("#adaptSoil").on("change", function(e) {
        setSoilRaster($(this).val());
      });

      // sampling method changed
      $("#samplingMethod").on("change", function(e) {
        var _method = $(this).val();
        if(_method == 'stratrand' || _method == 'stratdir'){
          $( "#samplingStratsize" ).prop( "disabled", false );
          $( "#samplingDistance" ).prop( "disabled", false );
          $( "#samplingEdge" ).prop( "disabled", false );
          $( "#samplingCriterium" ).prop( "disabled", false );
          $( "#samplingRun" ).prop( "disabled", false );

        } else if(_method == 'grid'){
          $( "#samplingStratsize" ).prop( "disabled", false );
          $( "#samplingEdge" ).prop( "disabled", false );
          $( "#samplingRun" ).prop( "disabled", false );

          $( "#samplingCriterium" ).prop( "disabled", true );
          $( "#samplingDistance" ).prop( "disabled", true );

        } else if(_method == 'dir'){
          $( "#samplingDistance" ).prop( "disabled", false );
          $( "#samplingEdge" ).prop( "disabled", false );
          $( "#samplingCriterium" ).prop( "disabled", false );
          $( "#samplingRun" ).prop( "disabled", false );


           $('#samplingStratsize').val('0');
          $( "#samplingStratsize" ).prop( "disabled", true );

        } else {
          alert('Select a Sampling Algorithm');
           $('#samplingStratsize').val('0');
           $( "#samplingStratsize" ).prop( "disabled", true );
          $( "#samplingDistance" ).prop( "disabled", true );
          $( "#samplingEdge" ).prop( "disabled", true );
          $( "#samplingCriterium" ).prop( "disabled", true );
          $( "#samplingRun" ).prop( "disabled", true );
        }

      });


      // draw polygon tool
      $("#polygon").click(function(){
            drawPolygon();
      });


      // draw rectangle tool
      $("#rectangle").click(function(){
            drawRectangle();
      });


      // delete polygon tool
      $("#delete").click(function(){
            drawnItems.clearLayers();
      });


      function disableDrawing(){
            $('#polygon').prop("disabled", true);
            $('#rectangle').prop("disabled", true);
            drawnItems.clearLayers();

      }

      function enableDrawing(){
            $('#polygon').prop("disabled", false);
            $('#rectangle').prop("disabled", false);

      }


        // clear selections on tool change
	function clearPanels(){
      
			// sampling design 
             $("#samplingSoil").val("select");

             $("#samplingMethod").val("select");

              $('#shapefile').val('');

               $( "#uploadfiles ul" ).empty();

             $('#samplingStratsize').val('');

             $('#samplingDistance').val('');

             $('#samplingEdge').val('');

             $('#samplingCriterium').val('');

             $('#samplingOutput').val('');

             drawnItems.clearLayers();

 			
			// local map adaptation

                $('#pointfile').val('');

                 $( "#uploadfiles2 ul" ).empty();

             $("#adaptSoil").val("select");

              $('#adaptAttribute').val("select");

             $('#adaptXcol').val("select");

             $('#adaptYcol').val("select");

             $('#adaptEpsg').val('');

             $('#adaptOutput').val('');

		// map
		if(soilLayer){
            map.removeLayer(soilLayer);
          }

		map.setView([-0.284200, 36.078709], 4)

     
	}

$('#collapseSettings a[data-toggle="tab"]').bind('click', function (e) {
            //clearPanels();
        });







      // run sampling design
      $( "#samplingRun" ).click(function(e) {

          //console.log(aoi);


          //var polygon = JSON.stringify(aoi);
          var aoi_method = $("input[name='aoiRadios']:checked").val();

          if(aoi_method == 'draw'){
              // run sampling for drawn area

              var soil_raster = $("#samplingSoil").val();
              var method = $("#samplingMethod").val();
              var strat_size = $("#samplingStratsize").val();
              var min_dist = $("#samplingDistance").val();
              var edge = $("#samplingEdge").val();
              var criterium = $("#samplingCriterium").val();
              //var output = $("#samplingOutput").val();

              var _url = '/samplingdraw/';

              var samplingdata = {
                "aoi": aoi,
                "soil_raster": soil_raster,
                "method": method,
                "strat_size": strat_size,
                "min_dist": min_dist,
                "edge": edge,
                "criterium": criterium
                //"output": output

              };

                var dialog_content = 'Sampling Design running<img src="/static/dist/images/spinner.gif" height="96" width="96">';
                dialog_content += '<button id="stopRun" type="button" class="btn btn-primary btn-block" onclick="abortRun()">Cancel</button>';

                waitingDialog.show(dialog_content);

              $.ajax({
                  type: "POST",
                  contentType: "application/json",
                  url: _url,
                  //async: false,
                  dataType: "json",
                  data: JSON.stringify(samplingdata),
                  success: function(data){

                       //console.log(data.shapefile);
                       waitingDialog.hide();

						//alert('Sampling Design Complete!');

                        $( "#outfiles p" ).empty();

                       var outfile = '<p>Download: <a href=/outputs/'+data.samplingout+'>'+data.samplingout+'</a></p>'

                       $( "#outfiles" ).append(outfile);
	
						alert('Sampling Design complete!');

						pointsOutgeo(data.pointsout);
                        strataOutgeo(data.strataout);



                  }
              });


          } else {

               // run sampling for uploaded shapefile
              var _url = '/samplingshp/';

              var samplingdata = {
                "shp": selected_shp,
                "soil_raster": $("#samplingSoil").val(),
                "method": $("#samplingMethod").val(),
                "strat_size": $("#samplingStratsize").val(),
                "min_dist": $("#samplingDistance").val(),
                "edge": $("#samplingEdge").val(),
                "criterium": $("#samplingCriterium").val(),
                "output": $("#samplingOutput").val()

              };
                //alert('Running..');
                var dialog_content = 'Sampling Design running<img src="/static/dist/images/spinner.gif" height="96" width="96">';
                dialog_content += '<button id="stopRun" type="button" class="btn btn-primary btn-block" onclick="abortRun()">Cancel</button>';

                waitingDialog.show(dialog_content);

              req = $.ajax({
                  type: "POST",
                  contentType: "application/json",
                  url: _url,
                  //async: false,
                  dataType: "json",
                  data: JSON.stringify(samplingdata),
                  success: function(data){

                        waitingDialog.hide();

						          //alert('Sampling Design complete!');

                        $( "#outfiles p" ).empty();

                       var outfile = '<p>Download: <a href=/outputs/'+data.samplingout+'>'+data.samplingout+'</a></p>'

                       $( "#outfiles" ).append(outfile);

						alert('Sampling Design complete!');

						pointsOutgeo(data.pointsout);
						strataOutgeo(data.strataout);



                  }
              });



          }



      });




        // run local map adaptation
      $("#adaptRun").click(function(e){

            var soil_raster = $("#samplingSoil").val();
            var attribute = $("#adaptAttribute").val();
            var xcolumn = $("#adaptXcol").val();
            var ycolumn = $("#adaptYcol").val();
            //var epsg = $("#adaptEpsg").val();
            //var _output = $("#adaptOutput").val();


            var adaptationdata = {
                "pointdata": pointdata,
				"aoidata": selected_shp,
                "soil_raster": soil_raster,
                "attribute": attribute,
                "xcolumn": xcolumn,
                "ycolumn": ycolumn
                //"epsg": epsg,
                //"output": _output

              };


            var dialog_content = 'Local Map Adaptation running<img src="/static/dist/images/spinner.gif" height="96" width="96">';
                dialog_content += '<button id="stopRun" type="button" class="btn btn-primary btn-block" onclick="abortRun()">Cancel</button>';

                waitingDialog.show(dialog_content);

            var _url = '/localadapt/';

            $.ajax({
                  type: "POST",
                  contentType: "application/json",
                  url: _url,
                  //async: false,
                  dataType: "json",
                  data: JSON.stringify(adaptationdata),
                  success: function(data){

                        waitingDialog.hide();

						alert('Local map adaptation complete!');

                       //console.log(data.feedback.length);
                       var feedback = data.feedback;
                       var evaluation = data.evaluation;


                       $( "#outfiles p" ).empty();

                       var outfile = '<p>Download: <a href=/outputs/'+data.adaptout+'>'+data.adaptout+'</a></p>'

                       $( "#outfiles" ).append(outfile);

                       // display feedback stats
                       $('#feedback').empty();

                       var feedback_table = '<h2>Feedback</h2>';
                       feedback_table += '<table class="table table-bordered"><thead>';
                       feedback_table += '<tr><th>Test</th><th>Value</th></tr></thead>';
                        feedback_table += '<tbody>';
                        feedback_table += '<tr><td>No of point observation data</td><td>'+feedback[0]+'</td></tr>';
                        feedback_table += '<tr><td>No of NA point observation data</td><td>'+feedback[1]+'</td></tr>';
                        feedback_table += '<tr><td>Number of point observation data within the mapping area</td><td>'+feedback[2]+'</td></tr>';
                        feedback_table += '<tr><td>Number of point locations without map data</td><td>'+feedback[3]+'</td></tr>';
                        feedback_table += '<tr><td>Number of used point observation data</td><td>'+feedback[4]+'</td></tr>';
                        feedback_table += '</tbody></table>';

                        $('#feedback').append(feedback_table);


                        // display evaluation stats
                         $('#evaluation').empty();
                         var evaluation_table = '<h2>Evaluation</h2>';
                         evaluation_table += '<table class="table table-bordered"><thead>';
                         evaluation_table += '<tr><th>Measure</th><th>MAE</th><th>RMSE</th><th>E</th><th>r2</th><th>ME</th></tr></thead>';
                         evaluation_table += '<tbody>';
                         evaluation_table += '<tr><td>map</td><td>'+evaluation[0][0]+'</td><td>'+evaluation[0][1]+'</td><td>'+evaluation[0][2]+'</td><td>'+evaluation[0][3]+'</td><td>'+evaluation[0][4]+'</td></tr>';
                         evaluation_table += '<tr><td>ordkrig_cv</td><td>'+evaluation[1][0]+'</td><td>'+evaluation[1][1]+'</td><td>'+evaluation[1][2]+'</td><td>'+evaluation[1][3]+'</td><td>'+evaluation[1][4]+'</td></tr>';
                         evaluation_table += '<tr><td>reskrig_cv</td><td>'+evaluation[2][0]+'</td><td>'+evaluation[2][1]+'</td><td>'+evaluation[2][2]+'</td><td>'+evaluation[2][3]+'</td><td>'+evaluation[2][4]+'</td></tr>';
                         evaluation_table += '<tr><td>regkrig_cv</td><td>'+evaluation[3][0]+'</td><td>'+evaluation[3][1]+'</td><td>'+evaluation[3][2]+'</td><td>'+evaluation[3][3]+'</td><td>'+evaluation[3][4]+'</td></tr>';
                         evaluation_table += '</tbody></table>';

                         $('#evaluation').append(evaluation_table);


                  }
              });






      });




      $('input[name="aoiRadios"]').change(function(){
          
			var aoi_method = $("input[name='aoiRadios']:checked").val();
		
			if(aoi_method == 'draw'){
				$("#aoi_shp").hide();
				$("#aoi_gadm").hide();

				// clear gadm areas
				myGadm.clearLayers();
        if(geojsonLayer){
            map.removeLayer(geojsonLayer);
                }

				$('#level1').empty().append('<option selected value="select">Level 1</option>');
				$('#level2').empty().append('<option selected value="select">Level 2</option>');

                // disable shape uploads
                 $( "#shapefile" ).prop( "disabled", true );
                 $( "#samplingUpload" ).prop( "disabled", true ); 
                  $( "#uploadfiles ul" ).empty();

                  enableDrawing();

			} 
			else if(aoi_method == 'shapefile'){
				$("#aoi_shp").show();
				$("#aoi_gadm").hide();

				// clear gadm areas
				myGadm.clearLayers();
				if(geojsonLayer){
                   map.removeLayer(geojsonLayer);
                }

				$('#level1').empty().append('<option selected value="select">Level 1</option>');
				$('#level2').empty().append('<option selected value="select">Level 2</option>');

                // enable shape uploads
                 $( "#shapefile" ).prop( "disabled", false );
                 $( "#samplingUpload" ).prop( "disabled", false );
  
                 disableDrawing();

			}
			else {
				$("#aoi_shp").hide();
				disableDrawing();
				$("#aoi_gadm").show();
				if(geojsonLayer){
                   map.removeLayer(geojsonLayer);
                }
                $( "#uploadfiles ul" ).empty();
			}
			

      });

        // sampling design shapefile upload
        $("#shpupload").submit(function(e){
            //alert("form submitted");
            e.preventDefault();

            waitingDialog.show('Uploading<img src="/static/dist/images/spinner.gif" height="96" width="96">');

            var formdata = new FormData(this);

                $.ajax({
                    url: "/uploads/samplingdata/",
                    type: "POST",
                    data: formdata,
                    mimeTypes:"multipart/form-data",
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function(data){
                        //console.log(data.layer_wms);

                        waitingDialog.hide();

						          alert('Upload complete!');

          						// clear previous upload
          						$( "#uploadfiles ul" ).empty();

                      selected_shp = data.url;

                      var _file = '<li>'+data.url+'</li>';
                      $( "#uploadfiles ul" ).append(_file);

                      addGeo_aoilayer(data.layer_wms);

                      $( "#samplingMethod" ).prop( "disabled", false );

                    },error: function(){
                        waitingDialog.hide();
                        alert("error");
                    }
                 });
         });


          // map adaptation point data upload
         $("#pointupload").submit(function(e){
            //alert("form submitted");
            e.preventDefault();

            waitingDialog.show('Uploading<img src="/static/dist/images/spinner.gif" height="96" width="96">');

            var formdata = new FormData(this);

                $.ajax({
                    url: "/uploads/adaptdata/",
                    type: "POST",
                    data: formdata,
                    mimeTypes:"multipart/form-data",
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function(data){
                        //alert(data.message);

                        waitingDialog.hide();

						          alert('Upload complete');

                        pointdata = data.url;
                        datafields = data.fields;

						// enable adaptation fields
						$( "#adaptAttribute" ).prop( "disabled", false );
						$( "#adaptXcol" ).prop( "disabled", false );
						$( "#adaptYcol" ).prop( "disabled", false );
						$( "#adaptRun" ).prop( "disabled", false );
          						
          						// clear previous upload and data fields
          						$( "#uploadfiles2 ul" ).empty();
          						
          						$('#adaptAttribute').empty().append('<option selected value="select">Select</option>');
          						$('#adaptXcol').empty().append('<option selected value="select">Select</option>');
          						$('#adaptYcol').empty().append('<option selected value="select">Select</option>');

                        //console.log(datafields.length)
                        // list uploaded data
                        var _file = '<li>'+data.url+'</li>';
                        $( "#uploadfiles2 ul" ).append(_file);

                        // display data fields
                        $.each(datafields, function (i, field){

                            $('#adaptAttribute').append($('<option>', {
                                value: field,
                                text: field
                            }));

                             $('#adaptXcol').append($('<option>', {
                                value: field,
                                text: field
                            }));

                             $('#adaptYcol').append($('<option>', {
                                value: field,
                                text: field
                            }));


                        });

                        //addGeolayer(data.layer_wms);

                    },error: function(){
                        waitingDialog.hide();
                        alert("error");
                    }
                 });
         });





          // validate sampling options
          $("#samplingStratsize").on("change", function(e) {
              var stratsize_val = $(this).val();

              if(stratsize_val < (Math.sqrt(aoi_area)/20)){
                  alert('Warning! Processing will take a very long time because the grid size is too small in relation to the size of the area. Consider a larger grid size.');
              }
 
          });


          $("#samplingDistance").on("change", function(e) {
              var distance_val = $(this).val();
              
              if(distance_val > (Math.sqrt(aoi_area)/60)){
                  alert('Warning! Processing may fail because the minimum distance between samples is too large. Make sure the minimum distance is smaller than half of the grid size if a stratification grid is specified.');
              }
          });


          $("#samplingEdge").on("change", function(e) {
              var edge_val = $(this).val();

              if(edge_val > (Math.sqrt(aoi_area)/20)){
                  alert('Warning! Processing may fail because the buffer zone is too wide in relation to the size of the area. Consider setting a smaller value.');
              }


          });


          $("#samplingCriterium").on("change", function(e) {
              var criterium_val = $(this).val();

              if(criterium_val > 4000){
                  alert('Warning! Maximum number of samples allowed is 4000.');
              }
          });
















});
