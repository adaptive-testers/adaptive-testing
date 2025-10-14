import SiteHeader from './components/SiteHeader'
import SiteFooter from './components/SiteFooter'
import SignUpContainer from './features/SignUp/SignUpPage'

function App() {
  return (
      <div className="bg-black min-h-screen flex flex-col items-center gap-10">
        <SiteHeader />
        <SignUpContainer />
        <SiteFooter />
      </div>
  )
}

export default App
