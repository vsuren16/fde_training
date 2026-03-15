function addToCart(productId) {
  const cart = JSON.parse(localStorage.getItem("cart") || "[]");
  cart.push(productId);
  localStorage.setItem("cart", JSON.stringify(cart));
}
