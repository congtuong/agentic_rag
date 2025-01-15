"use client";
import { fetchLogin, fetchProfile, fetchRegister } from "@/api/auth";
import {
	IUser,
	ILoginFormValues,
	IAPIResponse,
	IProfileResponse,
	IRegisterFormValues,
	IRegisterResponse,
} from "@/types";
import { getCookie, setCookie } from "cookies-next";
import { usePathname, useRouter } from "next/navigation";
import {
	useState,
	useEffect,
	useContext,
	createContext,
	ReactNode,
} from "react";

interface AuthContextType {
	user: IUser | null;
	accessToken: string;
	login: (body: ILoginFormValues) => Promise<IAPIResponse<IProfileResponse>>;
	logout: () => void;
	register: (body: IRegisterFormValues) => Promise<IRegisterResponse>;
	loading: boolean;
	isAuthenticated: boolean;
}

export const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
	children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
	const [user, setUser] = useState<IUser | null>(null);
	const [loading, setLoading] = useState(true);
	const [accessToken, setAccessToken] = useState("");
	const [isAuthenticated, setIsAuthenticated] = useState(false);
	const [isLoggedOut, setIsLoggedOut] = useState(false);
	const router = useRouter();
	const pathname = usePathname();
	const redirectURL = encodeURIComponent(pathname);

	useEffect(() => {
		const verifyToken = async () => {
			try {
				const user_access_token = getCookie("access_token") as string;
				if (!user_access_token) {
					throw new Error("Token not found");
				}

				// Optionally, call an endpoint to verify the token's validity
				const response = await fetchProfile();
				if (!response.ok) {
					throw new Error("Invalid token");
				}

				const userData: IAPIResponse<IProfileResponse> = await response.json();

				setUser(userData.data);
				setAccessToken(user_access_token);
				setIsAuthenticated(true);
			} catch (error) {
				console.error("Token verification failed:", error);
				setUser(null);
				setAccessToken("");
				setIsAuthenticated(false);
				setIsLoggedOut(true);
			} finally {
				setLoading(false);
			}
		};

		const intervalId = setInterval(() => {
			verifyToken();
		}, 30000);

		return () => {
			clearInterval(intervalId);
		};
	}, [router, pathname]);

	useEffect(() => {
		if (isLoggedOut && pathname !== "/auth/login") {
			router.push(`/auth/login?redirect=${redirectURL}`);
			setIsLoggedOut(false);
		}
	}, [isLoggedOut, pathname, router, redirectURL]);

	useEffect(() => {
		async function loadUserFromToken() {
			try {
				const user_access_token = getCookie("access_token") as string;
				if (!user_access_token) {
					throw new Error("Token not found");
				}
				const response = await fetchProfile();
				if (!response.ok) {
					throw new Error("Invalid token");
				}
				const userData: IAPIResponse<IProfileResponse> = await response.json();
				setAccessToken(user_access_token);
				setUser(userData.data);
				setIsAuthenticated(true);
			} catch (error) {
				console.error("Failed to verify token:", error);
				setIsAuthenticated(false);
			} finally {
				setLoading(false);
			}
		}
		loadUserFromToken();
	}, []);

	const login = async (body: ILoginFormValues) => {
		try {
			setLoading(true);
			const response = await fetchLogin(body);
			if (!response.ok) {
				throw new Error("Invalid credentials");
			}

			const path = localStorage.getItem("redirectPath") || "/";

			const profile = await fetchProfile();
			if (!profile.ok) {
				throw new Error("Failed to fetch profile");
			}

			const userData: IAPIResponse<IProfileResponse> = await profile.json();

			setUser(userData.data);
			setAccessToken(getCookie("access_token") as string);
			setIsAuthenticated(true);

			if (path === "/") {
				if (userData.data.user_role === "admin") {
					router.push("/admin");
				} else {
					router.push("/user");
				}
			} else {
				router.push(path);
			}

			return userData;
		} catch (err) {
			console.error("Error in login: ", err);
			throw new Error("Something wrong happened");
		} finally {
			setLoading(false);
		}
	};

	const logout = () => {
		setUser(null);
		setAccessToken("");
		setLoading(false);
		setIsAuthenticated(false);
		setIsLoggedOut(true);
		setCookie("access_token", "", { maxAge: -1, path: "/" });
		setCookie("refresh_token", "", { maxAge: -1, path: "/" });
	};

	const register = async (body: IRegisterFormValues) => {
		try {
			const result = await fetchRegister(body);
			if (!result.ok) {
				throw new Error("Registration failed");
			}
			const data: IAPIResponse<IRegisterResponse> = await result.json();

			return data.data;
		} catch (err) {
			console.error("Register failed: ", err || "Something wrong happened !!!");
			throw new Error("Something wrong happened");
		}
	};

	return (
		<AuthContext.Provider
			value={{
				user,
				accessToken,
				login,
				logout,
				register,
				loading,
				isAuthenticated,
			}}
		>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = (): AuthContextType => {
	const context = useContext(AuthContext);
	if (!context) {
		throw new Error("useAuth must be used within an AuthProvider");
	}
	return context;
};
