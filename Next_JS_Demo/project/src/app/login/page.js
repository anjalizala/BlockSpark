"use client"
import Link from "next/link";
import { useRouter } from "next/navigation"

const Login = () => {
    const router = useRouter();
    return ( <
        div >
        <
        h1 > Login < /h1> <br / > < Link href = "/" > Home Page < /Link> <br / >
        <
        button onClick = {
            () => router.push("/") } > Home Button < /button>{" "}<br / > < br / >
        <
        Link href = "login/studentlogin" > Student Login < /Link>{" "}<br / >
        <
        Link href = "login/teacherlogin" > Teacher Login < /Link>{" "} <
        /div>
    );
};

export default Login;