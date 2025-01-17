import { useToast } from "@/hooks/use-toast";
import { IAPIResponse, ILoginFormValues, IRegisterFormValues } from "@/types";
import { getCookie } from "cookies-next";

const fetchLogin = async (body: ILoginFormValues) => {
	// Fetch the login endpoint
	const response = await fetch(
		`${process.env.NEXT_PUBLIC_API_URL}/auth/login`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			credentials: "include",
			body: JSON.stringify(body),
		}
	);
	return response;
};

const fetchProfile = async () => {
	const header = new Headers();
	header.append("content-type", "application/json");
	header.append("authorization", `Bearer ${getCookie("access_token")}`);

	const response = await fetch(
		`${process.env.NEXT_PUBLIC_API_URL}/auth/profile`,
		{
			method: "GET",
			headers: header,
		}
	);
	return response;
};

const fetchRegister = async (body: IRegisterFormValues) => {
	const response = await fetch(
		`${process.env.NEXT_PUBLIC_API_URL}/auth/register`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(body),
		}
	);
	return response;
};

const fetchWithToken = async (url: string, method: string, body?: any) => {
	const header = new Headers();
	const token = getCookie("access_token");
	if (!token) {
		throw new Error("No token found");
	}
	header.append("content-type", "application/json");
	header.append("authorization", `Bearer ${token}`);

	const response = await fetch(url, {
		method,
		headers: header,
		body: JSON.stringify(body),
	});
	return response;
};

export { fetchLogin, fetchProfile, fetchRegister, fetchWithToken };
