<?php
// POWER_UPDATE.PHP
    //Read variables from AJAX call
    $new_state = $_POST['new_gpo_state'];
    $gpo_choice = $_POST['selected_gpo'];

    require "hydropi_connect.php";
    // Get each of the relay names from the database and place in an array
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
    // Update the selected relay in table time_override with the setting selected from the webpage           
    foreach ($colnames as $title) {
        if($gpo_choice == "" .$title. "_timer"){
            $stmt = mysqli_prepare($conn, "UPDATE timer_override SET " .$title." = ? WHERE pk = 1");
            mysqli_stmt_bind_param($stmt, 's', $new_state);
            mysqli_stmt_execute($stmt);
        }
    }
    mysqli_close($conn);
?>