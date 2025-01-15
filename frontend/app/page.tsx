"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { getCookie } from "cookies-next";
import { useEffect } from "react";

export default function Home() {
	const router = useRouter();
	const accessToken = getCookie("access_token");

	useEffect(() => {
		if (accessToken) {
			router.push("/");
		}
	}, [accessToken]);

	return (
		<div className="flex items-center justify-center h-screen">
			<div className="w-full max-w-sm">
				<Image
					src="/logo.svg"
					alt="Logo"
					width={100}
					height={100}
					className="mx-auto"
				/>
				<h1 className="text-3xl font-semibold text-center">
					Welcome to Next.js
				</h1>
			</div>
		</div>
	);
}
