<!-- Tycho Koster, David Stap, Jeroen Terstall -->

<html>
<body>

<form action="assignment_week_5.php" method="post">
  <input type="text" placeholder="jaar" name="jaar">
  <input type="text" placeholder="partij" name="partij">
  <input type="text" placeholder="ministerie" name="ministerie">
  <input type="int" placeholder="aantal deelvragen" name="aantal_deelvragen">
  <input type="submit" value="Search!">
</form>

</body>
</html>


<?php
$servername = "localhost";
$username = "root";
$password = "root";

if(!empty($_POST['jaar']) || !empty($_POST['partij']) || !empty($_POST['ministerie']) || !empty($_POST['aantal_deelvragen']))
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
      $query = $conn->prepare('SELECT *, MATCH(jaar, partij, ministerie, aantal_deelvragen) AGAINST(:jaar, :partij, :ministerie, :aantal_deelvragen) AS score FROM `kamervragen` WHERE MATCH(jaar, partij, ministerie, aantal_deelvragen) AGAINST(:jaar, :partij, :ministerie, :aantal_deelvragen) ORDER BY score DESC');
      $query->execute(array(':jaar' => $_POST['jaar'],
                            ':partij' => $_POST['partij'],
                            'ministerie' => $_POST['ministerie'],
                            'aantal_deelvragen' => $_POST['aantal_deelvragen']));
      $res = $query->fetchAll();
      foreach($res as $value)
      {
        print_r("Titel: " . $value['titel']);
        echo "<br />\n";
      }
}
?>
