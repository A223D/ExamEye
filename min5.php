<?php
$myfile=fopen("time.txt", "w");
fwrite($myfile, 5);
fclose($myfile);
header('Refresh: 1; URL=http://exameye.000webhostapp.com/');
 ?>
