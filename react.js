import React from "react";
import axios from "axios";
import { useState } from "react";
import Footer from "./Footer";
// import "./Login.css";

function Login() {
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");

  const handleLogin = async (event) => {
    event.preventDefault();
    const data = {
      username: username,
      Password: password,
    };

    try {
      const response = await axios.post("http://localhost:5000/login", {
        username,
        password,
      });
      localStorage.setItem("access_token", response.data.access_token);
      // Redirect to protected route
      alert("Login successful");
    } catch (error) {
      console.error(error);
      // Display error message to user
    }
  };

  const handleUsernameChange = (event) => {
    setUsername(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  return (
    <div >

          <form method="post" >
              <input
                type="text"
                id=""
                placeholder="Username"
                name="username"
                required
                value={username}
                onChange={handleUsernameChange}
              />
              <input
                type="text"
                id=""
                placeholder="Your email"
              />
              <input
                type="password"
                required
                placeholder="Your Password"
                name="password"
                value={password}
                onChange={handlePasswordChange}
              />
          </form>
          <button type="submit" onClick={handleLogin}>
            Log In
          </button>

    </div>
  );

}

export default Login;