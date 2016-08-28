<?php
// RELAY_WEBPAGE_NAMES.PHP
    // Get the names of the connected relays
    include "relay_table_names.php";
    // Present more descriptive names for each relay to webpage
    foreach ($relaynames as $title) {
        if ($title == "relay_1_timer") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Pool Pump\";\n";
        }
        else if ($title == "relay_2_timer") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Gazebo Lights\";\n";
        }
        else if ($title == "relay_3_timer") {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Water Feature\";\n";
        }
        else {
          echo  "document.getElementById(\"".$title."_name\").innerHTML = \"Miscellaneous\";\n";
        }
    }
?>