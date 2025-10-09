import { BrowserRouter, Routes, Route } from "react-router-dom";

import { AuthProvider } from "./context/AuthContext";
import LogInContainer from "./features/LogIn/LogInContainer";
import SignUpPage from "./features/SignUp/SignUpPage";

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <div className="bg-black min-h-screen flex flex-col items-center justify-center gap-10">
          <Routes>
            <Route path="/" element={<LogInContainer />} />
            <Route path="/signup" element={<SignUpPage />} />
            <Route path="/login" element={<LogInContainer />} />
          </Routes>
        </div>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
