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
            <div class="row">
                <div class="col">
                <!-- Create a card for the Raspberry Pi functions -->
                    <div class="card border border-dark text-light mb-3" style= "background-color:#033C73"> 
                        <div class="card-title">
                            <h4 class="d-flex justify-content-center">Raspberry Pi Tools</h4>
                        </div>
                        <div class="card-body d-flex justify-content-center">
                            <div class="col">
                                <button type="button" class="btn btn-md btn-info btn-block mb-2" onclick="Shutdown()">Shutdown</button>
                            </div>
                            <div class="col">
                                <button type="button" class="btn btn-md btn-primary btn-block mb-2" onclick="Restart()">Restart</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                <!-- Create a card for the MySQL database delete functions -->
                    <div class="card border border-dark text-light mb-3" style= "background-color:#033C73">
                        <div class="card-title">
                            <h4 class="d-flex justify-content-center">MySQL Delete Readings</h4>
                        </div>
                        <div class="card-body d-flex justify-content-center">
                            <div class="col">
                                <button type="button" class="btn btn-md btn-info btn-block mb-2" onclick="Delete_MySQL(0)">Delete All</button>
                            </div>
                            <div class="col">
                                <button type="button" class="btn btn-md btn-primary btn-block mb-2" onclick="Delete_MySQL(90)">Over 3 Months</button>
                            </div>
                            <div class="col">
                                <button type="button" class="btn btn-md btn-info btn-block mb-2" onclick="Delete_MySQL(180)">Over 6 Months</button>
                            </div>
                            <div class="col">
                                <button type="button" class="btn btn-md btn-primary btn-block mb-2" onclick="Delete_MySQL(365)">Over 12 Months</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col">
                <!-- Create a card for the current settings -->
                    <div class="card border border-dark text-light mb-3" style= "background-color:#033C73">
                        <div class="card-title mb-2">
                            <h4 class="d-flex justify-content-center">Misc Settings</h4>
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
echo "                              <div class=\"form-group row col mb-2\">\n";
echo "                                  <div class=\"col-sm-4 d-flex justify-content-center\">\n";
echo "                                      <label class=\"col-form-label\" for=\"text-input\" id=\"" .$title. "_name\"></label>\n";
echo "                                  </div>\n";
echo "                                  <div class=\"col-sm-8\">\n";
echo "                                      <input name=\"" .$title. "\" class=\"form-control input-md d-flex justify-content-center " .$mycolor. "\" id=\"" .$title. "\" autocomplete=\"off\">\n";
echo "                                  </div>\n";
echo "                              </div>\n";
                                }
                                ?>
                                <!-- Create a button to update the settings values -->
                                <div style="background-color:#033C73" class="col-sm-12 d-flex justify-content-center">
                                    <button name="singlebutton" class="btn btn-success my-2" id="singlebutton">Update Settings</button>
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
    <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

    <!-- Custom JavaScript
    ================================================== -->
    <script src="js/hydropi.js"></script>
</html>
