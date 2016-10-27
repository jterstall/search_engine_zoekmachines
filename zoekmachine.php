<html>
<body>

<form action="zoekmachine.php" method="post">
  <input type="text" name="keyword">
  <input type="submit" value="Search!">
</form>

</body>
</html>


<?php
if(!empty($_POST['keyword']))
{
	$output = passthru("python3 finalass.py ". $_POST['keyword']);
	echo $output;
}
