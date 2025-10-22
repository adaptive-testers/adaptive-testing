import { screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useNavigate } from 'react-router-dom'

import RoleSelectionPage from '../features/SignUp/RoleSelectionPage'
import { render } from './utils'

// Mock the router hook
vi.mock('react-router-dom', async (importOriginal) => {
    const actual = await importOriginal() as Record<string, unknown>
    return {
        ...actual,
        useNavigate: vi.fn()
    }
})

describe("RoleSelectionPage", () => {
    const mockNavigate = vi.fn()

    beforeEach(() => {
        vi.clearAllMocks()
        vi.mocked(useNavigate).mockReturnValue(mockNavigate)
    })

    // Basic rendering tests
    describe("Rendering", () => {
        it("renders the page with correct title", () => {
            render(<RoleSelectionPage />)
            expect(screen.getByText("Select Your Role")).toBeInTheDocument()
        })

        it("renders both role options", () => {
            render(<RoleSelectionPage />)
            expect(screen.getByText("Student")).toBeInTheDocument()
            expect(screen.getByText("Instructor")).toBeInTheDocument()
        })

        it("renders continue button in disabled state initially", () => {
            render(<RoleSelectionPage />)
            const continueButton = screen.getByText("Continue")
            expect(continueButton).toBeInTheDocument()
            expect(continueButton).toBeDisabled()
        })
    })

    // User interaction tests
    describe("User Interactions", () => {
        it("enables continue button when a role is selected", async () => {
            const user = userEvent.setup()
            render(<RoleSelectionPage />)
            
            const studentOption = screen.getByText("Student").closest('div[role="button"]')
            expect(studentOption).toBeInTheDocument()
            
            await user.click(studentOption!)
            
            const continueButton = screen.getByRole('button', { name: /continue/i })
            expect(continueButton).not.toHaveAttribute('disabled')
        })

        it("applies correct styles when student role is selected", async () => {
            const user = userEvent.setup()
            render(<RoleSelectionPage />)
            
            const studentOption = screen.getByText("Student").closest('div[role="button"]')
            await user.click(studentOption!)
            
            expect(studentOption).toHaveClass('border-[rgba(174,58,58,0.8)]')
            expect(screen.getByText("Student")).toHaveClass('text-[var(--color-primary-text)]')
        })

        it("applies correct styles when instructor role is selected", async () => {
            const user = userEvent.setup()
            render(<RoleSelectionPage />)
            
            const instructorOption = screen.getByText("Instructor").closest('div[role="button"]')
            await user.click(instructorOption!)
            
            expect(instructorOption).toHaveClass('border-[rgba(174,58,58,0.8)]')
            expect(screen.getByText("Instructor")).toHaveClass('text-[var(--color-primary-text)]')
        })

        it("navigates to signup page with correct role when continue is clicked", async () => {
            const user = userEvent.setup()
            render(<RoleSelectionPage />)
            
            const studentOption = screen.getByText("Student").parentElement?.parentElement
            await user.click(studentOption!)
            
            const continueButton = screen.getByText("Continue")
            await user.click(continueButton)
            
            expect(mockNavigate).toHaveBeenCalledWith('/signup', {
                state: { role: 'student' }
            })
        })

        it("allows switching between roles", async () => {
            const user = userEvent.setup()
            render(<RoleSelectionPage />)
            
            const studentOption = screen.getByText("Student").closest('div[role="button"]')
            const instructorOption = screen.getByText("Instructor").closest('div[role="button"]')
            
            await user.click(studentOption!)
            expect(studentOption).toHaveClass('border-[rgba(174,58,58,0.8)]')
            expect(instructorOption).not.toHaveClass('border-[rgba(174,58,58,0.8)]')
            
            await user.click(instructorOption!)
            expect(instructorOption).toHaveClass('border-[rgba(174,58,58,0.8)]')
            expect(studentOption).not.toHaveClass('border-[rgba(174,58,58,0.8)]')
        })
    })

    // Accessibility tests
    describe("Accessibility", () => {
        it("supports keyboard navigation", async () => {
            const user = userEvent.setup()
            render(<RoleSelectionPage />)
            
            // Get elements
            const studentOption = screen.getByText("Student").closest('div[role="button"]') as HTMLElement
            const instructorOption = screen.getByText("Instructor").closest('div[role="button"]') as HTMLElement
            const continueButton = screen.getByRole('button', { name: /continue/i })
            
            // Initial tab should focus student option
            await user.tab()
            expect(studentOption).toHaveFocus()
            
            // Tab to instructor
            await user.tab()
            expect(instructorOption).toHaveFocus()
            
            // Tab to continue button
            await user.tab()
            expect(continueButton).toHaveFocus()
            
            // Tab back to student (full circle)
            await user.tab()
            expect(studentOption).toHaveFocus()
        })

        it("allows role selection with keyboard", async () => {
            const user = userEvent.setup()
            render(<RoleSelectionPage />)
            
            const studentOption = screen.getByText("Student").closest('div[role="button"]')
            
            await user.tab()
            expect(studentOption).toHaveFocus()
            
            await user.keyboard('{Enter}')
            expect(studentOption).toHaveClass('border-[rgba(174,58,58,0.8)]')
            expect(screen.getByRole('button', { name: /continue/i })).not.toHaveAttribute('disabled')
        })
    })
})
