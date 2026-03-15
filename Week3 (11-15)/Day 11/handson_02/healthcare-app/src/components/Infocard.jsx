import React from "react";

const InfoCard = ({ title, value, subtitle }) => {
  return (
    <div className="col-md-4 mb-3">
      <div className="card shadow-sm h-100">
        <div className="card-body">
          <h6 className="text-muted mb-2">{title}</h6>
          <h2 className="fw-bold mb-1">{value}</h2>
          {subtitle ? <p className="mb-0 text-secondary">{subtitle}</p> : null}
        </div>
      </div>
    </div>
  );
};

export default InfoCard;
