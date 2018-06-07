<?php

	session_start();
	
	if (!isset($_SESSION['zalogowany']))
	{
		header('Location: index.php');
		exit();
	}
	
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
		
	</head>

<body onload="odliczanie();">
<?php
	echo "<a href='logout.php' class='footerlink'><div class='out'>";
	echo "<p align='center'> [ Wyloguj się! ]</p>";
	echo "</div> </a> <div style='clear: both;'></div>";
	echo "<div id='container'>";
	echo	"<div class='rectangle' style='text-align: right;'>";
	echo		"<div id='logo'>";
	echo			"<a href='index.html' class='footerlink'>";
	echo 				"Witaj ".$_SESSION['login'].'!';
	echo 			"<a>";
	echo		"</div>";
	echo	"</div>";
	
	
echo<<< END
			<div class="square">
				<div class="tile2">
					<a href="ftp://ftpuser:raspberry@192.168.1.72/download" class="tilelink2">
						<i class="icon-superscript"></i><br />
						Zebrane dane
					</a>
				</div>
			</div>
			
			<div class="square">
				<div class="tile22">
					<a href="pwm.php" class="tilelink2">
						<i class="icon-beaker"></i><br />
						Sterowanie zgrzewarką
					</a>
				</div>
			</div>
			<div style="clear: both;"></div>
		
			<div class="rectangle">
				<a href="http://www.littlewebhut.com/" target="_blank" title="littlewebhut.com"  class="footerlink">Przydatna strona o języku HTML</a>
			</div>
		</div>
		
END;
	
?>

</body>
</html>
