<!DOCTYPE html>
<html>
<head>
<style>
body {
  color: white;
  text-align: center;
}

h1 {
  color: white;
  text-align: center;
}
</style>
</head>
<body>
<h1 style="color:White;">Zambretti Forecast</h1>
<?php
$myfile = fopen("forecast.txt", "r") or die("Unable to open file!");
echo fgets($myfile);
fclose($myfile);
?>
<br>
<body style="background-color:black;">
<center><img src="graph1.png"/><br><img src="graph2.png"/><br><img src="graph3.png"/></center>
</body>
</html>