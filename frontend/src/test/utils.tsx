import { render, type RenderOptions } from '@testing-library/react'
import { type ReactElement } from 'react'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from '../context/AuthContext'

// Custom render function that wraps components with providers
const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) => render(ui, { 
  wrapper: ({ children }) => (
    <BrowserRouter>
      <AuthProvider>{children}</AuthProvider>
    </BrowserRouter>
  ),
  ...options 
})

export * from '@testing-library/react'
export { customRender as render }
