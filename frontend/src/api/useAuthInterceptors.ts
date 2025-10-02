import { useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { initializeAuthInterceptors } from './interceptors';

// Custom hook to initialize auth interceptors
export const useAuthInterceptors = () => {
  const { accessToken, setAccessToken } = useAuth();

  useEffect(() => {
    // Initialize interceptors with auth functions
    initializeAuthInterceptors(
      () => accessToken, // getAccessToken function
      setAccessToken,    // setAccessToken function
      (path: string) => {
        // Simple navigation function - you can replace this with your router
        window.location.href = path;
      }
    );
  }, [accessToken, setAccessToken]);
};
