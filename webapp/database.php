<?php
// database.php

// Database configuration
$host = "";   // Database host ip
$db   = ""; // Database name
$user = ""; // Database username
$pass = ""; // Database password
$charset = "utf8mb4";

// Data Source Name (DSN)
$dsn = "mysql:host=$host;dbname=$db;charset=$charset";

// PDO options
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION, // Throw exceptions on errors
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,       // Return associative arrays
    PDO::ATTR_EMULATE_PREPARES   => false,                  // Use native prepared statements
];

try {
    // Create a PDO instance (database connection)
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    // Handle connection errors
    write_log($e);
    http_response_code(500); // internal server error
    echo json_encode(["status" => "error", "message" => "Database connection failed"]);
    exit;
}