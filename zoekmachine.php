<html>
<body>

<form action="zoekmachine.php" method="post">
  <input type="text" name="keyword">
  <input type="submit" value="Search!">
</form>

</body>
</html>


<?php
$servername = "localhost";
$username = "root";
$password = "root";

if(!empty($_POST['keyword']))
{
	$output = passthru("python finalass.py ".$_POST['keyword']);
	echo $output;
}