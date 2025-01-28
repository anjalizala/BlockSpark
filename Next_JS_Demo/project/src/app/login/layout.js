"use client"
import Link from "next/link";
import "./login.css";
import { usePathname } from "next/navigation";

export default function Layout({
    children
}) {
    const pathname = usePathname();
    return ( <
        div > {
            pathname !== "/login/teacherlogin" ?
            <
            ul className = "login-menu" >
            <
            li >
            <
            h4 > Login - Navbar < /h4>{" "} < /
            li > { " " } <
            li >
            <
            Link href = "/login" > Login - Main < /Link>{" "} < /
            li > { " " } <
            li >
            <
            Link href = "/login/studentlogin" > Student Login < /Link>{" "} < /
            li > { " " } <
            li >
            <
            Link href = "/login/teacherlogin" > Teacher Login < /Link>{" "} < /
            li > { " " } <
            /ul>:<
            Link href = "/login" > Go to Main Login Page < /Link>
        } { children } { " " } <
        /div>
    );
}