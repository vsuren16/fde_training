import axios from "axios";

const API_URL = "https://dummyjson.com/products";

export const getProducts = async () => {
  const res = await axios.get(API_URL);

  return res.data.products.map((u) => ({
    id: u.id,
    name: u.title,
    title: u.title,
    price: u.price,
    rating: u.rating,
    image: u.thumbnail
  }));
};
