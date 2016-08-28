<?php
// GET_GRAPH.PHP
    require "hydropi_connect.php";
    // Read variables from AJAX call
    $timeframe = $_POST['newtimeframe'];
    $sensor_name = $_POST['sensor'];
    $label_name = $_POST['label'];
    // Get the sensor readings for the selected timeframe
    $sql = "SELECT timestamp, ".$sensor_name." from sensors where timestamp > now() - interval '".$timeframe."' day";
    $result = mysqli_query($conn, $sql);
    $row = mysqli_fetch_row($result);

    $table = array();
    $table['cols'] = array(
        array('label' => 'Date', 'type' => 'string'),
        array('label' => $label_name, 'type' => 'number')
        );
    $rows = array();

    foreach($result as $row){
        // Build array for google chart
        $time = strtotime($row['timestamp']);
        $short_date = date("d/m G:i", $time);
        $temp = array();

        //Value
        $temp[] = array('v' => (string) $short_date);
        $temp[] = array('v' => (float) round($row[$sensor_name],2));
        $rows[] = array('c' => $temp);
    }
    $result->free();
    $table['rows'] = $rows;
    $jsonTable = json_encode($table, true);
    // Return array to javascript for google chart
    echo json_encode($table, JSON_PRETTY_PRINT);

    mysqli_close($conn);
?>