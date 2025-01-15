"use client";

import { LoginForm } from "../../../components/login-form";

const LoginPage = () => {
	return (
		<div className="flex items-center justify-center h-screen">
			<div className="w-full max-w-sm">
				<LoginForm />
			</div>
		</div>
	);
};

export default LoginPage;
