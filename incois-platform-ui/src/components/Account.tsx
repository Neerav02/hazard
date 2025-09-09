// src/components/Account.tsx
import { supabase } from '../supabaseClient';
import { useAuth } from '../contexts/AuthContext';

export default function Account() {
  const { user } = useAuth();

  const handleLogout = async () => {
    try {
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
    } catch (error: any) {
      alert(error.error_description || error.message);
    }
  };

  return (
    <div>
      <h2>Account</h2>
      <p>Welcome, {user?.email}!</p>
      <button onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}