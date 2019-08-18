<?php
// HYDROPI_CONNECT.PHP
    // Set database login details
    $servername = "localhost";
    $username = "YourDatabaseUserName";
    $password = "YourDatabasePassword";
    $dbname = "hydropidb"; // Default change to your database name if necessary

    // Default, change to your timezone. https://www.php.net/manual/en/timezones.php
    $timezone = 'Australia/Perth';
    
    // Create connection

    $conn = mysqli_connect($servername, $username, $password, $dbname);

    // Check connection

    if (!$conn) {
        die("Connection failed: " . mysqli_connect_error());
    }
?>