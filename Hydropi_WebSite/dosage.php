<!DOCTYPE html>
<!-- DOSAGE.PHP -->
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
        <div class="container">
            <!-- Create a panel and insert rows for each strip test calculation -->
            <div class="panel panel-info">
                <div class="panel-heading">
                    <h3 class="panel-title text-center">Strip Test Calculations</h3>
                </div>
                <div class="panel-body" style="padding-top: 0px; padding-bottom: 0px">
                    <!-- Create a row for each strip test value -->
                    <div class="row">
                        <div class="col-xs-12 col-sm-3 text-center">
                            <h3>Stabliser</h3>
                        </div>
                        <div class="col-xs-12 col-sm-3">
                            <div class="col-xs-6 col-sm-6" style="padding-top: 5px">
                                <input class="form-control input-md text-center" name="cya_value" id="cya_input" type="number">
                            </div>
                            <div class="col-xs-6 col-sm-6 text-center" style="padding-top: 5px">
                            <?php
                            // Get the pool size value from the database to calculate the required dosage
                            require "php/hydropi_connect.php";
                            $sql="SELECT pool_size FROM settings";
                            $result=mysqli_query($conn,$sql);
                            $pool_vol = mysqli_fetch_row($result);
echo "                          <button class=\"btn btn-info\" name=\"singlebutton\" id=\"tcl_button\" onclick=\"chemical_check_cya(".$pool_vol[0].")\">Calculate</button>\n";
                            mysqli_free_result($result);
                            mysqli_close($conn);
                            ?>
                            </div>
                        </div>
                        <div class="col-xs-12 col-sm-6 text-center">
                            <h3 id=cya_action></h3>
                        </div>
                    </div>
                    <div class="row" style="background-color: #E3E3E3">
                        <div class="col-xs-12 col-sm-3 text-center">
                            <h3>Total Alkalinity</h3>
                        </div>
                        <div class="col-xs-12 col-sm-3">
                            <div class="col-xs-6 col-sm-6" style="padding-top: 5px">
                                <input class="form-control input-md text-center" name="ta_value" id="ta_input" type="number">
                            </div>
                            <div class="col-xs-6 col-sm-6 text-center" style="padding-top: 5px">
                            <?php
                            require "php/hydropi_connect.php";
                            $sql="SELECT pool_size FROM settings";
                            $result=mysqli_query($conn,$sql);
                            $pool_vol = mysqli_fetch_row($result);
echo "                          <button class=\"btn btn-info\" name=\"singlebutton\" id=\"tcl_button\" onclick=\"chemical_check_ta(".$pool_vol[0].")\">Calculate</button>\n";
                            mysqli_free_result($result);
                            mysqli_close($conn);
                            ?>
                            </div>
                        </div>
                        <div class="col-xs-12 col-sm-6 text-center">
                            <h3 id=ta_action></h3>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-xs-12 col-sm-3 text-center">
                            <h3>Total Chlorine</h3>
                        </div>
                        <div class="col-xs-12 col-sm-3">
                            <div class="col-xs-6 col-sm-6" style="padding-top: 5px">
                                <input class="form-control input-md text-center" name="tcl_value" id="tcl_input" type="number">
                            </div>
                            <div class="col-xs-6 col-sm-6 text-center" style="padding-top: 5px">
                            <?php
                            require "php/hydropi_connect.php";
                            $sql="SELECT pool_size FROM settings";
                            $result=mysqli_query($conn,$sql);
                            $pool_vol = mysqli_fetch_row($result);
echo "                          <button class=\"btn btn-info\" name=\"singlebutton\" id=\"tcl_button\" onclick=\"chemical_check_tcl(".$pool_vol[0].")\">Calculate</button>\n";
                            mysqli_free_result($result);
                            mysqli_close($conn);
                            ?>
                            </div>
                        </div>
                        <div class="col-xs-12 col-sm-6 text-center">
                            <h3 id=tcl_action></h3>
                        </div>
                    </div>
                    <div  class="row" style="background-color: #E3E3E3">
                        <div class="col-xs-12 col-sm-3 text-center">
                            <h3>Calcium Hardness</h3>
                        </div>
                        <div class="col-xs-12 col-sm-3">
                            <div class="col-xs-6 col-sm-6" style="padding-top: 5px">
                                <input class="form-control input-md text-center" name="ch_value" id="ch_input" type="number">
                            </div>
                            <div class="col-xs-6 col-sm-6 text-center" style="padding-top: 5px">
                            <?php
                            require "php/hydropi_connect.php";
                            $sql="SELECT pool_size FROM settings";
                            $result=mysqli_query($conn,$sql);
                            $pool_vol = mysqli_fetch_row($result);
echo "                          <button class=\"btn btn-info\" name=\"singlebutton\" id=\"tcl_button\" onclick=\"chemical_check_ch(".$pool_vol[0].")\">Calculate</button>\n";
                            mysqli_free_result($result);
                            mysqli_close($conn);
                            ?>
                            </div>
                        </div>
                        <div class="col-xs-12 col-sm-6 text-center">
                            <h3 id=ch_action></h3>
                        </div>
                        <!-- Create button to clear the calculated values -->
                        <div style="background-color:#033C73" class="col-xs-12 text-center">
                            <button class="btn btn-success" style="margin-bottom:5px; margin-top: 5px;" name="singlebutton" id="clearme" onclick="clear_dosage()">Clear All</button>
                        </div>
                    </div>
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