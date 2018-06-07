<?php

	session_start();
	
	if (!isset($_SESSION['zalogowany']))
	{
		header('Location: index.php');
		exit();
	}
	
	echo "<a href='mainPage.php' class='footerlink'><div class='out'>";
	echo "<p align='center'> [ Powrót ]</p>";
	echo "</div> </a> <div style='clear: both;'></div>";
	
?>
<!DOCTYPE HTML>
<html lang="pl">
	<head>
		<meta charset="utf-8" />
		<title>Strona główna</title>
		<meta name="description" content="Serwer zajmujący się zbieraniem danych o zgrzewarce" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
		<link href="style_css.css" rel="stylesheet" type="text/css" />
		<link href="css/fontello.css" rel="stylesheet" type="text/css" />
		<link href="https://fonts.googleapis.com/css?family=Josefin+Sans|Lato&amp;subset=latin-ext" rel="stylesheet">
		
		
		<style>
			.error
			{
				color:red;
			}
			.message
			{
				color:green;
			}
		</style>
	</head>

<body>	
		<form  action="pwm.php"  method="post">
		<?php
			echo '<br/> <input type="checkbox" name="PWM"/> PWM <br/>';
			echo '<input type="checkbox" name="czas"/> CZAS <br/>';
			echo '<input type="checkbox" name="maxI"/> max Prąd <br/><br/>';
			echo '<input type="submit" value="dalej">';
		?>
	</form>

</body>
</html>
