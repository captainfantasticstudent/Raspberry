<?php

	session_start();
	
	if (!isset($_SESSION['zalogowany']))
	{
		header('Location: index.php');
		exit();
	}
	
	require_once "connect.php";
	
	if(isset($_POST['fill']) || isset($_POST['time']) || isset($_POST['fill1']) || isset($_POST['time1']) || isset($_POST['MaxI2']) || isset($_POST['time_z']))
	{	
		$polaczenie = @new mysqli($host, $db_user, $db_password, $db_name2);
		if(isset($_POST['fill']) && strlen($_POST['fill']) > 0){	
			$wszystko_ok = true;
			$fill = $_POST['fill'];
			if(strlen($fill) > 2 || strlen($fill) < 1)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_pwm'] = 'Nieprawidłowa wartość! PWM prawidłowo od 0 do 99!';
				
			}
			elseif(ctype_digit($fill)==false)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_pwm'] = 'Wypełnienie PWM1 nie jest liczbą!';
			}
			if($wszystko_ok == true)
			{
				if ($polaczenie->connect_errno!=0) {
					$_SESSION['e_message_pwm'] = "Error: ".$polaczenie->connect_errno;
				}
				else {
					$SQL_query = "UPDATE parametry SET PWM=".$fill." WHERE id=1";
					@$polaczenie->query($SQL_query);
					$_SESSION['e_message_pwm'] = '<div class="message">UDANE WPISANIE WARTOŚCI PWM DO BAZY</div>';
					
				}
			}
		}
		if(isset($_POST['time']) && strlen($_POST['time']) > 0){	
			$wszystko_ok = true;
			$time = $_POST['time'];
			if(strlen($time) > 3 || strlen($time) < 1)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_czas'] = 'Nieprawidłowa wartość! czas prawidłowo od 0 do 999!';
				
			}
			elseif(ctype_digit($time)==false)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_czas'] = 'Czas nie jest liczbą!';
			}
			if($wszystko_ok == true)
			{
				if ($polaczenie->connect_errno!=0) {
					$_SESSION['e_message_czas'] = "Error: ".$polaczenie->connect_errno;
				}
				else {
					$SQL_query = "UPDATE parametry SET czas=".$time." WHERE id=1";
					@$polaczenie->query($SQL_query);
					$_SESSION['e_message_czas'] = '<div class="message">UDANE WPISANIE WARTOŚCI czas DO BAZY</div>';
					
				}
			}
		}
		
		if(isset($_POST['fill1']) && strlen($_POST['fill1']) > 0){	
			$wszystko_ok = true;
			$fill1 = $_POST['fill1'];
			if(strlen($fill1) > 2 || strlen($fill1) < 1)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_pwm1'] = 'Nieprawidłowa wartość! PWM1 prawidłowo od 0 do 99!';
				
			}
			elseif(ctype_digit($fill1)==false)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_pwm1'] = 'Wypełnienie PWM1 nie jest liczbą!';
			}
			if($wszystko_ok == true)
			{
				if ($polaczenie->connect_errno!=0) {
					$_SESSION['e_message_pwm1'] = "Error: ".$polaczenie->connect_errno;
				}
				else {
					$SQL_query = "UPDATE parametry SET PWM1=".$fill1." WHERE id=1";
					@$polaczenie->query($SQL_query);
					$_SESSION['e_message_pwm1'] = '<div class="message">UDANE WPISANIE WARTOŚCI PWM1 DO BAZY</div>';
					
				}
			}
		}
		if(isset($_POST['time1']) && strlen($_POST['time1']) > 0){	
			if ($rezultat = @$polaczenie->query("SELECT * FROM parametry WHERE id=1")) {
				$wiersz = $rezultat->fetch_assoc();
				$czas = $wiersz['czas'];
				$rezultat->free_result();
			}
				
			$wszystko_ok = true;
			$time1 = $_POST['time1'];	
			$czas1a = $czas + 0;
			$time1a = $time1 + 0;
			
			if(strlen($time1) > 3 || strlen($time1) < 1)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_czas1'] = 'Nieprawidłowa wartość! czas1 prawidłowo od 0 do 999!';
				
			}
			elseif(ctype_digit($time1)==false)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_czas1'] = 'Czas1 nie jest liczbą!';
			}
			elseif($time1a <= $czas1a and $time1a != 0)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_czas1'] = 'Czas1 musi byc większy od Czas lub równy 0!';
			}
			if($wszystko_ok == true)
			{
				if ($polaczenie->connect_errno!=0) {
					$_SESSION['e_message_czas1'] = "Error: ".$polaczenie->connect_errno;
				}
				else {
					$SQL_query = "UPDATE parametry SET czas1=".$time1." WHERE id=1";
					@$polaczenie->query($SQL_query);
					$_SESSION['e_message_czas1'] = '<div class="message">UDANE WPISANIE WARTOŚCI czas DO BAZY</div>';
					
				}
			}
		}
		if(isset($_POST['time_z']) && strlen($_POST['time_z']) > 0){	
			$wszystko_ok = true;
			$time_z = $_POST['time_z'];
			if(strlen($time_z) > 3 || strlen($time_z) < 1)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_czas_z'] = 'Nieprawidłowa wartość! Czas_Z prawidłowo od 0 do 999!';
				
			}
			elseif(ctype_digit($time_z)==false)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_czas_z'] = 'Czas_Z nie jest liczbą!';
			}
			if($wszystko_ok == true)
			{
				if ($polaczenie->connect_errno!=0) {
					$_SESSION['e_message_czas_z'] = "Error: ".$polaczenie->connect_errno;
				}
				else {
					$SQL_query = "UPDATE parametry SET czas_z=".$time_z." WHERE id=1";
					@$polaczenie->query($SQL_query);
					$_SESSION['e_message_czas_z'] = '<div class="message">UDANE WPISANIE WARTOŚCI czas_z DO BAZY</div>';
					
				}
			}
		}
		if(isset($_POST['MaxI2']) && strlen($_POST['MaxI2']) > 0){	
			$wszystko_ok = true;
			$MaxI = $_POST['MaxI2'];
			if(strlen($MaxI) > 3 || strlen($MaxI) < 1)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_MaxI'] = 'Nieprawidłowa wartość! Max prądu prawidłowo od 0 do 999!';
				
			}
			elseif(ctype_digit($MaxI)==false)
			{
				$wszystko_ok = false;
				$_SESSION['e_message_MaxI'] = 'Maksymalny prąd nie jest liczbą!';
			}
			if($wszystko_ok == true)
			{
				if ($polaczenie->connect_errno!=0) {
					$_SESSION['e_message_MaxI'] = "Error: ".$polaczenie->connect_errno;
				}
				else {
					$SQL_query = "UPDATE parametry SET MaxI=".$MaxI." WHERE id=1";
					@$polaczenie->query($SQL_query);
					$_SESSION['e_message_MaxI'] = '<div class="message">UDANE WPISANIE WARTOŚCI Max prądu DO BAZY</div>';
					
				}
			}
		}
		
		if ($rezultat = @$polaczenie->query("SELECT * FROM parametry WHERE id=1")) {
			$wiersz = $rezultat->fetch_assoc();
			$czas = $wiersz['czas'];
			$czas1 = $wiersz['czas1'];
			$time_z = $wiersz['czas_z'];
			$rezultat->free_result();
		}
		$czas1a = $czas + 0;
		$czas2a = $czas1 + 0;
		$time_za = $time_z + 0;
		$czas_a1 = $czas1a + $time_za;
		$czas_a2 = $czas2a - $czas_a1;
		
		if($czas_a2 <= 0 && $czas2a > 0)
		{
			$time_za = $czas1 - $czas - 1;
			echo $time_za."</br>";
			$_SESSION['e_message_czas_z'] = 'Czas_Z za duży! Zmniejszono wartośc do dozwolonej';
			$SQL_query = "UPDATE parametry SET czas_z=".$time_za." WHERE id=1";
			@$polaczenie->query($SQL_query);
		}
		elseif((999 - $czas_a1) < 0){
			$time_za = 999 - $czas1a;
			$_SESSION['e_message_czas_z'] = 'Czas_Z za duży! Zmniejszono wartośc do dozwolonej';
			$SQL_query = "UPDATE parametry SET czas_z=".$time_za." WHERE id=1";
			@$polaczenie->query($SQL_query);
		}
		
		
		
		$SQL_query = "UPDATE parametry SET START = 0 WHERE id=1";
		@$polaczenie->query($SQL_query);
		$polaczenie->close();
	}
	elseif(isset($_POST['start']))
	{
		$polaczenie = @new mysqli($host, $db_user, $db_password, $db_name2);
		
		if ($rezultat = @$polaczenie->query("SELECT * FROM parametry WHERE id=1")) {
			$wiersz = $rezultat->fetch_assoc();
			$gotowe = $wiersz['GOTOWE'];
			$gotowe = $gotowe + 0;
			$rezultat->free_result();
		}
		if ($polaczenie->connect_errno!=0) {
			$_SESSION['e_message_start'] = "Error: ".$polaczenie->connect_errno;
		}
		elseif ($gotowe == 0) {
			$_SESSION['e_message_start'] = 'ZGRZEWARKA NIEGOTOWA!';
		}
		else {
			$SQL_query = "UPDATE parametry SET Start=1 WHERE id=1";
			@$polaczenie->query($SQL_query);
			$_SESSION['e_message_start'] = '<div class="message">WYSŁANO SYGNAŁ STARTU DO ZGRZEWARKI</div><br/>';
			$polaczenie->close();
		}
	}
	else
	{
		$_SESSION['e_message'] = '<div class="error">NIE PODJĘTO ŻADNEJ AKCJI</div><br/>';
		$polaczenie = @new mysqli($host, $db_user, $db_password, $db_name2);
		$SQL_query = "UPDATE parametry SET Start=0 WHERE id=1";
		@$polaczenie->query($SQL_query);
		$polaczenie->close();
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
		
		
		<style>
			.error
			{
				color: red;
				font-size: small;
			}
			.message
			{
				color: green;
				font-size: small;
			}
		</style>
	</head>

<body>
	
	<div id="container3">
		<a href='mainPage.php' class='footerlink'><div class='out'>
			<p align='center'> [ Powrót ]</p>
		</div> </a> <div style='clear: both;'></div>
		
		<div class="square_big">

			<?php	
				$polaczenie = @new mysqli($host, $db_user, $db_password, $db_name2);
				if ($polaczenie->connect_errno!=0) {
					echo "Error: ".$polaczenie->connect_errno;
				}
				else {
					if ($rezultat = @$polaczenie->query("SELECT * FROM parametry WHERE id=1"))
					{
						$liczba_wierszy = $rezultat->num_rows;
						if($liczba_wierszy>0) {
							$wiersz = $rezultat->fetch_assoc();
							$pwm = $wiersz['PWM'];
							$czas = $wiersz['czas'];
							$gotowe = $wiersz['GOTOWE'];
							$pwm1 = $wiersz['PWM1'];
							$czas1 = $wiersz['czas1'];
							$czas_z = $wiersz['czas_z'];
							$start = $wiersz['START'];
							$MaxI = $wiersz['MaxI'];
							$rezultat->free_result();
							
							if ($czas1 < $czas) {
								$SQL_query = "UPDATE parametry SET czas1=0 WHERE id=1";
								@$polaczenie->query($SQL_query);
								$czas1 = 0;
							}
							
							echo "<h5>Wartości zapisane w BAZIE DANYCH ZGRZEWRKI</h5>";
							echo "<table border='3' align='center'>";
							echo	"<tr>";
							echo		"<td width='200'>PWM</td> <td width='100'>".$pwm."</td>";
							echo	"</tr>";
							echo	"<tr>";
							echo		"<td>CZAS</td> <td>".$czas."</td>";
							echo	"</tr>";
							echo	"<tr>";
							echo		"<td>PWM1</td> <td>".$pwm1."</td>";
							echo	"</tr>";
							echo	"<tr>";
							echo		"<td>CZAS1</td> <td>".$czas1."</td>";
							echo	"</tr>";
							echo	"<tr>";
							echo		"<td>Czas_Z - Czas martwy</td> <td>".$czas_z."</td>";
							echo	"</tr>";
							echo	"<tr>";
							echo		"<td>Max prąd (x 100 A)</td> <td>".$MaxI."</td>";
							echo	"</tr>";
							echo	"<tr>";
							echo	"<tr>";
							echo		"<td>GOTOWOŚĆ</td> <td>".$gotowe."</td>";
							echo	"</tr>";
							echo	"<tr>";
							echo		"<td>START</td> <td>".$start."</td>";
							echo	"</tr>";
							echo "</table> </br>";
							
							echo '<form action="pwm.php" method="post">	';
							echo 	'<input type="submit" value="ODŚWIEŻ TABELĘ" />';
							echo '</form>';
							echo '</br>';
						} 
						else {
							echo "BLAD";
						}
					}
					$polaczenie->close();
				}
			?>
		
			<form method="post">
				PWM 	<br/> <input type="text" name="fill"/> <br/>
				Czas	<br/> <input type="text" name="time"/> <br/>
				PWM1	<br/> <input type="text" name="fill1"/> <br/>
				Czas1 	<br/> <input type="text" name="time1"/> <br/>
				Czas_Z 	<br/> <input type="text" name="time_z"/> <br/>
				Max prąd (x 100 A) 	<br/> <input type="text" name="MaxI2"/> <br/>
				<input type="submit" value="Wyślij dane do zgrzewarki"> <br/>
			</form>
			
			<form method="post">
				<?php
					echo '<br/> <input type="checkbox" name="start"/> Start zgrzewania <br/>';
					echo '<input type="submit" value="Start zgrzewarki">';
				?>
			</form>
		
		</div>
		
		<div class="square_big2">
			<h5>INFORMACJE/BŁĘDY</h5>
			<?php
				if(isset($_SESSION['e_message_pwm']))
				{
					echo '<div class="error">'.$_SESSION['e_message_pwm'].'</div>';
					unset($_SESSION['e_message_pwm']);
				}
				if(isset($_SESSION['e_message_pwm1']))
				{
					echo '<div class="error">'.$_SESSION['e_message_pwm1'].'</div>';
					unset($_SESSION['e_message_pwm1']);
				}
				if(isset($_SESSION['e_message_start']))
				{
					echo '<div class="error">'.$_SESSION['e_message_start'].'</div>';
					unset($_SESSION['e_message_start']);
				}
				if(isset($_SESSION['e_message']))
				{
					echo '<div class="error">'.$_SESSION['e_message'].'</div>';
					unset($_SESSION['e_message']);
				}
				if(isset($_SESSION['e_message_czas']))
				{
					echo '<div class="error">'.$_SESSION['e_message_czas'].'</div>';
					unset($_SESSION['e_message_czas']);
				}
				if(isset($_SESSION['e_message_czas1']))
				{
					echo '<div class="error">'.$_SESSION['e_message_czas1'].'</div>';
					unset($_SESSION['e_message_czas1']);
				}
				if(isset($_SESSION['e_message_MaxI']))
				{
					echo '<div class="error">'.$_SESSION['e_message_MaxI'].'</div>';
					unset($_SESSION['e_message_MaxI']);
				}
				if(isset($_SESSION['e_message_czas_z']))
				{
					echo '<div class="error">'.$_SESSION['e_message_czas_z'].'</div>';
					unset($_SESSION['e_message_czas_z']);
				}
			?>
		</div>
		<div class="square_big3">
			<h5>POMOC/SCHEMAT DZIAŁANIA</h5>
			<img src="img/help_new.png" alt="HELPPWM" width="300" />
			<p align="justify"> 
				<font size=3> 
					&nbsp Proszę wybrać wypełnienie sygnału<font color="red"> PWM i CZAS TRWANIA</font>. zgrzewania o danym
					wypełnieniu (Rys. powyżej). Akceptowalna wartość PWM to zakres od <font color="red">0 do 99</font>. <br/>
					&nbsp Czas trwania zadawania sygnału PWM podawany jest w mikisekundach. <br/>
					&nbsp Łączny czas zgrzewania (CZAS lub CZAS1) <font color="red">nie może przekraczać 1000 ms</font>. <br/>
					&nbsp Jeżeli Czas_Z będzie równy <font color="red">0</font> to przerwa pomiędzy progami PWM nie będzie uwzględniana. <br/>
					&nbsp Jeżeli Czas1 będzie równy <font color="red">0</font> sygnał będzie składał się tylko z jednego progu wypełnienia PWM.<br/>
				</font>
			</p>
		</div>
	</div>
</body>
</html>
