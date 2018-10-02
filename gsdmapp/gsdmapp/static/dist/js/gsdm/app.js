$(document).ready(function(){

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


        // clear selections
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

              var _url = 'http://localhost/samplingdraw/';

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

                       for(var i=0; i < data.samplingout.length; i++){

                            //var outfile = '<li>'+data.samplingout[i]+'</li>';
                            var outfile = '<li><a href=/outputs/'+data.samplingout[i]+'>'+data.samplingout[i]+'</a></li>'

                            $( "#outfiles ul" ).append(outfile);
                       }


                  }
              });


          } else {

               // run sampling for uploaded shapefile
              var _url = 'http://localhost/samplingshp/';

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

                        $( "#outfiles ul" ).empty();
                       //console.log(data.samplingout);
                       for(var i=0; i < data.samplingout.length; i++){

                            //var outfile = '<li>'+data.samplingout[i]+'</li>';
                            var outfile = '<li><a href=/outputs/'+data.samplingout[i]+'>'+data.samplingout[i]+'</a></li>'

                            $( "#outfiles ul" ).append(outfile);
                       }


                  }
              });



          }



      });




      $('input[name="aoiRadios"]').change(function(){
          if($('#aoiRadios2').prop('checked')){
                $( "#shapefile" ).prop( "disabled", false );
                $( "#samplingUpload" ).prop( "disabled", false );


                drawnItems.clearLayers();

                map.removeControl(draw_control);

          }else{

                $( "#shapefile" ).prop( "disabled", true );
                $( "#samplingUpload" ).prop( "disabled", true );

                 $( "#uploadfiles ul" ).empty();

                 map.addControl(draw_control);

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
                        //alert(data.message);

                        waitingDialog.hide();


                        selected_shp = data.url;

                        var _file = '<li>'+data.url+'</li>';
                        $( "#uploadfiles ul" ).append(_file);

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

                    },error: function(){
                        waitingDialog.hide();
                        alert("error");
                    }
                 });
         });












});