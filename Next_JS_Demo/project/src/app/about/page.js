"use client"
import Link from "next/link";
import { useRouter } from "next/navigation";

const About = () => {
    const router = useRouter();
    const navigate = (page) => {
        router.push("/about/" + page);
    };
    return ( <
        div >
        <
        h1 > About Us Page < /h1> <br / >
        <
        Link href = "/" > Home Page < /Link> <br / >
        <
        button onClick = {
            () => router.push("/") } > Home Button < /button> <br / > < br / >
        <
        button onClick = {
            () => navigate("aboutclg") } > About College < /button><br / >
        <
        button onClick = {
            () => navigate("aboutstudent") } > About Student < /button>{" "} <
        /div>
    );
};
export default About;