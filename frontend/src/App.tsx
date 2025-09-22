import { useState } from 'react'
import './App.css'
import SiteHeader from './components/SiteHeader'
import SignUpContainer from './features/SignUp/SignUpContainer'

function App() {


  return (
      <div className="bg-black min-h-screen flex flex-col items-center gap-15">
        <SiteHeader />
        <SignUpContainer />
      </div>
  )
}

export default App
