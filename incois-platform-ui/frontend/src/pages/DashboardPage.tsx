import { useAuth } from '../contexts/AuthContext';
import { supabase } from '../supabaseClient';
import ObservationsMap from '../components/ObservationsMap';

const DashboardPage = () => {
  const { user } = useAuth();
  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Welcome, {user?.email}!</p>
      <button onClick={handleLogout}>Logout</button>
      <hr />
      <h3>Observations Map</h3>
      <ObservationsMap />
    </div>
  );
};

export default DashboardPage;
