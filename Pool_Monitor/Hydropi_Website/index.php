<!DOCTYPE html>
<!-- INDEX.PHP -->
<html lang="en">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <!-- The above 3 meta tags *must* come first in the head section -->
            <!-- Refresh the page every 5 minutes -->
            <meta http-equiv="refresh" content="300">
            <meta name="description" content="HydroPi Pool Management and Power Control">
            <meta name="author" content="">
            <link rel="icon"
                  type="image/png"
                  href="favicon.png"> <!-- Or href="http://localhost/favicon.png"> -->
            <title>HydroPi - Pool Monitor</title>

            <!-- Bootstrap core CSS -->
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

            <!-- Custom styles for this template -->
            <link rel="stylesheet" type="text/css" href="css/hydropi_theme.css">

        </head>
<?php
    //Create the top menu
    include "php/top_menu.php"
?>
        <div class="container">
            <!--Sensors Panel starts here -->
            <div class="col-sm-12">
                <div class="card border border-dark text-light mb-3" style= "background-color:#033C73;">
                    <div class="card-header">
                        <h2 class="d-flex justify-content-center">Sensors</h2>
                    </div>
                    <div class="table-responsive-sm"> 
                        <table class="table table-bordered my-0">
                            <thead class="bg-info text-dark">
                                <tr class="d-none d-sm-flex">
                                    <th class="d-flex justify-content-center py-2 col-sm-4" scope="col"><h3>Sensor</h3></th>
                                    <th class="d-flex justify-content-center py-2 col-sm-2" scope="col"><h3>Now</h3></th>
                                    <th class="d-flex justify-content-center py-2 col-sm-2" scope="col"><h3>Avg</h3></th>
                                    <th class="d-flex justify-content-center py-2 col-sm-4" scope="col"><h3>Action</h3></th>
                                </tr>
                            </thead>
                            <tbody>
                        <?php
                            // Read the sensors that are connected from the database and create a row for each
                            include "php/sensor_col_names.php";
                            foreach ($colnames as $title) {
echo "                              <tr class=\"d-sm-flex\">\n";                            
echo "                                  <th id=\"" .$title. "_name\" class=\"d-flex justify-content-center text-light py-2 col-sm-4\" scope=\"row\"></th>\n";
echo "                                  <th id=\"" .$title. "_curr\" class=\"bg-primary d-flex justify-content-center text-light py-2 col-sm-2\"></th>\n";
echo "                                  <th id=\"" .$title. "_avg\" class=\"bg-primary d-flex justify-content-center text-light py-2 col-sm-2\"></th>\n";
echo "                                  <th id=\"" .$title. "_check\" class=\"d-flex justify-content-center text-light py-2 col-sm-4\"></th>\n";
echo "                              </tr>\n";
                            }
                            ?>
                                <!-- add a pause button to the bottom of the sensors panel -->
                                <tr>
                                    <td class="d-flex justify-content-center py-4" colspan ="4">
                                        <button id="pause_state" type="button" class="btn" onclick="set_pause_state()"></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
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
             <div class="col-sm-12">
                <div class="card border border-dark text-light mb-3" style= "background-color:#033C73;">
                    <div class="card-header">
                        <h2 class="d-flex justify-content-center">Power Outlets</h2>
                    </div>
                    <div class="table-responsive-sm"> 
                        <table class="table table-bordered my-0">
                            <thead class="bg-info text-dark">
                                <tr class="d-none d-sm-flex">
                                    <th class="d-flex justify-content-center py-2 col-sm-5" scope="col"><h3>Relay</h3></th>
                                    <th class="d-flex justify-content-center py-2 col-sm-5" scope="col"><h3>Setting</h3></th>
                                    <th class="d-flex justify-content-center py-2 col-sm-2" scope="col"><h3>State</h3></th>
                                </tr>
                            </thead>
                            <tbody>
                        <?php
                            include "php/relay_table_names.php";
                            $relay_num = count($relaynames);
                            for ($x = 1; $x <= $relay_num; $x++) {
echo "                          <tr class=\"d-sm-flex\">\n";                            
echo "                              <th id=\"" .$relaynames[$x]. "_name\" class=\"d-flex justify-content-center text-light py-2 col-sm-5\" scope=\"row\"></th>\n";
echo "                              <th id=\"" .$relaynames[$x]. "_state\" class=\"d-flex justify-content-center text-light py-2 col-sm-5\" style= \"background-color:#033C73;\">\n";
echo "                              <div class=\"btn-group btn-group-sm\" role=\"group\">\n";
echo "                                  <button type=\"button\" class=\"btn btn-success border border-dark\" onclick=\"set_power_state('on', '". $relaynames[$x] ."')\">On</button>\n";
echo "                                  <button type=\"button\" class=\"btn btn-warning border border-dark\" onclick=\"set_power_state('auto', '". $relaynames[$x] ."')\">Auto</button>\n";
echo "                                  <button type=\"button\" class=\"btn btn-danger border border-dark\" onclick=\"set_power_state('off', '". $relaynames[$x] ."')\">Off</button>\n";
echo "                              </div>\n";
echo "                              </th>\n";
echo "                              <th id=\"" .$relaynames[$x]. "_curr\" class=\"d-flex justify-content-center text-light py-2 col-sm-2\" style= \"background-color:#033C73;\"></th>\n";
echo "                          </tr>\n";
                                }
                                ?>
                            </tbody>
                        </table>
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
    <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    <!-- Custom JavaScript
    ================================================== -->
    <script src="js/hydropi.js"></script>
</html>
