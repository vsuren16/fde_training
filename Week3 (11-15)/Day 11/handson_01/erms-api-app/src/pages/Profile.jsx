import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../context/UserContext";

const Profile = () => {
  const { user, updateDisplayName } = useContext(UserContext);

  const [displayName, setDisplayName] = useState("");
  const [message, setMessage] = useState("");

  // Initialize local state from context
  useEffect(() => {
    if (user?.name) setDisplayName(user.name);
  }, [user]);

  const handleSave = (e) => {
    e.preventDefault();
    setMessage("");

    if (!displayName.trim()) {
      setMessage("Display name cannot be empty.");
      return;
    }

    updateDisplayName(displayName.trim());
    setMessage("Profile updated successfully.");
  };

  if (!user) {
    return <div className="alert alert-warning">No user logged in.</div>;
  }

  return (
    <div>
      <h2 className="mb-4">User Profile</h2>

      {message && <div className="alert alert-info py-2">{message}</div>}

      <div className="card shadow-sm">
        <div className="card-body">
          <p className="mb-2">
            <strong>Role:</strong> {user.role}
          </p>

          <form onSubmit={handleSave} className="mt-3">
            <div className="mb-3">
              <label className="form-label">Display Name</label>
              <input
                className="form-control"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Enter display name"
              />
            </div>

            <button type="submit" className="btn btn-primary">
              Save Changes
            </button>
          </form>

          <p className="text-muted mt-3 mb-0" style={{ fontSize: 12 }}>
            * Display name updates locally (mock).
          </p>
        </div>
      </div>
    </div>
  );
};

export default Profile;
