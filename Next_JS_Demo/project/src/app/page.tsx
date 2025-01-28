"use client"
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div>
          <h1 >Hello</h1>
          <User name="Anjali Zala"/>
          <Link href="/login">Login Page</Link>
          <br />
          <Link href="/about">About Page</Link>
          <br />
          <button onClick={()=>router.push("/login")}>Login Button</button>
          <button onClick={()=>router.push("/about")}>About Button</button>
        </div>
        </main>
    </div>
  );
}

const User = (props) => {
  return (
    <div>
      <h2>{props.name}</h2>
    </div>
  )
}
