import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

const UserProfile = () => {
  const { user } = useContext(AuthContext);

  if (!user) {
    return (
      <div className="alert alert-warning mt-4">
        No user information available.
      </div>
    );
  }

  return (
    <div>
      <h3 className="mb-4">User Profile</h3>

      <div className="card shadow-sm" style={{ maxWidth: "500px" }}>
        <div className="card-body">
          <div className="mb-3">
            <label className="form-label text-muted">Username</label>
            <div className="fw-semibold">{user.name}</div>
          </div>

          <div className="mb-3">
            <label className="form-label text-muted">Role</label>
            <div>
              <span className="badge bg-primary">
                {user.role}
              </span>
            </div>
          </div>

          <div className="mt-3 text-muted">
            <small>
              Access permissions are controlled based on your role.
            </small>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
