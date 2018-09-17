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

      // run sampling design
      $( "#samplingRun" ).click(function() {
        
        /*
        waitingDialog.show('Sampling Design running..');
        setTimeout(function () {
              waitingDialog.hide();
            }, 9000);

          }); */
          //console.log(aoi);

          //var polygon = JSON.stringify(aoi);
          var soil_raster = $("#samplingSoil").val();
          var method = $("#samplingMethod").val();
          var strat_size = $("#samplingStratsize").val();
          var min_dist = $("#samplingDistance").val();
          var edge = $("#samplingEdge").val();
          var criterium = $("#samplingCriterium").val();
          var output = $("#samplingOutput").val();

          var _url = 'http://localhost/sampling/';

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

         
          $.ajax({
              type: "POST",
              contentType: "application/json",
              url: _url,
              async: false,
              dataType: "json",
              data: JSON.stringify(samplingdata),
              success: function(data){

                   //console.log(data.shapefile);
                 

              }
          }); 

      });


      $('input[name="aoiRadios"]').change(function(){
          if($('#aoiRadios2').prop('checked')){
            var upload_form = '<form action="/uploads/" method="post" enctype="multipart/form-data">';
            upload_form += '<label for="shapefile">Select a file:</label>';
            upload_form += '<input id="shapefile" name="shapefile" type="file" />';
            upload_form += '<input type="submit" value="Upload"/>';
            upload_form += ' </form>';

            $( ".custom-file" ).append(upload_form);

          }else{

              $( ".custom-file" ).empty();
          }
      });










});