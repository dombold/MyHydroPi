<!DOCTYPE html>
<!-- GRAPHS.PHP -->
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
        <div class="container"></div>
        <!-- Create custom menu for selecting the timeframe for plotting the graphs -->
        <div class="container">
            <nav class="navbar navbar-inverse">
                <div class="container">
                    <div class="navbar-header">
                        <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar2" aria-expanded="false" aria-controls="navbar">
                            <span class="sr-only">Toggle navigation</span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                        </button>
                        <a class="navbar-brand" href="#">View Chart for:</a>
                    </div>
                    <div id="navbar2" class="navbar-collapse collapse">
                        <ul class="nav navbar-nav">
                            <li><a type="button" href="#" onclick="drawChart(1);">1 Day</a></li>
                            <li><a type="button" href="#" onclick="drawChart(7);">1 Week</a></li>
                            <li><a type="button" href="#" onclick="drawChart(30);">1 Month</a></li>
                            <li><a type="button" href="#" onclick="drawChart(90);">3 Months</a></li>
                            <li><a type="button" href="#" onclick="drawChart(180);">6 Months</a></li>
                            <li><a type="button" href="#" onclick="drawChart(365);">1 Year</a></li>
                        </ul>
                    </div><!--/.nav-collapse -->
                </div>
            </nav>


            <div class="panel-group">
            <?php
                // Read the sensors that are connected from the database and create a panel for each graph
                include "php/sensor_col_names.php";
                foreach ($colnames as $title){
echo "                <div class=\"panel panel-info\">\n";
echo "                    <div class=\"panel-heading\">\n";
echo "                        <div class=\"panel-title text-center\" id=\"" .$title. "_name\">\n";
echo "                        </div>\n";
echo "                    </div>\n";
echo "                    <div class=\"panel-body\" id=\"" .$title. "_graph\" style=\"height:400px\" class=\"panel-body\">\n";
echo "                    </div>\n";
echo "                </div>\n";
            }
            ?>
            <script>
                <?php
                    // populate the graph panel with webpage names
                    include "php/sensor_webpage_names.php";
                ?>
            </script>
            </div>
        </div>
    </body>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>

    <!-- Google Charts JavaScript
    ================================================== -->
    <script src="https://www.google.com/jsapi"></script>

    <!-- Custom JavaScript
    ================================================== -->
    <script src="js/hydropi.js"></script>
    <!-- When the page has loaded draw the graphs into each panel -->
    <script>
    google.load("visualization", "1", {packages:["corechart"]});
    google.setOnLoadCallback(function(){drawChart(1)});
    </script>
    <!-- Redraw the graphs to fit when the window size changes -->
    <script>
    var chart1 = "done";
    $(window).resize(function() {
        if(chart1=="done"){
            chart1 = "waiting";
            setTimeout(function(){drawChart(1);chart1 = "done"},1000);
        }
    });
    </script>
</html>