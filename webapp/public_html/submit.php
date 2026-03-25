<?php

function write_log($message, $file = "server.log") {
    $date = date("Y-m-d H:i:s");
    file_put_contents(__DIR__ . "/../logs/$file", "[$date] $message\n", FILE_APPEND);
}



header("Content-Type: application/json");
require_once __DIR__ . "/../database.php";


$input = json_decode(file_get_contents("php://input"), true);
$qr_text = $input['qr'] ?? null;
$action = $input['action'] ?? null;

// usage
write_log("QR request received: " . json_encode($input));
write_log("Student {$geo_id} updated for action {$action}");

if (!$qr_text || !$action) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Invalid request"]);
    exit;
}

// Extract attendee ID
if (!preg_match('/gmcid=(\d+)/', $qr_text, $matches)) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Invalid QR code"]);
    exit;
}
$geo_id = $matches[1];

// Check attendee
$stmt = $pdo->prepare("SELECT * FROM attendees WHERE id = ?");
$stmt->execute([$geo_id]);
$attendee = $stmt->fetch();

if (!$attendee) {
    http_response_code(404);
    echo json_encode(["status" => "error", "message" => "attendee not found"]);
    exit;
}

$workshops = ["digital_twins_(nicolas)", "participatory_mapping_(candela)", "disaster_management_(andres)"];
// Handle attendance update
if ($action === "dinner") {
    if (!empty($attendee['dinner'])) {
        http_response_code(409);
        echo json_encode(["status" => "conflict", "message" => "⚠️ attendee {$attendee['name']} already marked for dinner"]);
        exit;
    }
    $update = $pdo->prepare("UPDATE attendees SET dinner = 'done' WHERE id = ?");
    $update->execute([$geo_id]);
} elseif ($action === "welcome") {
    if (!empty($attendee['welcome'])) {
        http_response_code(409);
        echo json_encode(["status" => "conflict", "message" => "⚠️ attendee {$attendee['name']} already marked for welcome"]);
        exit;
    }
    $update = $pdo->prepare("UPDATE attendees SET welcome = 'done' WHERE id = ?");
    $update->execute([$geo_id]);

} elseif (in_array($action, $workshops)) {
    if (!empty($attendee['workshop'])) {
        http_response_code(409);
        echo json_encode(["status" => "conflict", "message" => "⚠️ attendee {$attendee['name']} already marked for a workshop"]);
        exit;
    }
    $update = $pdo->prepare("UPDATE attendees SET workshop = ? WHERE id = ?");
    $update->execute([$action, $geo_id]);
}

http_response_code(200);
echo json_encode(["status" => "ok", "message" => "$action registered for $qr_text"]);