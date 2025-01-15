"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { RegisterFormProps } from "@/types/form";
import { useAuth } from "@/hooks/use-auth";
import { useToast } from "@/hooks/use-toast";

type RegisterFormData = z.infer<typeof RegisterFormProps>;

export default function RegisterForm() {
	const [serverError, setServerError] = useState<string | null>(null);
	const { registerProvider } = useAuth();
	const { toast } = useToast();

	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
	} = useForm<RegisterFormData>({
		resolver: zodResolver(RegisterFormProps),
	});

	const onSubmit = async (data: RegisterFormData) => {
		setServerError(null);
		try {
			console.log("Register attempt with:", data);
			await registerProvider(data);

			toast({
				title: "Registration successful!",
			});
		} catch (error) {
			setServerError(
				"An error occurred during registration. Please try again."
			);
		}
	};

	return (
		<Card className="w-full max-w-sm mx-auto">
			<CardHeader className="items-center">
				<CardTitle>Register</CardTitle>
				<CardDescription>Create a new account</CardDescription>
			</CardHeader>
			<CardContent className="space-y-8">
				<form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
					<div className="space-y-2">
						<Label htmlFor="name">Username</Label>
						<Input
							id="username"
							type="username"
							placeholder="Enter your username"
							{...register("username")}
							aria-invalid={errors.username ? "true" : "false"}
						/>
						{errors.username && (
							<p className="text-red-500 text-sm mt-1">
								{errors.username.message}
							</p>
						)}
					</div>
					<div className="space-y-2">
						<Label htmlFor="email">Email</Label>
						<Input
							id="email"
							type="email"
							placeholder="Enter your email"
							{...register("email")}
							aria-invalid={errors.email ? "true" : "false"}
						/>
						{errors.email && (
							<p className="text-red-500 text-sm mt-1">
								{errors.email.message}
							</p>
						)}
					</div>
					<div className="space-y-2">
						<Label htmlFor="password">Password</Label>
						<Input
							id="password"
							type="password"
							placeholder="Enter your password"
							{...register("password")}
							aria-invalid={errors.password ? "true" : "false"}
						/>
						{errors.password && (
							<p className="text-red-500 text-sm mt-1">
								{errors.password.message}
							</p>
						)}
					</div>

					<div className="space-y-2">
						<Label htmlFor="user_fullname">Full Name</Label>
						<Input
							id="user_fullname"
							type="text"
							placeholder="Enter your full name"
							{...register("user_fullname")}
							aria-invalid={errors.user_fullname ? "true" : "false"}
						/>
						{errors.user_fullname && (
							<p className="text-red-500 text-sm mt-1">
								{errors.user_fullname.message}
							</p>
						)}
					</div>

					{serverError && <p className="text-red-500 text-sm">{serverError}</p>}
					<Button
						type="submit"
						className="w-full hover:bg-slate-500 cursor-pointer"
						disabled={isSubmitting}
					>
						{isSubmitting ? "Please wait..." : "Register"}
					</Button>

					<div className="mt-4 text-center text-sm">
						Already have an account?{" "}
						<a
							href="/auth/login"
							className="underline underline-offset-4 hover:text-blue-500"
						>
							Login here
						</a>
					</div>
				</form>
			</CardContent>
		</Card>
	);
}
