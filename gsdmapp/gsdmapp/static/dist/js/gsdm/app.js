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


      $( "#samplingRun" ).click(function() {
        
        /*
        waitingDialog.show('Sampling Design running..');
        setTimeout(function () {
              waitingDialog.hide();
            }, 9000);

          }); */
          $.ajax({
            type: "GET",
            url: 'http://'+site_name+'/'+'&limit=0&format=json',
            async: false,
            dataType: "json",
            success: function(data){

                
                
               

            }
        });


      $('input[name="aoiRadios"]').change(function(){
          if($('#aoiRadios2').prop('checked')){
              
            $( ".custom-file" ).append( '<input type="file" class="custom-file-input" id="customFile">' );

          }else{

              $( ".custom-file" ).empty();
          }
      });










    });