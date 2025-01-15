"use client";

import RegisterForm from "@/components/register-form";

const RegisterPage = () => {
	return (
		<div className="flex items-center justify-center h-screen">
			<div className="w-full max-w-sm">
				<RegisterForm />
			</div>
		</div>
	);
};

export default RegisterPage;
