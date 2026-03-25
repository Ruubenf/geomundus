<?php
$action = $_GET['action'] ?? 'unknown';

// Load scan.html and replace {{ action }}
$template = file_get_contents(__DIR__ . '/../templates/scan.html');
$template = str_replace('{{ action }}', htmlspecialchars($action), $template);

echo $template;