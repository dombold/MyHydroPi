<?php
// SENSOR_WEBPAGE_NAMES.PHP
    include "sensor_col_names.php";
    // Get all the connected sensors from database and change names for web presentation
    foreach ($colnames as $title) {
        if ($title == "ds18b20_temp") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Air Temp\";\n";
        }
        else if ($title == "atlas_temp") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Pool Temp\";\n";
        }
        else if ($title == "ph") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"pH\";\n";
        }
        else if ($title == "orp") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"ORP\";\n";
        }
        else if ($title == "ec") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Salinity\";\n";
        }
    }
?>