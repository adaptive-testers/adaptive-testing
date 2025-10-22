import { Routes, Route } from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import Dashboard from "./features/Dashboard/DashBoard";
import DashboardLayout from "./features/Dashboard/DashBoardLayout";
import Profile from "./features/Dashboard/Profile";
import Settings from "./features/Dashboard/Settings";
import LogInPage from "./features/LogIn/LogInPage";
import SignUpPage from "./features/SignUp/SignUpPage";

function App() {
  return (
    <AuthProvider>
      <div className="bg-black min-h-screen flex flex-col items-center justify-center gap-10">
        <Routes>
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/login" element={<LogInPage />} />

          <Route element={<DashboardLayout />}>
            <Route path="/" element={<Profile />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Routes>
      </div>
    </AuthProvider>
  );
}

export default App;
