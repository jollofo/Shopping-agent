import axios from "axios";
import { useState } from "react";

export default function ShoppingResult({ results }) {
  const [c, setC] = useState([]);

  const content = () => {
    axios
      .post("http://localhost:8000/shop_items/", { shopping_results: results })
      .then((res) => console.log(res.data));
  };

  setC(content);

  return (
    <>
      <ul className="bg-transparent text-white text-xl rounded-xl p-2 outline-none">
        {c.map((c, i) => {
          <li key={i}>{r}</li>;
        })}
      </ul>
    </>
  );
}
