// 3. Logout function for the navbar
    function logout() {
      localStorage.clear(); // Wipe the saved user data
      window.location.href = "login.html"; // Send back to login
    }
