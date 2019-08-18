<?php
// TOP_MENU.PHP
echo "        \n<body onload=\"updateClock(); setInterval('updateClock()', 1000);\">
        <!-- Fixed navbar -->
        <nav class=\"navbar navbar-dark navbar-expand-md sticky-top\" style= \"background-color:#033C73\">
            <div class=\"container\">
                <a class=\"navbar-brand\" href=\"/index.php\"><img src=\"Images/HydroPi Logo.png\" width=\"54\" height=\"28\" alt=\"HydroPi Home Link\"></a>
                
                <span class=\"navbar-text text-light mr-auto\">
                    <span class=\"clock\" id=\"myday\"></span>
                    &nbsp;
                    <span class=\"clock\" id=\"mydate\">
                    &nbsp;
                    </span>
                    <span class=\"clock\" id=\"mytime\">
                    &nbsp;
                    </span>
                </span>
                <button class=\"navbar-toggler\" type=\"button\" data-toggle=\"collapse\" data-target=\"#navbar\" aria-expanded=\"false\" aria-controls=\"navbar\" aria-label=\"Toggle navigation\">
                    <span class=\"navbar-toggler-icon\"></span>
                </button>
                <div class=\"collapse navbar-collapse\" id=\"navbar\">
                    <ul class=\"navbar-nav ml-auto\">
                        <li class=\"nav-item\">
                            <a class=\"nav-link\" href=\"index.php\">Home</a></li>
                        <li class=\"nav-item\">
                            <a class=\"nav-link\" href=\"graphs.php\">Graphs</a></li>
                        <li class=\"nav-item\">
                            <a class=\"nav-link\" href=\"timers.php\">Timers</a></li>
                        <li class=\"nav-item\">
                            <a class=\"nav-link\" href=\"dosage.php\">Dosage</a></li>
                        <li class=\"nav-item\">
                            <a class=\"nav-link\" href=\"settings.php\">Settings</a></li>
                        <li class=\"nav-item\">
                            <a class=\"nav-link\" href=\"https://hydropi.dombold.com/phpmyadmin/\">Database</a></li>
                    </ul>
                </div><!--.nav-collapse -->
            </div>
        </nav>
        <div class=\"col-lg-12\" style=padding-top:90px;>
        </div>\n";
?>
