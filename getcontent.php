<?
//include ('g-auth.php');
$name=$_SERVER['PHP_SELF'];
$type = $_POST['type'];
$gnumber = $_POST['gnumber'];
$Tname = $_POST['Tname'];
$infofile = "task.txt";
$abbr1 = $_POST['faculties'];
	
//echo "$type \r\n $gnumber \r\n $Tname \r\n $abbr1  ";

if (!file_exists($infofile)) 
	{
		$file = fopen($infofile,"w+");
		if (!$Tname)
		{
			fwrite($file, $type ."\r\n" .$gnumber."\r\n".$abbr1);
		}
		else
		{
			fwrite($file, $type ."\r\n" .$Tname."\r\n".$abbr1);
		}
			
		fclose($file);
	}

else
	{
		$file = fopen($infofile,"r+");
		file_put_contents($infofile, ' ');
		if (!$Tname)
		{
			fwrite($file, $type ."\r\n".$gnumber."\r\n" .$abbr1);	
		}
		else
		{
			fwrite($file, $type ."\r\n" .$Tname."\r\n" .$abbr1);
		}
					
		fclose($file);
	}
	
	shell_exec('python geturlcontent.py 2>&1');
	
	
?>