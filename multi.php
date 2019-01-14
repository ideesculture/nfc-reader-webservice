<?php
	error_reporting(0);
	ini_set('display_errors', 0);

	$content_type = 'application/json';
	$status = 200;
	$codes = Array(
		200 => 'OK',
		400 => 'Bad Request',
		401 => 'Unauthorized',
		402 => 'Payment Required',
		403 => 'Forbidden',
		404 => 'Not Found',
		500 => 'Internal Server Error',
		501 => 'Not Implemented',
	);

	header("Access-Control-Allow-Origin: *");
	header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");
	header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept, Authorization");
	header('Content-type: ' . $content_type);
	// set the status
	$status_header = 'HTTP/1.1 '.$status.' '.$codes[$status];
	header($status_header);


	if($_GET["write"] != 1 ) {

		// Get mode : reading value from NFC chip
		$vs_reading_line = 8;
		if (isset($_GET["line"]) && $_GET["line"] >= 0 && $_GET["line"] <= 8) {
			$vs_reading_line = $_GET["line"];
		}

		if (isset($_GET["usingreader"]) && $_GET["usingreader"] >= 0) {
			$vs_usingreader = " --usingreader " . $_GET["usingreader"];
		}

		$vs_command = "python NFCReader.py --read " . $vs_reading_line . $vs_usingreader . " 2>&1";
		if (PHP_OS == "Darwin") {
			$vs_command = "sudo " . $vs_command;
		}
		$vs_command = "cd " . __DIR__ . " && " . $vs_command;
		exec($vs_command, $output, $return_var);

		$result = array();
		// return reader used
		//$result["usingreader"] = substr($output[1], 9, 2) * 1;

		if (isset($output[0]) && substr($output[0], 0, 9) == "Traceback") {
			// Traceback return : we have a crash
			foreach ($output as $row) {
				if (substr($row, 0, 12) == "ImportError:") {
					$result["result"] = "crash";
					$result["hint"] = $row;
				}
				if (substr($row, 0, 29) == "smartcard.pcsc.PCSCExceptions") {
					$result["result"] = "crash";
					$result["hint"] = $row;
				}
			}
		} else {

			if (isset($output[0]) && substr($output[0], 0, 18) == "Available readers:") {
				$result["readers"] = substr($output[0], 19);
			}
			// Everything seems ok
			if (isset($output[2])) {
				$result["line"] = $vs_reading_line;
					$result["value"] = [];
					$dump=$output;
					unset($dump[0]);
					unset($dump[1]);
					$i=0;
					foreach($dump as $temp) {
						$pattern = '/^([0-9])\[([0-9]+)\] \| (.*)/';
						preg_match($pattern, $temp, $matches, PREG_OFFSET_CAPTURE);
						$value = array("reader"=>$matches[1][0], "line"=>$matches[2][0], "value"=>$matches[3][0]);
						$result["value"][$i]=$value;
						//print_r($matches);
						$i++;
					}
			} else {
				$result["result"] = "crash";
				$result["hint"] = "sorry. arg. only arg. no hint at all.";
			}
		}

		print json_encode($result, JSON_PRETTY_PRINT);
	} else {
		// Post mode : writing value to NFC chip

		$value = $_GET["value"];

		$vs_writing_line = 8;
		if (isset($_GET["line"]) && $_GET["line"] >= 0 && $_GET["line"] <= 8) {
			$vs_writing_line = $_GET["line"];
		}

		if (isset($_GET["usingreader"]) && $_GET["usingreader"] >= 0) {
			$vs_usingreader = " --usingreader " . $_GET["usingreader"];
		}

		$vs_command = "python NFCReaderMulti.py --write ". str_pad($vs_writing_line, 8)." ".$value. $vs_usingreader . " 2>&1";
		if (PHP_OS == "Darwin") {
			$vs_command = "sudo " . $vs_command;
		}
		$vs_command = "cd " . __DIR__ . " && " . $vs_command;
		exec($vs_command, $output, $return_var);
		$result = array();
		// return reader used
		//$result["usingreader"] = substr($output[1], 9, 2) * 1;

		if (isset($output[0]) && substr($output[0], 0, 9) == "Traceback") {
			// Traceback return : we have a crash
			foreach ($output as $row) {
				if (substr($row, 0, 12) == "ImportError:") {
					$result["result"] = "crash";
					$result["hint"] = $row;
				}
				if (substr($row, 0, 29) == "smartcard.pcsc.PCSCExceptions") {
					$result["result"] = "crash";
					$result["hint"] = $row;
				}
			}
		} else {

			if (isset($output[0]) && substr($output[0], 0, 18) == "Available readers:") {
				$result["readers"] = substr($output[0], 19);
			}
			// Everything seems ok
			if (isset($output[2])) {
				$result["line"] = $vs_writing_line;

				if (substr($output[2],0,5) == "Wrote") {
					$result["result"] = "success";
				} else {
					$result["result"] = "error";
				}
			} else {
				$result["result"] = "crash";
				$result["hint"] = "sorry. arg. only arg. no hint at all.";
			}
		}

		print json_encode($result, JSON_PRETTY_PRINT);
	}