import React from "react";

const ProductCard = ({ product }) => {
  return (
    <div className="card h-100 shadow-sm">
      <img
        src={product.image}
        className="card-img-top"
        alt={product.name}
        style={{ height: "200px", objectFit: "contain" }}
      />
      <div className="card-body d-flex flex-column text-center">
        <h5 className="card-title">{product.name}</h5>

        <p className="mb-2">
          <strong>Title:</strong> {product.title}
        </p>
        <p className="mb-2">
          <strong>Price:</strong> ${product.price}
        </p>
        <p className="mb-0">
          <strong>Rating:</strong> {product.rating}
        </p>
      </div>
    </div>
  );
};

export default ProductCard;
