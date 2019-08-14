<?php
// HYDROPI_CONNECT.PHP
    // Set database login details
    $servername = "localhost"
    $username = "yourDatabbaseUsername"
    $password = "yourdatabasePassword"
    $dbname = "hydropidb"

    // Create connection

    $conn = mysqli_connect($servername, $username, $password, $dbname);

    // Check connection

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }
?>