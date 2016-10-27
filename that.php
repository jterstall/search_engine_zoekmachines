<!-- Tycho Koster, David Stap, Jeroen Terstall -->

<html>
<body>

<form action="that.php" method="post">
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
  try {
      $conn = new PDO("mysql:host=$servername;dbname=zoekmachines", $username, $password);
      // set the PDO error mode to exception
      $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
      }
  catch(PDOException $e)
      {
      echo "Connection failed: " . $e->getMessage();
      }
      $query = $conn->prepare('SELECT *, MATCH(title, body) AGAINST (:keyword) AS score FROM `MyWebCollection` WHERE MATCH(title, body) AGAINST (:keyword) ORDER BY score DESC');
      $query->execute(array(':keyword' => $_POST['keyword']));
      $res = $query->fetchAll();
      foreach($res as $value)
      {
        print_r("Title: " . $value['TITLE'] . ", ");
        print_r("Score: " . $value['score'] . ", ");
        print_r("URL: ". $value['URL']);
        echo "<br />\n";
      }
}
?>
