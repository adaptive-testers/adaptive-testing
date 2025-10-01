import { useState } from 'react'
import './App.css'
import SiteHeader from './components/SiteHeader'
import SignUpContainer from './features/SignUp/SignUpContainer'
import SiteFooter from './components/SiteFooter'

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
