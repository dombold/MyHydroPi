<?php
// TOP_MENU.PHP
echo "        \n<body onload=\"updateClock(); setInterval('updateClock()', 1000);\">
        <!-- Fixed navbar -->
        <nav class=\"navbar navbar-inverse navbar-fixed-top\">
            <div class=\"container\">
                <div class=\"navbar-header\">
                    <button type=\"button\" class=\"navbar-toggle collapsed\" data-toggle=\"collapse\" data-target=\"#navbar\" aria-expanded=\"false\" aria-controls=\"navbar\">
                    <span class=\"sr-only\">Toggle navigation</span>
                    <span class=\"icon-bar\"></span>
                    <span class=\"icon-bar\"></span>
                    <span class=\"icon-bar\"></span>
                    </button>
                    <a class=\"navbar-brand\" href=\"/index.php\"><img src=\"Images/HydroPi Logo.png\" width=\"54\" height=\"28\" alt=\"HydroPi Home Link\"></a>
                    <div class=\"navbar-text\"><span class=\"clock\" id=\"myday\"></span>&nbsp;<span class=\"clock\" id=\"mydate\">&nbsp;</span><span class=\"clock\" id=\"mytime\">&nbsp;</span>
                    </div>
                </div>
                <div id=\"navbar\" class=\"navbar-collapse collapse navbar-right\">
                    <ul class=\"nav navbar-nav\">
                        <li><a href=\"index.php\">Home</a></li>
                        <li><a href=\"graphs.php\">Graphs</a></li>
                        <li><a href=\"timers.php\">Timers</a></li>
                        <li><a href=\"dosage.php\">Dosage</a></li>
                        <li><a href=\"settings.php\">Settings</a></li>
                    </ul>
                </div><!--.nav-collapse -->
            </div>
        </nav>
        <div class=\"col-lg-12\" style=padding-top:90px;>
        </div>\n";
?>
