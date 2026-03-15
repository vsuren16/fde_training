import React, { createContext, useEffect, useState } from "react";

export const UserContext = createContext();

const STORAGE_KEY = "erms_user";

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Load user from localStorage on refresh
  useEffect(() => {
    const savedUser = localStorage.getItem(STORAGE_KEY);

    if (savedUser) {
      const parsedUser = JSON.parse(savedUser);
      setUser(parsedUser);
      setIsLoggedIn(true);
    }
  }, []);

  // Login function
  const login = ({ username, role }) => {
    const userData = {
      name: username,
      role: role,
    };

    setUser(userData);
    setIsLoggedIn(true);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(userData));
  };

  // Logout function
  const logout = () => {
    setUser(null);
    setIsLoggedIn(false);
    localStorage.removeItem(STORAGE_KEY);
  };

  // Update display name (Profile page feature)
  const updateDisplayName = (newName) => {
    setUser((prevUser) => {
      if (!prevUser) return prevUser;

      const updatedUser = {
        ...prevUser,
        name: newName,
      };

      localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedUser));
      return updatedUser;
    });
  };

  return (
    <UserContext.Provider
      value={{
        user,
        role: user?.role || null,
        isLoggedIn,
        login,
        logout,
        updateDisplayName,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};
