$(document).ready(function(){

       $('.glyphicon-question-sign').tooltip({trigger:'click',placement:'bottom'});

      // Basemap changed
      $("#selectStandardBasemap").on("change", function(e) {
        setBasemap($(this).val());
      });

      // Search
      var input = $(".geocoder-control-input");
      input.focus(function(){
        $("#panelSearch .panel-body").css("height", "150px");
      });
      input.blur(function(){
         $("#panelSearch .panel-body").css("height", "auto");
      });

      // Attach search control for desktop or mobile
      function attachSearch() {
        var parentName = $(".geocoder-control").parent().attr("id"),
          geocoder = $(".geocoder-control"),
          width = $(window).width();
        if (width <= 767 && parentName !== "geocodeMobile") {
          geocoder.detach();
          $("#geocodeMobile").append(geocoder);
        } else if (width > 767 && parentName !== "geocode"){
          geocoder.detach();
          $("#geocode").append(geocoder);
        }
      }

      $(window).resize(function() {
        attachSearch();
      });

      attachSearch();

      // soil raster changed

      $("#samplingSoil").on("change", function(e) {
        setSoilRaster($(this).val());
      });

      $("#adaptSoil").on("change", function(e) {
        setSoilRaster($(this).val());
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




        // clear selections
        /*
      $("#samplingClear").click(function(){

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

      });


      $("#adaptClear").click(function(){

                $('#pointfile').val('');

                 $( "#uploadfiles2 ul" ).empty();

             $("#adaptSoil").val("select");

              $('#adaptAttribute').val("select");

             $('#adaptXcol').val("select");

             $('#adaptYcol').val("select");

             $('#adaptEpsg').val('');

             $('#adaptOutput').val('');



      });
      */



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
              var output = $("#samplingOutput").val();

              var _url = '/samplingdraw/';

              var samplingdata = {
                "aoi": aoi,
                "soil_raster": soil_raster,
                "method": method,
                "strat_size": strat_size,
                "min_dist": min_dist,
                "edge": edge,
                "criterium": criterium,
                "output": output

              };

                 waitingDialog.show('Sampling Design running..');

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

                       $( "#outfiles ul" ).empty();

                       var outfile = '<li><a href=/outputs/'+data.samplingout+'>'+data.samplingout+'</a></li>'

                       $( "#outfiles ul" ).append(outfile);



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
                waitingDialog.show('Sampling Design running..');

              $.ajax({
                  type: "POST",
                  contentType: "application/json",
                  url: _url,
                  //async: false,
                  dataType: "json",
                  data: JSON.stringify(samplingdata),
                  success: function(data){

                        waitingDialog.hide();

                        $( "#outfiles p" ).empty();

                       var outfile = '<p>Download: <a href=/outputs/'+data.samplingout+'>'+data.samplingout+'</a></p>'

                       $( "#outfiles" ).append(outfile);



                  }
              });



          }



      });


        // run local map adaptation
      $("#adaptRun").click(function(e){

            var soil_raster = $("#adaptSoil").val();
            var attribute = $("#adaptAttribute").val();
            var xcolumn = $("#adaptXcol").val();
            var ycolumn = $("#adaptYcol").val();
            var epsg = $("#adaptEpsg").val();
            var _output = $("#adaptOutput").val();


            var adaptationdata = {
                "pointdata": pointdata,
                "soil_raster": soil_raster,
                "attribute": attribute,
                "xcolumn": xcolumn,
                "ycolumn": ycolumn,
                "epsg": epsg,
                "output": _output

              };

            waitingDialog.show('Local Map Adaptation running..');

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
          if($('#aoiRadios2').prop('checked')){
                $( "#shapefile" ).prop( "disabled", false );
                $( "#samplingUpload" ).prop( "disabled", false );


                disableDrawing();

                //map.removeControl(draw_control);

          }else{

                $( "#shapefile" ).prop( "disabled", true );
                $( "#samplingUpload" ).prop( "disabled", true );

                 $( "#uploadfiles ul" ).empty();

                 //map.addControl(draw_control);

                 enableDrawing();

          }
      });

        // sampling design shapefile upload
        $("#shpupload").submit(function(e){
            //alert("form submitted");
            e.preventDefault();

            waitingDialog.show('Uploading..');

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


                        selected_shp = data.url;

                        var _file = '<li>'+data.url+'</li>';
                        $( "#uploadfiles ul" ).append(_file);

                        addWMSlayer(data.layer_wms);

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

            waitingDialog.show('Uploading..');

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

                        pointdata = data.url;
                        datafields = data.fields;
						
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

                        addWMSlayer(data.layer_wms);

                    },error: function(){
                        waitingDialog.hide();
                        alert("error");
                    }
                 });
         });












});
