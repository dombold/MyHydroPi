function Delete_MySQL(timeinterval) {
    if (timeinterval > 1){
        if (confirm("Are you sure you want to delete records older than "+timeinterval+" days?") == true){
            $.ajax({
                url: "/php/delete_sensors.php",
                type: "POST",
                data: {newtime: timeinterval},
            });
            window.alert("All Data Older than "+timeinterval+" Days has been cleared from the Sensors Log");
        }
        else {
            window.alert("Delete Aborted.");
        }
    }
    else if (timeinterval < 1) {
        if (confirm("Are you sure you want to delete all the records?") == true){
        $.ajax({
            url: "/php/delete_sensors.php",
            type: "POST",
            data: {newtime: timeinterval},
        });
        window.alert("All Data has been cleared from the Sensors Log");
        }
        else {
            window.alert("Delete Aborted.");
        }
    }
}

function Restart() {

    if (confirm("Are you sure you want to restart?") == true){
        window.alert("The HydroPi is Restarting");
        $.ajax({
            url: "/php/restart.php",
            type: "POST",
        });
    }
    else {
        window.alert("Restart Aborted.");
    }
}
function Shutdown() {

    if (confirm("Are you sure you want to Shutdown?") == true){
        window.alert("The HydroPi is Shutting Down. It is now safe to turn off the Power");
        $.ajax({
            url: "/php/shutdown.php",
            type: "POST",
        });
    }
    else {
        window.alert("Shutdown Aborted.");
    }
}

function set_power_state(gpo_state, gpo_number){

  //Call PHP script to update mySQL with the new value

  $.ajax({
    url: "php/power_update.php",
    type: "POST",
    data: {new_gpo_state: gpo_state, selected_gpo: gpo_number}
  });

  //Update webpage with new background colors to indicate the current state
    if(gpo_state=='off'){
        document.getElementById(gpo_number + "_state").style.backgroundColor = "#e12b31";
        document.getElementById(gpo_number + "_curr").innerHTML = "Off";
        document.getElementById(gpo_number + "_curr").style.color = "#e12b31";
      };
    if(gpo_state=='on'){
        document.getElementById(gpo_number + "_state").style.backgroundColor = "#88c149";
        document.getElementById(gpo_number + "_curr").innerHTML = "On";
        document.getElementById(gpo_number + "_curr").style.color = "#88c149";
      };
    if(gpo_state=='auto'){
        document.getElementById(gpo_number + "_state").style.backgroundColor = "#ff6707";
        document.getElementById(gpo_number + "_curr").innerHTML = "???";
        document.getElementById(gpo_number + "_curr").style.color = "#ff6707";
        $.ajax({
        url: "php/gpio_state.php",
        type: "POST",
        data: {new_gpo_state: gpo_state, selected_gpo: gpo_number}
        }).done(function(curr_state) {
            if (curr_state == 0) {
                document.getElementById(gpo_number + "_curr").innerHTML = "Off";
                document.getElementById(gpo_number + "_curr").style.color = "#e12b31";
            }
            else if (curr_state == 1) {
                document.getElementById(gpo_number + "_curr").innerHTML = "On";
                document.getElementById(gpo_number + "_curr").style.color = "#88c149";
            }
            });
    };
}

function chemical_check_cya(pool_size){
    var test_value = document.getElementById("cya_input").value;
    if (test_value >= 30 && test_value <= 50){
        document.getElementById("cya_action").innerHTML = "OK" ;
        document.getElementById("cya_input").value = "" ;
    }
    else if (test_value > 50){
        document.getElementById("cya_action").innerHTML = "Remove some water and add Fresh Water";
    }
    else if(test_value < 30){
      var add_stabliser = ((40-test_value)*(0.001*pool_size));
      document.getElementById("cya_action").innerHTML = "Add " + add_stabliser + "g of stabliser."
    }
    document.getElementById("cya_input").value = "" ;
}
function chemical_check_ta(pool_size){
    var test_value = document.getElementById("ta_input").value;
    if (test_value >= 80 && test_value <= 150){
        document.getElementById("ta_action").innerHTML = "OK" ;
    }
    else if (test_value > 150){
        document.getElementById("ta_action").innerHTML = "Remove some water and add Fresh Water";
    }
    else if(test_value < 80){
      var add_alk = ((115-test_value)*(0.001*pool_size));
      document.getElementById("ta_action").innerHTML = "Add " + add_alk + "g of AlkPlus.";
    }
    document.getElementById("ta_input").value = "" ;
}
function chemical_check_tcl(pool_size){
    var test_value = document.getElementById("tcl_input").value;
    if (test_value >= 3 && test_value <= 5){
        document.getElementById("tcl_action").innerHTML = "OK" ;
    }
    else if (test_value > 5){
        document.getElementById("tcl_action").innerHTML = "Remove some water and add Fresh Water";
    }
    else if(test_value < 3){
      var add_chlorine = ((4-test_value)*(0.001*pool_size));
      document.getElementById("tcl_action").innerHTML = "Add " + add_chlorine + "g of Chlorine.";
    }
    document.getElementById("tcl_input").value = "" ;
}
function chemical_check_ch(pool_size){
    var test_value = document.getElementById("ch_input").value;
    if (test_value >= 150 && test_value <= 250){
        document.getElementById("ch_action").innerHTML = "OK" ;
    }
    else if (test_value > 250){
        document.getElementById("ch_action").innerHTML = "Remove some water and add Fresh Water";
    }
    else if(test_value < 150){
      var add_cal_plus = ((200-test_value)*(0.001*pool_size));
      document.getElementById("ch_action").innerHTML = "Add " + add_cal_plus + "g of CalPlus.";
    }
    document.getElementById("ch_input").value = "" ;
}
function clear_dosage(){
    document.getElementById("cya_input").value = "" ;
    document.getElementById("ta_input").value = "" ;
    document.getElementById("tcl_input").value = "" ;
    document.getElementById("ch_input").value = "" ;
    document.getElementById("cya_action").innerHTML = "" ;
    document.getElementById("ta_action").innerHTML = "" ;
    document.getElementById("tcl_action").innerHTML = "" ;
    document.getElementById("ch_action").innerHTML = "" ;
    }

