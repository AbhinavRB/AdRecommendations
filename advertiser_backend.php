<?php

    set_time_limit(300);
    
    if ( 0 < $_FILES['file']['error'] ) {
        echo 'Error: ' . $_FILES['file']['error'] . '<br>';
    }
    else {
        move_uploaded_file($_FILES['file']['tmp_name'], './ImageData/' . 'adImage.jpg');
    }

    $startDate = $_POST['startDate'];
    $endDate = $_POST['endDate'];
    $startDate = str_replace("-", "/", $startDate);
    $endDate = str_replace("-", "/", $endDate);
    $startDate = str_replace("2017", "2016", $startDate);
    $endDate = str_replace("2017", "2016", $endDate);

    $fp = fopen("sampleLabels.txt", "w");
    $labelText = "[";

    $labels = explode(", ", $_POST['labels']);
    foreach ($labels as $l) {
        $labelText = $labelText."'".$l."', ";
    }
    $labelText = substr($labelText, 0, -2)."]";
    fwrite($fp, $labelText);

    fclose($fp);

    $result = shell_exec("python advertiser_updated.py ImageData/adImage.jpg sampleLabels.txt ".$startDate." ".$endDate);
    echo $result;

    // echo "Image got put";
?>