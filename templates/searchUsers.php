<?php
// Connect to MySQL database
$servername = "localhost";
$username = "root";
$password = "thriambak";
$dbname = "users";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get search term from the request
$searchTerm = isset($_GET['searchTerm']) ? $_GET['searchTerm'] : '';
$role = isset($_GET['role']) ? $_GET['role'] : '';
$status = isset($_GET['status']) ? $_GET['status'] : '';

// Construct the SQL query
$sql = "SELECT id, username, name, email, role, phone, created_at FROM users WHERE username LIKE ?";

// Add filters for role and status if provided
if (!empty($role)) {
    $sql .= " AND role = ?";
}

if (!empty($status)) {
    $sql .= " AND status = ?";
}

// Prepare and execute the statement
$stmt = $conn->prepare($sql);
if (!empty($role) && !empty($status)) {
    $stmt->bind_param('sss', $searchTerm, $role, $status);
} else if (!empty($role)) {
    $stmt->bind_param('ss', $searchTerm, $role);
} else if (!empty($status)) {
    $stmt->bind_param('ss', $searchTerm, $status);
} else {
    $stmt->bind_param('s', $searchTerm);
}

$stmt->execute();
$result = $stmt->get_result();

// Fetch all the rows
$users = [];
while ($row = $result->fetch_assoc()) {
    $users[] = $row;
}

// Return the results as JSON
echo json_encode($users);

// Close the connection
$stmt->close();
$conn->close();
?>
