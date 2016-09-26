<!DOCTYPE HTML>
<!-- TIMERS.PHP -->
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

            <!-- Include Rome.css to style the datepicker -->
            <link rel="stylesheet" type="text/css" href="css/rome.css">

            <!-- Custom styles for this template -->
            <link rel="stylesheet" type="text/css" href="css/hydropi_theme.css">
        </head>

<script src="js/rome.js"></script>
<?php
    //Create the top menu
    include "php/top_menu.php"
?>
        <div class="container">
                <?php
                    include "php/relay_table_names.php";
                    $loop = 0;
                    $relay_num = count($relaynames);
                    for ($x = 1; $x <= $relay_num; $x++) {
                        $loop += 1;
echo "                      <div class=\"col-xs-12\">\n";
echo "                        <div class=\"panel panel-info\">\n";
echo "                            <div class=\"panel-heading\">\n";
echo "                                <h2 class=\"panel-title text-center\" id=\"".$relaynames[$x]."_name\"></h2>\n";
echo "                            </div>\n";
echo "                            <div class=\"panel-body\" style=\"padding-left:0px; padding-right:0px; padding-bottom:0px;\">\n";
echo "                            <form class=\"form\" method=\"POST\" action=\"/php/update_timers.php\">\n";
echo "                                <fieldset>\n";
echo "                                    <div class=\"form-group row col-xs-12 center-block\" style=\"margin-bottom: 0px;\">\n";
                                            include "php/num_dt_pairs.php";
                                              for ($i = 1; $i <= $dt_count; $i++ ){
echo "                                        <div class=\"col-sm-4 col-md-2 col-xs-12 text-center\" style=\"padding-bottom:5px; padding-top:15px;\">\n";
echo "                                            <label class=\"col-form-label control-label \" for=\"textinput\">Start Time " .$i. "</label>\n";
echo "                                        </div>\n";
echo "                                        <div class=\"col-sm-8 col-md-4 col-xs-12\" style=\"padding-bottom:5px; padding-top:5px;\">\n";
echo "                                            <input name=\"gpostarttime" .$i. "\" class=\"form-control input-md text-center btn-info\" id=\"gpo" .$loop. "starttime" .$i. "\" type=\"datetime\" autocomplete=\"off\">\n";
echo "                                        </div>\n";
echo "                                        <div  class=\"col-sm-4 col-md-2 col-xs-12 text-center\" style=\"padding-bottom:5px; padding-top:15px;\">\n";
echo "                                            <label class=\"col-form-label control-label\" for=\"textinput\">Stop Time " .$i. "</label>\n";
echo "                                        </div>\n";
echo "                                        <div class=\"col-sm-8 col-md-4 col-xs-12\" style=\"padding-bottom:5px; padding-top:5px;\">\n";
echo "                                            <input name=\"gpostoptime" .$i. "\" class=\"form-control input-md text-center btn-primary\" id=\"gpo" .$loop. "stoptime" .$i. "\" type=\"datetime\" autocomplete=\"off\">\n";
echo "                                        </div>\n";
                                              include "php/initial_timer_data.php";
                                              }
echo "                                        <input name=\"gponumber\" type=\"hidden\" value=\"" .$relaynames[$x]. "\">\n";
echo "                                        <div class=\"col-xs-12 text-center\" style=\"background-color:#033C73;\">\n";
echo "                                            <button style=\"margin-bottom:5px; margin-top: 5px;\" name=\"singlebutton\" class=\"btn btn-success\" id=\"singlebutton\">Update Relay " .$loop. "</button>\n";
echo "                                        </div\n";
echo "                                    </div>\n";
echo "                                </fieldset>\n";
echo "                            </form>\n";
echo "                        </div>\n";
echo "                        </div>\n";
echo "                    </div>";
                    }
echo "              <script>\n";
                    // populate each relay with updated relay name
                    include "php/relay_webpage_names.php";
echo "              </script>\n";
                    ?>

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
