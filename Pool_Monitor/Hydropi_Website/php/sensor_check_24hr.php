<?php
// SENSOR_CHECK_24HR.PHP

// Use this file to present a rolling 24hr average, rename the file to sensor_check.php
// in order for it to work with the other php scripts

    include "sensor_col_names.php";
    // Get an array of all the connected sensors names
    require "hydropi_connect.php";

    //Get the pool volume

    $sql="SELECT pool_size FROM settings";
    $result=mysqli_query($conn,$sql);
    $pool_vol = mysqli_fetch_row($result);

    mysqli_free_result($result);

            //Check Averages based on previous 24 hours, not on relay/pump times

           $startdt_1 = new DateTime(date('Y-m-d H:i:s'));
           $stopdt_1 =  new DateTime(date('Y-m-d H:i:s'));

            date_sub($startdt_1, date_interval_create_from_date_string('1 days'));
                $query_start_date = new DateTime($startdt_1->format('Y-m-d') .' ' .$startdt_1->format('H:i:s'));
                $query_stop_date = new DateTime($stopdt_1->format('Y-m-d') .' ' .$stopdt_1->format('H:i:s'));
                $query_start_date = $query_start_date->format('\"Y-m-d H:i:s\"');
                $query_stop_date = $query_stop_date->format('\"Y-m-d H:i:s\"');

                foreach ($colnames as $title) {
                    $stmt = ("SELECT AVG(".$title.") FROM sensors WHERE timestamp BETWEEN ".$query_start_date." AND ".$query_stop_date."");
                    if($result = mysqli_query($conn, $stmt)){
                        $row = mysqli_fetch_row($result);
                        if ($title == "ds18b20_temp") {
                            echo  "document.getElementById(\"".$title."_avg\").innerHTML = \"".round($row[0],1)."<sup>&degC</sup>\";\n";
                            $check = mysqli_query($conn, ("SELECT ds18b20_temp_low FROM settings WHERE pk=1"));
                            $value = mysqli_fetch_row($check);
                            // Present a recommended action based on the average values returned
                            if(round($row[0],1) < ($value[0])){
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"Too Cold for a Swim\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#e12b31\";\n";
                            }
                            else {
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"OK\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#88c149\";\n";
                            }
                            mysqli_free_result($check);
                        }
                        elseif ($title == "atlas_temp") {
                            echo  "document.getElementById(\"".$title."_avg\").innerHTML = \"".round($row[0],1)."<sup>&degC</sup>\";\n";
                            $check = mysqli_query($conn, ("SELECT atlas_temp_low FROM settings WHERE pk=1"));
                            $value_low = mysqli_fetch_row($check);
                            $check2 = mysqli_query($conn, ("SELECT atlas_temp_hi FROM settings WHERE pk=1"));
                            $value_high = mysqli_fetch_row($check2);
                            if(round($row[0],1) < ($value_low[0])){
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"Put the cover on\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#e12b31\";\n";
                            }
                            elseif(round($row[0],1) > ($value_high[0])){
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"Take the cover off\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#e12b31\";\n";
                            }
                            else {
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"OK\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#88c149\";\n";
                            }
                            mysqli_free_result($check);
                            mysqli_free_result($check2);
                        }
                        elseif ($title == "ph") {
                            echo  "document.getElementById(\"".$title."_avg\").innerHTML = \"".round($row[0],2)."\";\n";
                            $check = mysqli_query($conn, ("SELECT ph_low FROM settings WHERE pk=1"));
                            $value_low = mysqli_fetch_row($check);
                            $check2 = mysqli_query($conn, ("SELECT ph_hi FROM settings WHERE pk=1"));
                            $value_high = mysqli_fetch_row($check2);
                            if ((round($row[0],1) < ($value_low[0]))) {
                                $ph_inc_value = (((7.4 - (round($row[0],1)))/0.1)*2)*($pool_vol[0]/1000);
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"Add ".$ph_inc_value." g of pH Inc\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#e12b31\";\n";
                            }
                            elseif ((round($row[0],1) > ($value_high[0]))) {
                                $ph_hcl = ((round($row[0],1)) - 7.1)*$pool_vol[0]*0.03;
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"Add ".$ph_hcl." ml of Acid\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#e12b31\";\n";
                            }
                            else {
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"OK\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#88c149\";\n";
                            }
                            mysqli_free_result($check);
                            mysqli_free_result($check2);
                        }
                        elseif ($title == "orp") {
                            echo  "document.getElementById(\"".$title."_avg\").innerHTML = \"".round($row[0],0)."mV\";\n";
                            $check = mysqli_query($conn, ("SELECT orp_low FROM settings WHERE pk=1"));
                            $value_low = mysqli_fetch_row($check);
                            $check2 = mysqli_query($conn, ("SELECT orp_hi FROM settings WHERE pk=1"));
                            $value_high = mysqli_fetch_row($check2);
                            if ((round($row[0],0) < ($value_low[0]))) {
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"Add 100 g of Chlorine\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#e12b31\";\n";
                            }
                            elseif ((round($row[0],0) > ($value_high[0]))) {
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"Reduce chlorinator / remove cover\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#e12b31\";\n";
                            }
                            else {
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"OK\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#88c149\";\n";
                            }
                            mysqli_free_result($check);
                            mysqli_free_result($check2);
                        }
                        elseif ($title == "ec") {
                            echo  "document.getElementById(\"".$title."_avg\").innerHTML = \"".round($row[0],0)."ppm\";\n";
                            $check = mysqli_query($conn, ("SELECT ec_low FROM settings WHERE pk=1"));
                            $value_low = mysqli_fetch_row($check);
                            $check2 = mysqli_query($conn, ("SELECT ec_hi FROM settings WHERE pk=1"));
                            $value_high = mysqli_fetch_row($check2);
                            if ((round($row[0],0) < ($value_low[0]))) {
                                $salt_start = ($pool_vol[0]*($row[0]))/1000000;
                                $salt_finish = ($pool_vol[0]*5500)/1000000;
                                $add_salt = round(($salt_finish - $salt_start),0);
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"Add ".$add_salt." kg of salt\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#e12b31\";\n";
                            }
                            elseif ((round($row[0],0) > ($value_high[0]))) {
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"Add fresh water\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#e12b31\";\n";
                            }
                            else {
                                echo  "document.getElementById(\"".$title."_check\").innerHTML = \"OK\";\n";
                                echo  "document.getElementById(\"".$title."_check\").style.color = \"#FFFFFF\";\n";
                                echo  "document.getElementById(\"".$title."_color\").style.backgroundColor = \"#88c149\";\n";
                            }
                            mysqli_free_result($check);
                            mysqli_free_result($check2);
                        }

                    }
                }
            break;

    mysqli_free_result($result);
    mysqli_close($conn);
?>
