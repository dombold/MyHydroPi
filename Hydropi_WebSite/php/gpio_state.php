<?php
// GPIO_STATE.PHP
    //Read variables from AJAX call
    $new_state = $_POST['new_gpo_state'];
    $gpo_choice = $_POST['selected_gpo'];

    require "hydropi_connect.php";
    // Get each of the relay names from the database and place in an array
    $sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'hydropi' AND TABLE_NAME = 'timer_override'";
    $result = mysqli_query($conn, $sql);
    if (mysqli_num_rows($result) > 0) {
        $colnames = array();
        // output data of each row
        while($row = mysqli_fetch_assoc($result)) {
            if ($row['COLUMN_NAME'] != "pk") {
                array_push($colnames, $row['COLUMN_NAME']);
            }
        }
    }
    mysqli_free_result($result);
    sleep(2); // Wait for 2 seconds for python script to update database
    foreach ($colnames as $title) {
        // read the current state of the relay
        if($gpo_choice == "" .$title. "_timer"){
            $sql = "SELECT " .$title." FROM timer_override WHERE pk = 2";
            $result = mysqli_query($conn, $sql);
            $curr_state = mysqli_fetch_row($result);
            //return current realy state to javascript to update webpage
            echo ($curr_state[0]);
        }
    }
    mysqli_free_result($result);
    mysqli_close($conn);
?>