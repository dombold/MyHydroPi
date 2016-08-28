<?php
// UPDATE_TIMERS.PHP
    require "hydropi_connect.php";
    // Get the number of date time pairs for the selected relay
    $gponum = $_POST['gponumber'];
    $sql= ("SELECT * FROM ".$gponum."");
    if ($result = mysqli_query($conn, $sql)) {
        $dt_count = mysqli_num_rows($result);
        mysqli_free_result($result);
    }

    for ($i = 1; $i <= $dt_count; $i++ ){
    // Update the database date time pairs from the times supplied
        $starttimer = $_POST{"gpostarttime$i"};
        $stoptimer = $_POST{"gpostoptime$i"};

        if ((empty($starttimer))or(empty($stoptimer))){
            // Add NULL entries to database if the date time pair is empty
            $starttimer = "NULL";
            $stoptimer = "NULL";
            $sql = "UPDATE ".$gponum." SET `starttime` = ".$starttimer.", `stoptime` = ".$stoptimer." WHERE pk = ".$i."";
            $result = mysqli_query($conn, $sql);
            mysqli_free_result($result);
        }
        else{
            $sql = "UPDATE ".$gponum." SET `starttime` = \"".$starttimer."\", `stoptime` = \"".$stoptimer."\" WHERE pk = ".$i."";
            $result = mysqli_query($conn, $sql);
            mysqli_free_result($result);
        }
    }
    mysqli_close($conn);
    // Alert user that timers have been changed
    echo "<script>alert('Timers Updated');document.location='/timers.php'</script>";
?>
