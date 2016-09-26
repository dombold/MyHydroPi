<?php
// NUM_DT_PAIRS.PHP
    require "hydropi_connect.php";
    // Count the number of datetime pairs associated with the relay
    $sql= ("SELECT * FROM ".$relaynames[$x]."");
    if ($result = mysqli_query($conn, $sql)) {
        $dt_count = mysqli_num_rows($result);
    mysqli_free_result($result);
}
mysqli_close($conn);
?>
