<?php
// UPDATE_PAUSE.PHP
    require "hydropi_connect.php";
    // When the pause button is pressed set pause to True(1)
    $sql = "UPDATE settings SET pause_readings = 1 WHERE pk = 1";
    mysqli_query($conn, $sql);
    mysqli_close($conn);
?>