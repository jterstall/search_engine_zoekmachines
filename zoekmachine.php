  <html>
  <body>

  <form action="zoekmachine.php" method="post">
    <input type="text" name="keyword">
    Title
    <input type="checkbox" name="titleform" value="Yes" />
    Text
    <input type="checkbox" name="textform" value="Yes" />
    <input type="submit" value="Search!">
  </form>
  </body>
  </html>



<?php
if(!empty($_POST['keyword']))
{
	if(isset($_POST['titleform']) && $_POST['titleform'] == 'Yes'){
		$title = 'Yes';
	}
	else {
		$title = 'No';
	}
	if(isset($_POST['textform']) && $_POST['textform'] == 'Yes'){
		$text = 'Yes';
	}
	else {
		$text = 'No';
	}
  $year = "1972";
    $output = passthru("/usr/bin/python /var/www/html/finalass.py ".$_POST['keyword']." ".$title." ".$text . " ".$year);
    echo $output;
}
?>
