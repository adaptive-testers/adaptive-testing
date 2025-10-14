import { AuthProvider } from './context/AuthContext'
import SignUpPage from './features/SignUp/SignUpPage'

function App() {
  return (
     <AuthProvider>
      <div className="bg-black min-h-screen flex flex-col items-center justify-center gap-10">
        <SignUpPage />
      </div>
    </AuthProvider>
  )
}

export default App
