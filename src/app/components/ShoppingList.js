"use client";

import { useState } from "react";
import axios from "axios";

export default function ShoppingList() {
  const [items, setItems] = useState([""]);

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
      axios.post(
        "http://localhost:8000/items/",
        {items: items}
      );
    }

    if (e.key === "Backspace" && items[index] === "" && items.length > 1) {
      const newItems = items.filter((_, i) => i !== index);
      setItems(newItems);
    }
  };

  return (
    <>
      <ul className="bg-transparent border-2 border-white rounded-xl m-16 p-4">
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
      </ul>
    </>
  );
}
