"use client";

import { useState } from "react";
import axios from "axios";
import { motion } from "motion/react";
import { animate } from "motion";

export default function ShoppingList() {
  const [items, setItems] = useState([""]);
  const [content, setContent] = useState("");
  const [expand, setExpand] = useState(false);

  const handleTextChange = (index, value) => {
    const newItems = [...items];
    newItems[index] = value; // Update the text of the current item
    setItems(newItems);
  };

  // Handle Enter key press
  const handleKeyPress = (e, index) => {
    if (e.key === "Enter") {
      e.preventDefault(); // Prevent new line
      const newItems = [...items];

      if (newItems[index].trim() !== "") {
        newItems.splice(index + 1, 0, "");
        setItems(newItems);
      }
    }

    if (e.key === "Backspace" && items[index] === "" && items.length > 1) {
      const newItems = items.filter((_, i) => i !== index);
      setItems(newItems);
    }
  };

  const handleSubmit = async () => {
    axios.post("http://localhost:8000/items/", { items: items }).then((res) => {
      setContent(res.data.content);
      console.log(content);
      setExpand(true);
    });
  };

  return (
    <>
      <ul
        className={`grid bg-transparent border-2 border-white rounded-xl m-16 p-4 ${expand ? "w-0" : ""}`}
      >
        {items.map((item, i) => (
          <li key={i}>
            <input
              className="bg-transparent text-white text-xl rounded-xl p-2 placeholder-slate-400 outline-none"
              placeholder="I want to buy..."
              value={item}
              autoFocus={i === items.length - 1}
              onChange={(e) => handleTextChange(i, e.target.value)}
              onKeyDown={(e) => handleKeyPress(e, i)}
            />
          </li>
        ))}
        <button onClick={handleSubmit} className="place-self-end">
          <motion.svg
            whileHover={{ scale: 1.1 }}
            xmlns="http://www.w3.org/2000/svg"
            width="32"
            height="32"
            viewBox="0 0 24 24"
          >
            <path
              fill="none"
              stroke="white"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="m19 12l-6-6m6 6l-6 6m6-6H5"
            />
          </motion.svg>
        </button>
      </ul>
    </>
  );
}
