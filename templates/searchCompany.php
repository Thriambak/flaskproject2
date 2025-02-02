<?php
// searchCompanies.php

// Connect to MySQL database
$servername = "localhost";
$username = "root";
$password = "123";
$dbname = "ADMIN";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get search term and filters from the request
$searchTerm = isset($_GET['searchTerm']) ? $_GET['searchTerm'] : '';
$industry   = isset($_GET['industry']) ? $_GET['industry'] : '';
$location   = isset($_GET['location']) ? $_GET['location'] : '';

// Use wildcard for partial matching
$searchTerm = "%{$searchTerm}%";

$sql = "SELECT id, name, industry, location, website FROM company WHERE name LIKE ?";

// Add filters if provided
if (!empty($industry)) {
    $sql .= " AND industry = ?";
}

if (!empty($location)) {
    $sql .= " AND location = ?";
}

// Prepare and bind parameters
$stmt = $conn->prepare($sql);

if (!empty($industry) && !empty($location)) {
    $stmt->bind_param('sss', $searchTerm, $industry, $location);
} elseif (!empty($industry)) {
    $stmt->bind_param('ss', $searchTerm, $industry);
} elseif (!empty($location)) {
    $stmt->bind_param('ss', $searchTerm, $location);
} else {
    $stmt->bind_param('s', $searchTerm);
}

$stmt->execute();
$result = $stmt->get_result();

// Fetch all matching companies
$companies = [];
while ($row = $result->fetch_assoc()) {
    $companies[] = $row;
}

// Return results as JSON
echo json_encode($companies);

// Close the connection
$stmt->close();
$conn->close();
?>
