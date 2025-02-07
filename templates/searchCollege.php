<?php
// searchColleges.php

// Connect to MySQL database
$servername = "localhost";
$username = "root";
$password = "thriambak";
$dbname = "college"
;

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get search term and filters from the request
$searchTerm = isset($_GET['searchTerm']) ? $_GET['searchTerm'] : '';
$location   = isset($_GET['location']) ? $_GET['location'] : '';
$status     = isset($_GET['status']) ? $_GET['status'] : '';

// If you wish to use wildcards for partial matches, uncomment the following line:
// $searchTerm = "%{$searchTerm}%";

$sql = "SELECT id, name, location, status, created_at FROM colleges WHERE name LIKE ?";

// Add filters if provided
if (!empty($location)) {
    $sql .= " AND location = ?";
}

if (!empty($status)) {
    $sql .= " AND status = ?";
}

// Prepare and bind parameters
$stmt = $conn->prepare($sql);

if (!empty($location) && !empty($status)) {
    $stmt->bind_param('sss', $searchTerm, $location, $status);
} else if (!empty($location)) {
    $stmt->bind_param('ss', $searchTerm, $location);
} else if (!empty($status)) {
    $stmt->bind_param('ss', $searchTerm, $status);
} else {
    $stmt->bind_param('s', $searchTerm);
}

$stmt->execute();
$result = $stmt->get_result();

// Fetch all matching colleges
$colleges = [];
while ($row = $result->fetch_assoc()) {
    $colleges[] = $row;
}

// Return results as JSON
echo json_encode($colleges);

// Close the connection
$stmt->close();
$conn->close();
?>
