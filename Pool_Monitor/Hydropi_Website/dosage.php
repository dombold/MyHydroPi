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
            <!-- Create a card and insert rows for each strip test calculation -->

                <div class="card border border-dark text-light mb-3" style= "background-color:#033C73">
                    <div class="card-title">
                        <h3 class="d-flex justify-content-center">Strip Test Calculations</h3>
                    </div>
                    <div class="card-body py-0">
                    <!-- Create a row for each strip test value -->
                    <div class="col-md-12 mb-3">
                        <div class="row">
                            <div class="col-md-4 d-flex justify-content-center">
                                <h3>Stabliser</h3>
                            </div>
                            <div class="col-md-2 pt-2">
                                <input class="form-control input-md d-flex justify-content-center" name="cya_value" id="cya_input" type="number">
                            </div>
                            <div class="col-md-2 d-flex justify-content-center pt-2">
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
                            <div class="col-md-4 d-flex justify-content-center">
                                <h3 id=cya_action></h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12 mb-3">
                        <div class="row">
                            <div class="col-md-4 d-flex justify-content-center">
                                <h3>Total Alkalinity</h3>
                            </div>
                            <div class="col-md-2 pt-2">
                                <input class="form-control input-md d-flex justify-content-center" name="ta_value" id="ta_input" type="number">
                            </div>
                            <div class="col-md-2 d-flex justify-content-center pt-2">
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
                            <div class="col-md-4 d-flex justify-content-center">
                                <h3 id=ta_action></h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12 mb-3">
                        <div class="row">
                            <div class="col-md-4 d-flex justify-content-center">
                                <h3>Total Chlorine</h3>
                            </div>
                            <div class="col-md-2 pt-2">
                                <input class="form-control input-md d-flex justify-content-center" name="tcl_value" id="tcl_input" type="number">
                            </div>
                            <div class="col-md-2 d-flex justify-content-center pt-2">
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
                            <div class="col-md-4 d-flex justify-content-center">
                                <h3 id=tcl_action></h3>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12 mb-3">
                        <div  class="row">
                            <div class="col-md-4 d-flex justify-content-center">
                                <h3>Calcium Hardness</h3>
                            </div>
                            <div class="col-md-2 pt-2">
                                <input class="form-control input-md d-flex justify-content-center" name="ch_value" id="ch_input" type="number">
                            </div>
                            <div class="col-md-2 d-flex justify-content-center pt-2">
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
                            <div class="col-md-4 d-flex justify-content-center">
                                <h3 id=ch_action></h3>
                            </div>
                        </div>
                    </div>
                    <!-- Create button to clear the calculated values -->
                    <div class="col-md-12 d-flex justify-content-center">
                        <button class="btn btn-success my-2" name="singlebutton" id="clearme" onclick="clear_dosage()">Clear All</button>
                    </div>
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
