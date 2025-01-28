'use client'
import Link from "next/link";

export default function StudentList() {
    return ( <
        div >
        <
        h1 > Student List < /h1>{" "} <
        ul >
        <
        li >
        <
        Link href = "/studentlist/jay" > Jay < /Link>{" "} <
        /li>{" "} <
        li >
        <
        Link href = "/studentlist/anjali" > Anjali < /Link>{" "} <
        /li>{" "} <
        li >
        <
        Link href = "/studentlist/dhvani" > Dhvani < /Link>{" "} <
        /li>{" "} <
        /ul>{" "} <
        /div>
    );
}