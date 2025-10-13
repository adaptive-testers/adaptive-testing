import { AuthProvider } from './context/AuthContext'
import RoleSelectionPage from './features/SignUp/RoleSelectionPage'
import SignUpPage from './features/SignUp/SignUpPage'

function App() {
  return (
     <AuthProvider>
      <div className="bg-black min-h-screen flex items-center justify-center p-4">
        <RoleSelectionPage />
      </div>
    </AuthProvider>
  )
}

export default App
