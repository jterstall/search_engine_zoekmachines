<html>
<body>

<form action="zoekmachine.php" method="post">
  <input type="text" name="keyword">
  Title
  <input type="checkbox" name="titleform" value="Yes" />
  Text
  <input type="checkbox" name="textform" value="Yes" />
  <input type="submit" value="Search!"> </br>
  <p>
  What year?
  <select name="formYear">
    <option value="0">All</option>
    <option value="1918">1918</option>
    <option value="1922">1922</option>
    <option value="1923">1923</option>
    <option value="1951">1951</option>
    <option value="1961">1961</option>
    <option value="1962">1962</option>
    <option value="1963">1963</option>
    <option value="1965">1965</option>
    <option value="1966">1966</option>
    <option value="1967">1967</option>
    <option value="1968">1968</option>
    <option value="1969">1969</option>
    <option value="1970">1970</option>
    <option value="1971">1971</option>
    <option value="1972">1972</option>
    <option value="1973">1973</option>
    <option value="1974">1974</option>
    <option value="1975">1975</option>
    <option value="1976">1976</option>
    <option value="1977">1977</option>
    <option value="1978">1978</option>
    <option value="1979">1979</option>
    <option value="1980">1980</option>
    <option value="1981">1981</option>
    <option value="1982">1982</option>
    <option value="1983">1983</option>
    <option value="1984">1984</option>
    <option value="1985">1985</option>
    <option value="1986">1986</option>
    <option value="1987">1987</option>
    <option value="1988">1988</option>
    <option value="1989">1989</option>
    <option value="1990">1990</option>
    <option value="1991">1991</option>
    <option value="1992">1992</option>
    <option value="1993">1993</option>
    <option value="1994">1994</option>
  </select>
  </p>
</form>
</body>
</html>



<?php
$servername = "localhost";
$username = "root";
$password = "root";

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
  $yearvar = $_POST['formYear'];
  $output = passthru("python finalass.py ".$_POST['keyword']." ".$title." ".$text." ".$yearvar);
}