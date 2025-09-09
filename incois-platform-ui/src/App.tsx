// Example router setup in src/App.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './components/Login';
import Dashboard from './components/Account'; // A new page for logged-in users

const router = createBrowserRouter([
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/',
    element: <ProtectedRoute />, // This is the guard
    children: [
      {
        path: '/account', // This route is now protected
        element: <Dashboard />,
      },
      // Add other protected routes here
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;