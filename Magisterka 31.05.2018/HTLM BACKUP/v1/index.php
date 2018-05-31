<?php

	session_start();
	
	if ((isset($_SESSION['zalogowany'])) && ($_SESSION['zalogowany']==true))
	{
		header('Location: mainPage.php');
		exit();
	}

?>

<!DOCTYPE HTML>
<html lang="pl">
	<head>
		<meta charset="utf-8" />
		<title>Strona logowania</title>
		<meta name="description" content="Serwer zajmujący się zbieraniem danych o zgrzewarce" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
		
		<link href="style_css.css" rel="stylesheet" type="text/css" />
		<link href="css/fontello.css" rel="stylesheet" type="text/css" />
		<link href="https://fonts.googleapis.com/css?family=Josefin+Sans|Lato&amp;subset=latin-ext" rel="stylesheet">
		
	</head>

<body>
	
	<h1 align="center">EKRAN LOGOWANIA</h1> <br /><br />
		<form action="zaloguj.php" method="post">
			
			<h5 align="center">
				LOGIN: <br/>
				<input type="text" name="login" />
				<br/><br/>
				HASŁO: <br/>
				<input type="password" name="haslo" />
				<br/><br/>
				<input type="submit" value="ZALOGUJ" />
			</h5>
		</form>
	
<?php
	if(isset($_SESSION['blad']))	echo '<h3 align="center">'.$_SESSION['blad']."</h3>";
?>

</body>
</html>