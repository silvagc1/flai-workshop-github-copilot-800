import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Users from './components/Users';
import Activities from './components/Activities';
import Teams from './components/Teams';
import Leaderboard from './components/Leaderboard';
import Workouts from './components/Workouts';

function Home() {
  return (
    <div className="container mt-5">
      <div className="jumbotron text-center">
        <h1 className="display-3 mb-4">🏋️ Welcome to OctoFit Tracker!</h1>
        <p className="lead fs-4 mb-4">Track your fitness activities, compete with teams, and achieve your goals.</p>
        <hr className="my-4" />
        <p className="fs-5">Use the navigation menu above to explore activities, teams, leaderboard, and workout suggestions.</p>
        <div className="mt-5">
          <Link to="/activities" className="btn btn-light btn-lg me-3">View Activities</Link>
          <Link to="/leaderboard" className="btn btn-outline-light btn-lg">See Leaderboard</Link>
        </div>
      </div>

      <div className="row mt-5">
        <div className="col-md-4 mb-4">
          <Link to="/users" className="text-decoration-none">
            <div className="card h-100 text-center home-card">
              <div className="card-body d-flex flex-column justify-content-center">
                <div className="display-1 mb-3">👥</div>
                <h3 className="card-title">Users</h3>
                <p className="card-text">View all registered users and their profiles</p>
              </div>
            </div>
          </Link>
        </div>
        
        <div className="col-md-4 mb-4">
          <Link to="/activities" className="text-decoration-none">
            <div className="card h-100 text-center home-card">
              <div className="card-body d-flex flex-column justify-content-center">
                <div className="display-1 mb-3">🏃</div>
                <h3 className="card-title">Activities</h3>
                <p className="card-text">Track and view all fitness activities</p>
              </div>
            </div>
          </Link>
        </div>
        
        <div className="col-md-4 mb-4">
          <Link to="/leaderboard" className="text-decoration-none">
            <div className="card h-100 text-center home-card">
              <div className="card-body d-flex flex-column justify-content-center">
                <div className="display-1 mb-3">🏆</div>
                <h3 className="card-title">Leaderboard</h3>
                <p className="card-text">See top performers and rankings</p>
              </div>
            </div>
          </Link>
        </div>
      </div>

      <div className="row">
        <div className="col-md-6 mb-4">
          <Link to="/teams" className="text-decoration-none">
            <div className="card h-100 text-center home-card">
              <div className="card-body d-flex flex-column justify-content-center">
                <div className="display-1 mb-3">👥</div>
                <h3 className="card-title">Teams</h3>
                <p className="card-text">Explore teams and join competitions</p>
              </div>
            </div>
          </Link>
        </div>
        
        <div className="col-md-6 mb-4">
          <Link to="/workouts" className="text-decoration-none">
            <div className="card h-100 text-center home-card">
              <div className="card-body d-flex flex-column justify-content-center">
                <div className="display-1 mb-3">💪</div>
                <h3 className="card-title">Workouts</h3>
                <p className="card-text">Get personalized workout recommendations</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            <img src="/octofit-logo.png" alt="OctoFit Logo" className="navbar-logo" />
            OctoFit Tracker
          </Link>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link className="nav-link" to="/">Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/users">Users</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/activities">Activities</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/teams">Teams</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/workouts">Workouts</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/users" element={<Users />} />
        <Route path="/activities" element={<Activities />} />
        <Route path="/teams" element={<Teams />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/workouts" element={<Workouts />} />
      </Routes>
    </div>
  );
}

export default App;
