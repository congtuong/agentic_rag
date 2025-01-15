import { z } from "zod";

export const LoginFormProps = z.object({
	username: z.string().nonempty(),
	password: z.string().nonempty(),
});
