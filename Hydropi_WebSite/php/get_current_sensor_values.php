<?php
// GET_CURRENT_SENSOR_VALUES.PHP
    include "sensor_col_names.php";
    require "hydropi_connect.php";
    // Get the latest sensor reading, round the result for each sensor and update webpage
    $sql = "SELECT * FROM sensors ORDER BY `timestamp` DESC LIMIT 1 ";
    $result = mysqli_query($conn, $sql);
    $row = mysqli_fetch_assoc($result);

    foreach ($colnames as $title) {
        if ($title == "ds18b20_temp") {
          echo "document.getElementById(\"".$title."_curr\").innerHTML = \"".round($row[$title],1)."<sup>&degC</sup>\";\n";
        }
        else if ($title == "atlas_temp") {
          echo "document.getElementById(\"".$title."_curr\").innerHTML = \"".round($row[$title],1)."<sup>&degC</sup>\";\n";
        }
        else if ($title == "ph") {
          echo "document.getElementById(\"".$title."_curr\").innerHTML = \"".round($row[$title],2)."\";\n";
        }
        else if ($title == "orp") {
          echo "document.getElementById(\"".$title."_curr\").innerHTML = \"".round($row[$title],0)."mV\";\n";
        }
        else if ($title == "ec") {
          echo "document.getElementById(\"".$title."_curr\").innerHTML = \"".round($row[$title],0)."ppm\";\n";
        }
    }
    mysqli_free_result($result);
    mysqli_close($conn);
?>
