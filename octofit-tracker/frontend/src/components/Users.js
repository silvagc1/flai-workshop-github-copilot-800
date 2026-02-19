import React, { useState, useEffect } from 'react';

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    full_name: '',
    email: '',
    team_id: ''
  });
  const [saving, setSaving] = useState(false);

  const fetchUsers = async () => {
    try {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
      console.log('Fetching users from:', apiUrl);
      
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Users data received:', data);
      
      // Handle both paginated (.results) and plain array responses
      const usersData = data.results || data;
      console.log('Processed users data:', usersData);
      
      setUsers(usersData);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching users:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  const fetchTeams = async () => {
    try {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
      const response = await fetch(apiUrl);
      if (response.ok) {
        const data = await response.json();
        const teamsData = data.results || data;
        setTeams(teamsData);
      }
    } catch (err) {
      console.error('Error fetching teams:', err);
    }
  };

  useEffect(() => {
    fetchUsers();
    fetchTeams();
  }, []);

  const handleEdit = (user) => {
    setEditingUser(user);
    setFormData({
      username: user.username || '',
      full_name: user.full_name || '',
      email: user.email || '',
      team_id: user.team_id || ''
    });
  };

  const handleClose = () => {
    setEditingUser(null);
    setFormData({
      username: '',
      full_name: '',
      email: '',
      team_id: ''
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/${editingUser.id}/`;
      console.log('Updating user at:', apiUrl, formData);

      const response = await fetch(apiUrl, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const updatedUser = await response.json();
      console.log('User updated:', updatedUser);

      // Refresh users list
      await fetchUsers();
      
      // Close modal
      handleClose();
      
      // Show success message (optional)
      alert('User updated successfully!');
    } catch (err) {
      console.error('Error updating user:', err);
      alert('Failed to update user: ' + err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return (
    <div className="container mt-5">
      <div className="text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading users...</p>
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
        <h2>👥 Users</h2>
        <p className="text-muted">Total Users: <strong>{users.length}</strong></p>
      </div>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Username</th>
              <th scope="col">Full Name</th>
              <th scope="col">Email</th>
              <th scope="col">Team</th>
              <th scope="col">Joined</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user, index) => (
              <tr key={user.id}>
                <td><strong>{index + 1}</strong></td>
                <td><span className="badge bg-primary">{user.username || 'N/A'}</span></td>
                <td><strong>{user.full_name || 'N/A'}</strong></td>
                <td>{user.email || 'N/A'}</td>
                <td>{user.team_id ? <span className="badge bg-info">{user.team_id}</span> : 'No team'}</td>
                <td>{user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</td>
                <td>
                  <button 
                    className="btn btn-sm btn-warning"
                    onClick={() => handleEdit(user)}
                  >
                    ✏️ Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Edit Modal */}
      {editingUser && (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit User: {editingUser.username}</h5>
                <button type="button" className="btn-close" onClick={handleClose}></button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                      type="text"
                      className="form-control"
                      id="username"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="full_name" className="form-label">Full Name</label>
                    <input
                      type="text"
                      className="form-control"
                      id="full_name"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="team_id" className="form-label">Team</label>
                    <select
                      className="form-select"
                      id="team_id"
                      name="team_id"
                      value={formData.team_id}
                      onChange={handleChange}
                    >
                      <option value="">No Team</option>
                      {teams.map((team) => (
                        <option key={team.id} value={team.id}>
                          {team.name}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="modal-footer">
                  <button 
                    type="button" 
                    className="btn btn-secondary" 
                    onClick={handleClose}
                    disabled={saving}
                  >
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    className="btn btn-primary"
                    disabled={saving}
                  >
                    {saving ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
