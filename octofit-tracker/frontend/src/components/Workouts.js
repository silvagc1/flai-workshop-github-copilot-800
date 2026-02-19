import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
        console.log('Fetching workouts from:', apiUrl);
        
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Workouts data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Processed workouts data:', workoutsData);
        
        setWorkouts(workoutsData);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching workouts:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) return (
    <div className="container mt-5">
      <div className="text-center">
        <div className="spinner-border text-info" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading workouts...</p>
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
        <h2>💪 Recommended Workouts</h2>
        <p className="text-muted">Total Workouts: <strong>{workouts.length}</strong></p>
      </div>
      <div className="row">
        {workouts.map((workout) => (
          <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
            <div className="card h-100">
              <div className="card-header bg-info text-white">
                <h5 className="card-title mb-0">{workout.name}</h5>
              </div>
              <div className="card-body">
                <p className="card-text">{workout.description}</p>
                <div className="mt-3 d-flex flex-wrap gap-2">
                  <span className="badge bg-primary">Category: {workout.category || 'General'}</span>
                  <span className="badge bg-secondary">Duration: {workout.duration} min</span>
                  <span className="badge bg-warning text-dark">Difficulty: {workout.difficulty}</span>
                </div>
                {Array.isArray(workout.exercises) && workout.exercises.length > 0 && (
                  <div className="mt-3">
                    <strong>Exercises:</strong>
                    <ul className="small mt-2 mb-0">
                      {workout.exercises.map((exercise, idx) => (
                        <li key={idx}>{exercise}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {Array.isArray(workout.recommended_for) && workout.recommended_for.length > 0 && (
                  <div className="mt-3">
                    <strong>Recommended for:</strong>
                    <div className="mt-2">
                      {workout.recommended_for.map((rec, idx) => (
                        <span key={idx} className="badge bg-success me-1 mb-1">{rec}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              <div className="card-footer bg-transparent">
                <button className="btn btn-sm btn-outline-info w-100">Start Workout</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Workouts;
