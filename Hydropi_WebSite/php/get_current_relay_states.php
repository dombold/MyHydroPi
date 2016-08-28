<?php
// GET_CURRENT_RELAY_STATES.PHP
    require "hydropi_connect.php";
    // Get relay names and add to an array
    $sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'hydropi' AND TABLE_NAME = 'timer_override'";
    $result = mysqli_query($conn, $sql);
    if (mysqli_num_rows($result) > 0) {
        // output data of each row
        $colnames = array();
        while($row = mysqli_fetch_assoc($result)) {
            if ($row['COLUMN_NAME'] != "pk") {
                array_push($colnames, $row['COLUMN_NAME']);
            }
        }
    }
    mysqli_free_result($result);

    $sql = "SELECT * FROM timer_override WHERE pk = 1";
    $result = mysqli_query($conn, $sql);
    $row = mysqli_fetch_row($result);
    $count = 1;
    // Update webpage with background color change and current state for each relay
    foreach ($colnames as $title) {
        if (($row[$count]) == "auto") {
            echo "document.getElementById(\"".$title."_timer_state\").style.backgroundColor = \"#ff6707\";\n";
            $sql = "SELECT * FROM timer_override WHERE pk = 2";
            $result = mysqli_query($conn, $sql);
            $row2 = mysqli_fetch_row($result);
            if ($row2[$count] == 0){
                echo "document.getElementById(\"".$title."_timer_curr\").innerHTML = \"Off\";\n";
                echo "document.getElementById(\"".$title."_timer_curr\").style.color = \"#e12b31\";\n";
            }
            elseif ($row2[$count] == 1){
                echo "document.getElementById(\"".$title."_timer_curr\").innerHTML = \"On\";\n";
                echo "document.getElementById(\"".$title."_timer_curr\").style.color = \"#88c149\";\n";
            }
        }
        elseif (($row[$count]) == "on") {
            echo "document.getElementById(\"".$title."_timer_state\").style.backgroundColor = \"#88c149\";\n";
            echo "document.getElementById(\"".$title."_timer_curr\").innerHTML = \"On\";\n";
            echo "document.getElementById(\"".$title."_timer_curr\").style.color = \"#88c149\";\n";
        }
        elseif (($row[$count]) == "off") {
            echo "document.getElementById(\"".$title."_timer_state\").style.backgroundColor = \"#e12b31\";\n";
            echo "document.getElementById(\"".$title."_timer_curr\").innerHTML = \"Off\";\n";
            echo "document.getElementById(\"".$title."_timer_curr\").style.color = \"#e12b31\";\n";
        }
        $count = $count + 1;
    mysqli_free_result($result);
    }
    // Get current pause delay setting and update button color
    $sql = "SELECT pause_readings FROM settings WHERE pk = 1";
    $result = mysqli_query($conn, $sql);
    $row = mysqli_fetch_row($result);
    if ($row[0] == 1) { //True
        echo "document.getElementById(\"pause_state\").innerHTML = \"Sensor Readings Paused\";\n";
        echo "document.getElementById(\"pause_state\").className = \"btn btn-md btn-danger\";\n";
    }
    elseif ($row[0] == 0) { //False
        echo "document.getElementById(\"pause_state\").innerHTML = \"Pause Sensor Readings\";\n";
        echo "document.getElementById(\"pause_state\").className = \"btn btn-md btn-success\";\n";
    }

    mysqli_free_result($result);
    mysqli_close($conn);
?>