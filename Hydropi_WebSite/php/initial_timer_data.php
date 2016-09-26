<?php
// INITIAL_TIMER_DATA.PHP
    require "php/hydropi_connect.php";
    // Select the datetime pairs from selected relay
    $sql= ("SELECT starttime, stoptime FROM ".$relaynames[$x]." WHERE pk = ".$i."");
    $result = mysqli_query($conn, $sql);
    $row = mysqli_fetch_row($result);
    // Fill webpage with the current datetime pairs and configure Rome DatePicker
    echo"                           <script>\n";
    echo"                           document.getElementById(\"gpo" .$loop. "starttime" .$i. "\").value = \"".$row[0]."\";\n";
    echo"                           document.getElementById(\"gpo" .$loop. "stoptime" .$i. "\").value = \"".$row[1]."\";\n";
    echo"                           if(window.innerWidth > 767){\n";
    echo"                             rome(gpo" .$loop. "starttime" .$i. ", {dateValidator: rome.val.beforeEq(gpo" .$loop. "stoptime" .$i. ")} );\n";
    echo"                             rome(gpo" .$loop. "stoptime" .$i. ", {dateValidator: rome.val.afterEq(gpo" .$loop. "starttime" .$i. ")} );\n";
    echo"                           }\n";
    echo"                           </script>\n";

    mysqli_free_result($result);
    mysqli_close($conn);
?>
