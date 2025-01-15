"use client";

import React from "react";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "./ui/card";
import { Label } from "./ui/label";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { useForm } from "react-hook-form";
import { Form, FormField, FormItem, FormControl } from "./ui/form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { LoginFormProps } from "@/types/form";
import { useToast } from "@/hooks/use-toast";
// import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/use-auth";

export function LoginForm() {
	const form = useForm<z.infer<typeof LoginFormProps>>({
		resolver: zodResolver(LoginFormProps),
		defaultValues: {
			username: "",
			password: "",
		},
	});
	// const router = useRouter();
	const { toast } = useToast();
	const { loginProvider } = useAuth();

	const handleLogin = async (values: z.infer<typeof LoginFormProps>) => {
		try {
			console.log(values);
			await loginProvider(values);
			toast({
				title: "Login success~",
			});
		} catch (error) {
			toast({
				title: "Login failed~",
				description: `${error}`,
			});
		}
	};

	return (
		<div className="flex flex-col gap-6 justify-center items-center">
			<Card>
				<CardHeader className="text-center">
					<CardTitle className="text-2xl font-semibold">Login</CardTitle>
					<CardDescription>
						Welcome back! Login to your account to continue.
					</CardDescription>
				</CardHeader>
				<CardContent>
					<Form {...form}>
						<form onSubmit={form.handleSubmit(handleLogin)}>
							<div className="grid gap-4">
								<div className="grid gap-4">
									<FormField
										control={form.control}
										name="username"
										render={({ field }) => (
											<FormItem>
												<div className="grid gap-2">
													<Label htmlFor="username">Username</Label>
													<FormControl>
														<Input
															id="username"
															placeholder="Username"
															required
															{...field}
														/>
													</FormControl>
												</div>
											</FormItem>
										)}
									/>
									<FormField
										control={form.control}
										name="password"
										render={({ field }) => (
											<div className="grid gap-2">
												<div className="flex">
													<Label htmlFor="password">Password</Label>
													<a
														href="#"
														className="hover:underline ml-auto text-sm inline-block text-xs"
													>
														Forgot password?
													</a>
												</div>
												<FormControl>
													<Input
														id="password"
														type="password"
														placeholder="Password"
														required
														{...field}
													/>
												</FormControl>
											</div>
										)}
									/>
								</div>
								<Button type="submit" className="w-full hover:bg-slate-500">
									Login
								</Button>
								<Button
									type="button"
									className="w-full bg-blue-500 hover:bg-slate-500"
								>
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
										<path
											d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
											fill="currentColor"
										/>
									</svg>
									Login with Google
								</Button>
								<div className="mt-4 text-center text-sm">
									Don&apos;t have an account?{" "}
									<a
										href="/auth/register"
										className="underline underline-offset-4 hover:text-blue-500"
									>
										Sign up
									</a>
								</div>
							</div>
						</form>
					</Form>
				</CardContent>
			</Card>
		</div>
	);
}
