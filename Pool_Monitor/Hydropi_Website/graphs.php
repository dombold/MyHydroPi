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
        <div class="container"></div>
        <!-- Create custom menu for selecting the timeframe for plotting the graphs -->
        <div class="container">
            <nav class="navbar navbar-dark navbar-expand-md">
                <div class="container">
                    <a class="navbar-brand" href="#">View Chart for:</a>
                    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar2" aria-expanded="false" aria-controls="navbar2" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse " id="navbar2">
                        <ul class="navbar-nav nav-tabs ml-auto">
                            <li class="nav-item"><a class="nav-link" style= "background-color:#033C73" type="button" href="#" onclick="drawChart(1);">1 Day</a></li>
                            <li class="nav-item"><a class="nav-link" style= "background-color:#033C73" type="button" href="#" onclick="drawChart(7);">1 Week</a></li>
                            <li class="nav-item"><a class="nav-link" style= "background-color:#033C73" type="button" href="#" onclick="drawChart(30);">1 Month</a></li>
                            <li class="nav-item"><a class="nav-link" style= "background-color:#033C73" type="button" href="#" onclick="drawChart(90);">3 Months</a></li>
                            <li class="nav-item"><a class="nav-link" style= "background-color:#033C73" type="button" href="#" onclick="drawChart(180);">6 Months</a></li>
                            <li class="nav-item"><a class="nav-link" style= "background-color:#033C73" type="button" href="#" onclick="drawChart(365);">1 Year</a></li>
                        </ul>
                    </div><!--/.nav-collapse -->
                </div>
            </nav>
        <div>


            <div class="card-group">
            <?php
                // Read the sensors that are connected from the database and create a panel for each graph
                include "php/sensor_col_names.php";
                foreach ($colnames as $title){
echo "             <div class=\"col-sm-12\">\n";
echo "                 <div class=\"card border border-dark text-light mb-3\" style= \"background-color:#033C73\">\n";
echo "                     <div class=\"card-title\">\n";
echo "                         <h2 class=\"d-flex justify-content-center\" id=\"" .$title. "_name\"></h2>\n";
echo "                     </div>\n";
echo "                     <div class=\"card-body\" id=\"" .$title. "_graph\" style=\"height:400px\" class=\"card-body\">\n";
echo "                     </div>\n";
echo "                 </div>\n";
echo "             </div>\n";
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
    <div class="col-sm-12">

    <!-- Bootstrap JQuery JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

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
