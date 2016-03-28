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

	// set the status
	$status_header = 'HTTP/1.1 200 '.$status.' '.$codes[$status];
	header($status_header);

	header("Access-Control-Allow-Origin: *");
	header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");
	header("Access-Control-Allow-Headers: Authorization");
	header('Content-type: ' . $content_type);

	if(!$_POST) {

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
		$result["usingreader"] = substr($output[1], 9, 2) * 1;

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
				if (strlen($output[2]) == 8) {
					$result["result"] = "success";
					$result["value"] = $output[2];
					for ($i = 3; $i <= 20; $i++) {
						if (isset($output[$i]) && (strlen($output[$i]) == 8)) {
							$result["value"] .= $output[$i];
						}
					}
				} else {
					$result["result"] = "error";
					$result["value"] = $output[2];
				}
			} else {
				$result["result"] = "crash";
				$result["hint"] = "sorry. arg. only arg. no hint at all.";
			}
		}

		print json_encode($result, JSON_PRETTY_PRINT);
	} else {
		// Post mode : writing value to NFC chip

		$value = $_POST["value"];

		$vs_writing_line = 8;
		if (isset($_GET["line"]) && $_GET["line"] >= 0 && $_GET["line"] <= 8) {
			$vs_writing_line = $_GET["line"];
		}

		if (isset($_GET["usingreader"]) && $_GET["usingreader"] >= 0) {
			$vs_usingreader = " --usingreader " . $_GET["usingreader"];
		}

		$vs_command = "python NFCReader.py --write ". $vs_writing_line." ".$value. $vs_usingreader . " 2>&1";
		if (PHP_OS == "Darwin") {
			$vs_command = "sudo " . $vs_command;
		}
		$vs_command = "cd " . __DIR__ . " && " . $vs_command;
		exec($vs_command, $output, $return_var);
		$result = array();
		// return reader used
		$result["usingreader"] = substr($output[1], 9, 2) * 1;

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