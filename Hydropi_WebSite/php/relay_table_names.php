<?php
// RELAY_TABLE_NAMES.PHP
    require "hydropi_connect.php";
    // Get all the connected relay names and place in an array
    $sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'hydropi'";
    $result = mysqli_query($conn, $sql);
    $row_cnt = mysqli_num_rows($result);
    if ($row_cnt > 0) {
        // output data of each row
        $relaynames = array();
        while($row = mysqli_fetch_assoc($result)) {
            $relaynum = 0;
            for ($x = 0; $x < $row_cnt; $x++) {
                $relaynum = $relaynum + 1;
                if ($row['TABLE_NAME'] == ("relay_" .$relaynum. "_timer")) {
                    $relaynames[$relaynum] = $row['TABLE_NAME'];
                }
            }
        }
    }
    mysqli_free_result($result);
    mysqli_close($conn);
?>
