<?php
// SETTINGS_WEBPAGE_NAMES.PHP
    include "settings_col_names.php";
    // Get all the settings values in the database and present to the webpage with relevant names
    foreach ($colnames as $title) {
        if ($title == "ds18b20_temp_hi") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Air Temp High\";\n";
        }
        else if ($title == "ds18b20_temp_low") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Air Temp Low\";\n";
        }
        else if ($title == "atlas_temp_hi") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Pool Temp High\";\n";
        }
        else if ($title == "atlas_temp_low") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Pool Temp Low\";\n";
        }
        else if ($title == "ph_hi") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"pH High\";\n";
        }
        else if ($title == "ph_low") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"pH Low\";\n";
        }
        else if ($title == "orp_hi") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"ORP High\";\n";
        }
        else if ($title == "orp_low") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"ORP Low\";\n";
        }
        else if ($title == "ec_hi") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Salt High\";\n";
        }
        else if ($title == "ec_low") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Salt Low\";\n";
        }
        else if ($title == "pool_size") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Pool Volume:\";\n";
        }
        else if ($title == "offset_percent") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Alarm Reset Percentage\";\n";
        }
                else if ($title == "read_sensor_delay") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Read Sensors Every:\";\n";
        }
        else if ($title == "pause_reset_delay") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Pause Readings For:\";\n";
        }
        else if ($title == "email_reset_delay") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Resend Email Every:\";\n";
        }
        else if ($title == "to_email") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Send Email To:\";\n";
        }
    }
?>