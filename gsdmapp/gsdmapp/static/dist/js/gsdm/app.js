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
            /*
            var upload_form = '<div class="form-group">';
            upload_form += '<form id="shpupload" action="" method="post" enctype="multipart/form-data">';
            upload_form += '<label for="shapefile" class="col-xs-3 control-label">Select zipped shapefile:</label>';
            upload_form += '<div class="col-xs-9">';
            upload_form += '<input id="shapefile" name="shapefile" type="file" class="form-control"/>';
            upload_form += '</div>';
            upload_form += '<div class="col-xs-9 col-xs-offset-3">';
            upload_form += '<button id="samplingUpload" type="submit" class="btn btn-primary btn-block">Upload</button>';
            upload_form += '</div>';
            upload_form += ' </form>';
            upload_form += '</div>';

            $( ".custom-file" ).append(upload_form);
            */

          }else{

              /*$( ".custom-file" ).empty();*/
          }
      });


        $("#shpupload").submit(function(e){
            //alert("form submitted");
            e.preventDefault();

            var formdata = new FormData(this);

                $.ajax({
                    url: "/uploads/",
                    type: "POST",
                    data: formdata,
                    mimeTypes:"multipart/form-data",
                    contentType: false,
                    cache: false,
                    processData: false,
                    success: function(data){
                        //alert(data.message);
                        waitingDialog.show(data.message);
                        setTimeout(function () {
                          waitingDialog.hide();
                        }, 2000);

                        var _file = '<li>'+data.url+'</li>';
                        $( "ul" ).append(_file);

                    },error: function(){
                        alert("error");
                    }
                 });
         });










});