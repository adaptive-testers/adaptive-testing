// src/context/AuthContext.tsx

import { createContext, useState, useContext, type ReactNode } from "react";
import { useNavigate } from "react-router-dom";

import { publicApi } from "../api/axios";
// Define the shape of our context state
interface AuthContextType {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Define a custom hook for convenience
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

// Provider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [accessToken, setAccessTokenState] = useState<string | null>(null);
  const navigate = useNavigate();

  const setAccessToken = (token: string | null) => {
    setAccessTokenState(token);
  };

  const logout = async () => {
    try {
      await publicApi.post("/auth/logout", {}, { withCredentials: true });
      // Backend clears the refresh cookie
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      setAccessToken(null);
      navigate("/login");
    }
  };

  return (
    <AuthContext.Provider value={{ accessToken, setAccessToken, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
