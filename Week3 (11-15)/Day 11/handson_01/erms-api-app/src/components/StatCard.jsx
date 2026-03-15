import React from "react";

const StatCard = ({ title, value, subtitle }) => {
  return (
    <div className="card shadow-sm h-100">
      <div className="card-body">
        <h6 className="text-muted mb-2">{title}</h6>
        <h2 className="fw-bold mb-1">{value}</h2>
        {subtitle ? <div className="text-muted">{subtitle}</div> : null}
      </div>
    </div>
  );
};

export default StatCard;
