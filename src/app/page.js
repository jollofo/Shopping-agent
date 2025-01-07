import Image from "next/image";
import Container from "./components/Container";
import ShoppingList from "./components/ShoppingList";

export default function Home() {
  return (
    <>
      <Container>
        <h1 className="text-5xl">Shopping Agent</h1>
        <ShoppingList />
      </Container>
    </>
  );
}
