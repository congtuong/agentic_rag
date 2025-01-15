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
import { fetchLogin } from "@/api/auth";
import { useForm } from "react-hook-form";
import { Form, FormField, FormItem, FormControl } from "./ui/form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { LoginFormProps } from "@/types/form";
import { useToast } from "@/hooks/use-toast";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/use-auth";

export function LoginForm() {
	const form = useForm<z.infer<typeof LoginFormProps>>({
		resolver: zodResolver(LoginFormProps),
		defaultValues: {
			username: "",
			password: "",
		},
	});
	const router = useRouter();
	const { toast } = useToast();
	const { loginProvider } = useAuth();

	const handleLogin = async (values: z.infer<typeof LoginFormProps>) => {
		try {
			console.log(values);
			await loginProvider(values);
			toast({
				title: "Login success~",
			});
			router.push("/");
		} catch (error) {
			toast({
				title: "Login failed~",
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
