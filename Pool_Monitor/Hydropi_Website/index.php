<!DOCTYPE html>
<!-- INDEX.PHP -->
<html lang="en">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
            <!-- Refresh the page every 5 minutes -->
            <meta http-equiv="refresh" content="300">
            <meta name="description" content="HydroPi Pool Management and Power Control">
            <meta name="author" content="">
            <link rel="icon"
                  type="image/png"
                  href="favicon.png"> <!-- Or href="http://localhost/favicon.png"> -->
            <title>HydroPi - Pool Monitor</title>

            <!-- Bootstrap core CSS -->
            <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">

            <!-- Custom styles for this template -->
            <link rel="stylesheet" type="text/css" href="css/hydropi_theme.css">

        </head>
<?php
    //Create the top menu
    include "php/top_menu.php"
?>
        <div class="container">
            <!--Sensors Panel starts here -->
            <div class="col-xs-12">
                <div class="panel panel-info">
                    <div class="panel-heading">
                        <h2 class="panel-title text-center">Sensors</h2>
                    </div>
                    <div class="panel-body" style="padding-top:0px; padding-bottom:0px;">
                        <div class="row hidden-xs" style="background-color:#2FA4E7; border-bottom:2px solid">
                            <div class="text-center col-xs-4" style="border-right:2px solid;">
                                <h4 style="color:#000000">Sensor</h4>
                            </div>
                            <div class="text-center col-xs-2" style="border-right:2px solid;">
                                <h4 style="color:#000000">Now</h4>
                            </div>
                            <div class="text-center col-xs-2" style="border-right:2px solid;">
                                <h4 style="color:#000000">Avg</h4>
                            </div>
                            <div class="text-center col-xs-4">
                                <h4 style="color:#000000">State</h4>
                            </div>
                        </div>
                        <?php
                            // Read the sensors that are connected from the database and create a row for each
                            include "php/sensor_col_names.php";
                            foreach ($colnames as $title) {
echo "                          <div class=\"row\" style=\" border-bottom:2px solid\">\n";
echo "                              <div class=\"text-center col-sm-4 col-xs-12\">\n";
echo "                                  <h4 id=\"" .$title. "_name\"></h4>\n";
echo "                              </div>\n";
echo "                              <div class=\"text-center col-sm-2 col-xs-6\" style=\"background-color:#022f5a\">\n";
echo "                                  <h4 id=\"" .$title. "_curr\" style=\"color:#FFFFFF\"></h4>\n";
echo "                              </div>\n";
echo "                              <div class=\"text-center col-sm-2 col-xs-6\" style=\"background-color:#022f5a\">\n";
echo "                                  <h4 id=\"" .$title. "_avg\" style=\"color:#FFFFFF\"></h4>\n";
echo "                              </div>\n";
echo "                              <div class=\"text-center col-sm-4 col-xs-12\" id=\"" .$title. "_color\">\n";
echo "                                  <h4><b style=\"color:#000000\" id=\"" .$title. "_check\"></b></h4>\n";
echo "                              </div>\n";
echo "                          </div>\n";
                            }
                        ?>
                        <!-- add a pause button to the bottom of the sensors panel -->
                        <div class="row">
                            <div class="col-xs-12 text-center" style= "padding-top:10px; padding-bottom:10px; background-color:#033C73">
                                <button id="pause_state" type="button" class="btn" onclick="set_pause_state()"></button>
                            </div>
                        </div>
                    </div>
                    <script>
                        <?php
                            // populate the sensors panel with updated sensor names and values
                            include "php/sensor_webpage_names.php";
                            include "php/get_current_sensor_values.php";
                            include "php/sensor_check.php";
                        ?>
                    </script>
                </div>
            </div>
             <!--Power Outlet Panel starts here -->
            <div class="col-xs-12">
                <div class="panel panel-info">
                    <div class="panel-heading">
                        <h2 class="panel-title text-center">Power Outlets</h2>
                    </div>
                    <div class="panel-body" style="padding-top:0px; padding-bottom:0px;">
                        <div class="row hidden-xs" style="background-color:#2FA4E7; border-bottom:2px solid">
                            <div class="text-center col-sm-6" style="border-right:2px solid;">
                                <h4 style="color:#000000">Relay</h4>
                            </div>
                            <div class="text-center col-sm-5" style="border-right:2px solid;">
                                <h4 style="color:#000000">Setting</h4>
                            </div>
                            <div class="text-center col-sm-1">
                                <h4 style="color:#000000">Now</h4>
                            </div>
                        </div>
                        <?php
                            include "php/relay_table_names.php";
                            $relay_num = count($relaynames);
                            for ($x = 1; $x <= $relay_num; $x++) {
echo "                      \n";
echo "                      <div class=\"row\" style=\"border-bottom:2px solid\">\n";
echo "                          <div class=\"text-center col-sm-6 col-xs-12\">\n";
echo "                              <h4 id=\"" .$relaynames[$x]. "_name\"></h4>\n";
echo "                          </div>\n";
echo "                          <div id=\"" .$relaynames[$x]. "_state\" class=\"text-center col-sm-5 col-xs-10\">\n";
echo "                              <div class=\"btn-group btn-group-md\" role=\"group\">\n";
echo "                                  <button type=\"button\" class=\"btn btn-success\" onclick=\"set_power_state('on', '". $relaynames[$x] ."')\">On</button>\n";
echo "                                  <button type=\"button\" class=\"btn btn-warning\" onclick=\"set_power_state('auto', '". $relaynames[$x] ."')\">Auto</button>\n";
echo "                                  <button type=\"button\" class=\"btn btn-danger\" onclick=\"set_power_state('off', '". $relaynames[$x] ."')\">Off</button>\n";
echo "                              </div>\n";
echo "                          </div>\n";
echo "                          <div class=\"text-center col-sm-1 col-xs-2\" style=\"background-color: #E0E0E0\">\n";
echo "                              <h4 id=\"" .$relaynames[$x]. "_curr\"></h4>\n";
echo "                          </div>\n";
echo "                      </div>\n";
                            }
                            ?>
                            <script>
                            <?php
                                // populate the relays panel with updated relay names and current settings
                                include "php/relay_webpage_names.php";
                                include "php/get_current_relay_states.php";
                            ?>
                            </script>
                    </div>
                </div>
            </div>
        </div>      <!-- Container close-->
    </body>

    <!-- Bootstrap JQuery JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>

    <!-- Custom JavaScript
    ================================================== -->
    <script src="js/hydropi.js"></script>
</html>
