import { describe, it, expect } from 'vitest'
import { screen } from '@testing-library/react'
import { render } from './utils'
import SignUpPage from '../features/SignUp/SignUpPage'

describe("SignUpPage", () => {

    it("renders the SignUpPage with the correct title", () => {
        render(<SignUpPage />)
        expect(screen.getByText("Sign Up")).toBeInTheDocument();
    })

    it("renders the SignUpPage with the correct email input", () => {
        render(<SignUpPage />)
        expect(screen.getByLabelText("Email")).toBeInTheDocument();
    })

    it("renders the SignUpPage with the correct password input", () => {
        render(<SignUpPage />)
        expect(screen.getByLabelText("Password")).toBeInTheDocument();
    })

    it("renders the SignUpPage with the correct first name input", () => {
        render(<SignUpPage />)
        expect(screen.getByLabelText("First Name")).toBeInTheDocument();
    })
    
    it("renders the SignUpPage with the correct last name input", () => {
        render(<SignUpPage />)
        expect(screen.getByLabelText("Last Name")).toBeInTheDocument();
    })

    it("renders the SignUpPage with the correct create account button", () => {
        render(<SignUpPage />)
        expect(screen.getByText("Create Account")).toBeInTheDocument();
    })

    
    
})