import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import App from "./App";
import LoginPage from "./pages/LoginPage";

// A custom private route component
const PrivateRoute = ({ children }) => {
  // Check if user is authenticated
  const isAuthenticated = localStorage.getItem("authToken") !== null;
  
  // If authenticated, render the children components
  // If not, redirect to login page
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <Router>
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route 
        path="/*" 
        element={
          <PrivateRoute>
            <App />
          </PrivateRoute>
        } 
      />
    </Routes>
  </Router>
);