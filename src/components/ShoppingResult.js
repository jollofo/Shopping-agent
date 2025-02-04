import axios from "axios";
import { useState } from "react";

export default function ShoppingResult({ items }) {
  const [cont, setCont] = useState("");
  const content = () => {
    axios
      .post("http://localhost:8000/shop_items/", { shopping_results: items })
      .then((res) => {
        console.log(res.data);
        setCont(res.data.content)
      }
    );
  };

  return (
    <>
    <button onClick={content}>Click me</button>
      <ul className="grid bg-transparent border-2 border-white rounded-xl m-16 p-4">
        <li>{cont}</li>
      </ul>
    </>
  );
}