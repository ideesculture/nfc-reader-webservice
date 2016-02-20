<?php
	error_reporting(0);
	@ini_set('display_errors', 0);
	
	//print __DIR__;
	exec("cd ".__DIR__." && python NFCReader.py --read 8 2>&1", $output, $return_var);
	if (isset($output[2])) {
		if (strlen($output[2]) == 8) {
			print json_encode(array("result"=>"success", "value"=>$output[2]), JSON_PRETTY_PRINT);
		} else {
			print json_encode(array("result"=>"error", "value"=>$output[2]), JSON_PRETTY_PRINT);
		}
	} else {
		print json_encode(array("result"=>"crash"), JSON_PRETTY_PRINT);
	}
	//var_dump($output);