function set_pause_state(){

  //Call PHP script to update mySQL with the new value

  $.ajax({
    url: "php/update_pause.php",
    type: "POST"
  });
  document.getElementById("pause_state").innerHTML = "Sensor Readings Paused";
  document.getElementById("pause_state").className = "btn btn-md btn-danger";
}

function drawChart(timeinterval) {  
    $.ajax({
        url: "php/get_graph.php",
        type: "POST",
        data: {newtimeframe: timeinterval, sensor: "ds18b20_temp", label: "Temp"},
        dataType: "json",
        success: function (jsonData) {
            // Create our data table out of JSON data loaded from server.
            var data =new google.visualization.DataTable(jsonData);
            var options = {
            title: 'Air Temperature',
            curveType: 'function'
            };
            var chart = new google.visualization.LineChart(document.getElementById('ds18b20_temp_graph'));
            chart.draw(data, options);
        }
    });
    $.ajax({
        url: "php/get_graph.php",
        type: "POST",
        data: {newtimeframe: timeinterval, sensor: "atlas_temp", label: "Temp"},
        dataType: "json",
        success: function (jsonData) {
            // Create our data table out of JSON data loaded from server.
            var data =new google.visualization.DataTable(jsonData);
            var options = {
            title: 'Pool Temperature',
            curveType: 'function'
            };
            var chart = new google.visualization.LineChart(document.getElementById('atlas_temp_graph'));
            chart.draw(data, options);
        }
    });

    $.ajax({
        url: "php/get_graph.php",
        type: "POST",
        data: {newtimeframe: timeinterval, sensor: "ph", label: "pH"},
        dataType: "json",
        success: function (jsonData) {
            // Create our data table out of JSON data loaded from server.
            var data =new google.visualization.DataTable(jsonData);
            var options = {
            title: 'pH',
            curveType: 'function'
            };
            var chart = new google.visualization.LineChart(document.getElementById('ph_graph'));
            chart.draw(data, options);
        }
    });
    $.ajax({
        url: "php/get_graph.php",
        type: "POST",
        data: {newtimeframe: timeinterval, sensor: "orp", label: "mV"},
        dataType: "json",
        success: function (jsonData) {
            // Create our data table out of JSON data loaded from server.
            var data =new google.visualization.DataTable(jsonData);
            var options = {
            title: 'Oxidation Reduction Potential',
            curveType: 'function'
            };
            var chart = new google.visualization.LineChart(document.getElementById('orp_graph'));
            chart.draw(data, options);
        }
    });
    $.ajax({
        url: "php/get_graph.php",
        type: "POST",
        data: {newtimeframe: timeinterval, sensor: "ec", label: "ppm"},
        dataType: "json",
        success: function (jsonData) {
            // Create our data table out of JSON data loaded from server.
            var data =new google.visualization.DataTable(jsonData);
            var options = {
            title: 'Salinity',
            curveType: 'function'
            };
            var chart = new google.visualization.LineChart(document.getElementById('ec_graph'));
            chart.draw(data, options);
        }
    });
}

function updateClock(){
  //Configure initial variables

  tday = new Array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday");
  tmonth = new Array("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec");
  var d = new Date();
  var nday = d.getDay(), nmonth = d.getMonth(), ndate = d.getDate(), nyear = d.getYear(), nhour = d.getHours(), nmin = d.getMinutes(), nsec = d.getSeconds(), ap;

      if(nhour==0)
      {ap = " AM"; nhour = 12;}
      else if(nhour<12)
      {ap = " AM";}
      else if(nhour==12)
      {ap = " PM";}
      else if(nhour>12)
      {ap = " PM"; nhour -= 12;}
      if(ndate<2 && ndate>0)
      {ndate += "<sup>st</sup>";}
      else if(ndate<3 && ndate>1)
      {ndate += "<sup>nd</sup>";}
      else if(ndate<4 && ndate>2)
      {ndate += "<sup>rd</sup>";}
      else
      {ndate += "<sup>th</sup>";}
      if(nyear<1000) nyear += 1900;
      if(nmin<=9) nmin = "0"+nmin;
      //if(nsec<=9) nsec = "0"+nsec;

  //Compose the string for display

  var currentDateString = tmonth[nmonth] + " " + ndate + ", " + nyear + " ";
  var currentDayString = tday[nday];
  var currentTimeString = nhour + ":" + nmin + " " + ap;

  document.getElementById("mydate").innerHTML = currentDateString;
  document.getElementById("myday").innerHTML = currentDayString;
  document.getElementById("mytime").innerHTML = currentTimeString;
}
