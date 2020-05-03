<?php
$myfile=fopen("time.txt", "w");
fwrite($myfile, 10);
fclose($myfile);
header('Refresh: 1; URL=http://exameye.000webhostapp.com/');
 ?>
