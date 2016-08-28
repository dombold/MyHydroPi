<?php
// INITIAL_TIMER_DATA.PHP
    require "hydropi_connect.php";
    $numofdays = $_POST['newtime'];
    // Delete the sensor readings for the selected timeframe
    if ($numofdays > 1) {
        $sql = mysqli_prepare($conn, "DELETE FROM sensors WHERE timestamp < (now() - interval ? day)");
        mysqli_stmt_bind_param($sql, 's',$numofdays);
        mysqli_stmt_execute($sql);
        mysqli_close($conn);
    }
    elseif ($numofdays < 1) {
        // Delete all of the readings from the sensors table
        $sql = ("DELETE FROM sensors");
        mysqli_query($conn, $sql);
        mysqli_close($conn);
    }
?>