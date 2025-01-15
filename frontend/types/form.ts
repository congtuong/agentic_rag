import { z } from "zod";

export const LoginFormProps = z.object({
	username: z.string().nonempty(),
	password: z.string().nonempty(),
});

export const RegisterFormProps = z.object({
	username: z
		.string()
		.min(6, "Username must be at least 6 characters long")
		.max(20, "Username must be at most 20 characters long"),
	email: z.string().email("Invalid email address"),
	password: z
		.string()
		.min(6, "Password must be at least 8 characters long")
		.max(32, "Password must be at most 32 characters long"),
	user_fullname: z.string().nonempty(),
});

export const ChatFormProps = z.object({
	query: z.string().nonempty(),
});
