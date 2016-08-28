<!DOCTYPE html>
<!-- SETTINGS.PHP -->
<html lang="en">
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
            <meta name="description" content="HydroPi Pool Management and Power Control">
            <meta name="author" content="">
            <link rel="icon"
                  type="image/png"
                  href="http://YourWebsite.com/favicon.png"> <!-- Or href="http://localhost/favicon.png"> -->

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
            <div class="col-xs-12">
            <!-- Create a panel for the Raspberry Pi functions -->
                <div class="panel panel-info">
                    <div class="panel-heading">
                        <h4 class="text-center" style="color:#FFFFFF">Raspberry Pi Tools</h4>
                    </div>
                    <div class="panel-body">
                        <div class="col-lg-6 col-xs-12 text-center">
                            <button style="margin-bottom: 20px;" type="button" class="btn btn-md btn-info btn-block" onclick="Shutdown()">Shutdown</button>
                        </div>
                        <div class="col-lg-6 col-xs-12 text-center">
                            <button style="margin-bottom: 20px;" type="button" class="btn btn-md btn-primary btn-block" onclick="Restart()">Restart</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xs-12">
                <!-- Create a panel for the MySQL database delete functions -->
                <div class="panel panel-info">
                    <div class="panel-heading">
                        <h4 class="text-center" style="color:#FFFFFF">MySQL Delete Readings</h4>
                    </div>
                    <div class="panel-body">
                        <div class="col-lg-3 col-sm-6 text-center">
                            <button style="margin-bottom: 20px;" type="button" class="btn btn-md btn-info btn-block" onclick="Delete_MySQL(0)">Delete All</button>
                        </div>
                        <div class="col-lg-3 col-sm-6 text-center">
                            <button style="margin-bottom: 20px;" type="button" class="btn btn-md btn-primary btn-block" onclick="Delete_MySQL(90)">Over 3 Months</button>
                        </div>
                        <div class="col-lg-3 col-sm-6 text-center">
                            <button style="margin-bottom: 20px;"type="button" class="btn btn-md btn-info btn-block" onclick="Delete_MySQL(180)">Over 6 Months</button>
                        </div>
                        <div class="col-lg-3 col-sm-6 text-center">
                            <button type="button" class="btn btn-md btn-primary btn-block" onclick="Delete_MySQL(365)">Over 12 Months</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xs-12">
                <!-- Create a panel for the current settings -->
                <div class="panel panel-info">
                    <div class="panel-heading" style="margin-bottom: 5px;">
                        <h4 class="text-center" style="color:#FFFFFF">Misc Settings</h4>
                    </div>
                        <!-- Create a form to hold the settings -->
                        <form class="form" method="POST" action="/php/update_settings.php">
                            <fieldset>
                                <?php
                                // Get the names of all the settings in the database and add an input for each to the form
                                include "php/settings_col_names.php";
                                $count = 0;
                                foreach ($colnames as $title) {
                                    $count += 1;
                                    if ($count % 2 == 0) {
                                        $mycolor = "btn-info";
                                    }
                                    else {
                                        $mycolor = "btn-primary";
                                    }
echo "                              <div class=\"form-group row col-lg-6 col-xs-12 center-block\" style=\"margin-bottom: 5px;\">\n";
echo "                                  <div class=\"col-lg-3 col-xs-12 text-center\">\n";
echo "                                      <label class=\"col-form-label\" for=\"text-input\" id=\"" .$title. "_name\"></label>\n";
echo "                                  </div>\n";
echo "                                  <div class=\"col-lg-9 col-xs-12\">\n";
echo "                                      <input name=\"" .$title. "\" class=\"form-control input-md text-center " .$mycolor. "\" id=\"" .$title. "\" autocomplete=\"off\">\n";
echo "                                  </div>\n";
echo "                              </div>\n";
                                }
                                ?>
                                <!-- Create a button to update the settings values -->
                                <div style="background-color:#033C73" class="col-xs-12 text-center">
                                    <button style="margin-bottom:5px; margin-top: 5px;" name="singlebutton" class="btn btn-success" id="singlebutton">Update Settings</button>
                                </div>

                            </fieldset>
                        </form>
                    <script>
                        <?php
                            // Add web names for each setting values and read all the current settings values
                            include "php/settings_webpage_names.php";
                            include "php/initial_settings_data.php";
                        ?>
                    </script>
                </div>
            </div>
        </div>
    </body>
    
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>

    <!-- Custom JavaScript
    ================================================== -->
    <script src="js/hydropi.js"></script>
</html>