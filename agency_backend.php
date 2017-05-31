<?php
    $pageno = $_POST['pageno'];
    $maxpages = $_POST['maxpages'];
    $addate = $_POST['addate'];
    $addate = str_replace("-", "/", $addate);

    $result = shell_exec("python agency_algo.py  ".$pageno." ".$maxpages." ".$addate);
    $result = str_replace("'", "", $result);
    $result = str_replace("[", "", $result);
    $result = str_replace("]", "", $result);
    echo $result;

    // echo "Image got put";
?>