import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
        console.log('Fetching leaderboard from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Leaderboard data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Processed leaderboard data:', leaderboardData);
        
        setLeaderboard(leaderboardData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching leaderboard:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) return (
    <div className="container mt-5">
      <div className="text-center">
        <div className="spinner-border text-danger" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading leaderboard...</p>
      </div>
    </div>
  );
  if (error) return (
    <div className="container mt-5">
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Error!</h4>
        <p>{error}</p>
      </div>
    </div>
  );

  return (
    <div className="container mt-5">
      <div className="mb-4">
        <h2>🏆 Leaderboard</h2>
        <p className="text-muted">Top Performers: <strong>{leaderboard.length}</strong></p>
      </div>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th scope="col">Rank</th>
              <th scope="col">User</th>
              <th scope="col">Team</th>
              <th scope="col">Total Points</th>
              <th scope="col">Activities</th>
              <th scope="col">Total Distance (km)</th>
              <th scope="col">Total Calories</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry, index) => (
              <tr key={entry.user_id || index} className={index < 3 ? 'table-warning' : ''}>
                <td>
                  {index === 0 && <span className="badge bg-warning text-dark fs-6">🥇 1st</span>}
                  {index === 1 && <span className="badge bg-secondary fs-6">🥈 2nd</span>}
                  {index === 2 && <span className="badge bg-danger fs-6">🥉 3rd</span>}
                  {index > 2 && <span className="rank-badge">{index + 1}</span>}
                </td>
                <td><strong>{entry.user_name || entry.username || entry.full_name || 'N/A'}</strong></td>
                <td>
                  {entry.team_id ? (
                    <span className="badge bg-info">{entry.team_id}</span>
                  ) : (
                    <span className="text-muted">No team</span>
                  )}
                </td>
                <td><span className="badge bg-success fs-6">{entry.total_points || 0}</span></td>
                <td>{entry.activity_count || 0}</td>
                <td>{entry.total_distance || 0}</td>
                <td><strong>{entry.total_calories || 0}</strong></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Leaderboard;
