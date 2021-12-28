<?
header('Location: page.html');

$name=$_SERVER['PHP_SELF'];
$type = $_POST['user'];
$gnumber = $_POST['gnumber'];
$Tname = $_POST['Tname'];
$infofile = "task.txt";
$abbr1 = $_POST['faculties'];
$sdate = $_POST['startdate'];
$edate = $_POST['enddate'];
$comment = $_POST['comment'];

echo "$type \r\n $gnumber \r\n $Tname \r\n $abbr1 $sdate  $edate $comment ";
if(isset($_POST['Ntf'])){
	$ntf = 'True';
}
else $ntf = 'False';

if (!file_exists($infofile)) 
	{
		$file = fopen($infofile,"w+");
		if (!$Tname)
		{
			fwrite($file, $type ."\r\n" .$gnumber."\r\n".$abbr1."\r\n".$sdate."\r\n".$edate."\r\n".$ntf."\r\n".$comment);
		}
		else
		{
			fwrite($file, $type ."\r\n" .$Tname."\r\n".$abbr1."\r\n".$sdate."\r\n".$edate."\r\n".$ntf."\r\n".$comment);
		}
			
		fclose($file);
	}

else
	{
		$file = fopen($infofile,"r+");
		file_put_contents($infofile, ' ');
		if (!$Tname)
		{
			fwrite($file, $type ."\r\n".$gnumber."\r\n" .$abbr1."\r\n".$sdate."\r\n".$edate."\r\n".$ntf."\r\n".$comment);	
		}
		else
		{
			fwrite($file, $type ."\r\n" .$Tname."\r\n" .$abbr1."\r\n".$sdate."\r\n".$edate."\r\n".$ntf."\r\n".$comment);
		}
					
		fclose($file);
	}
echo(shell_exec('python events_try1.py 2>&1'));
	

# echo "<HTML><HEAD>

# <META HTTP-EQUIV='Refresh' CONTENT='0; URL=page.html'>

# </HEAD></HTML>";
?>