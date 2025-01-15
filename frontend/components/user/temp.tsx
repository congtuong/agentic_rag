import { atom, useAtom } from "jotai";

export const mails = [
	{
		id: "6c84fb90-12c4-11e1-840d-7b25c5ee775a",
		name: "William Smith",
		email: "williamsmith@example.com",
		subject: "Meeting Tomorrow",
		text: "Hi, let's have a meeting tomorrow to discuss the project. I've been reviewing the project details and have some ideas I'd like to share. It's crucial that we align on our next steps to ensure the project's success.\n\nPlease come prepared with any questions or insights you may have. Looking forward to our meeting!\n\nBest regards, William",
		date: "2023-10-22T09:00:00",
		read: true,
		labels: ["meeting", "work", "important"],
	},
];

export type Mail = (typeof mails)[number];

export const accounts = [
	{
		label: "Alicia Koch",
		email: "alicia@example.com",
		icon: (
			<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
				<title>Vercel</title>
				<path d="M24 22.525H0l12-21.05 12 21.05z" fill="currentColor" />
			</svg>
		),
	},
	{
		label: "Alicia Koch",
		email: "alicia@gmail.com",
		icon: (
			<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
				<title>Gmail</title>
				<path
					d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z"
					fill="currentColor"
				/>
			</svg>
		),
	},
	{
		label: "Alicia Koch",
		email: "alicia@me.com",
		icon: (
			<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
				<title>iCloud</title>
				<path
					d="M13.762 4.29a6.51 6.51 0 0 0-5.669 3.332 3.571 3.571 0 0 0-1.558-.36 3.571 3.571 0 0 0-3.516 3A4.918 4.918 0 0 0 0 14.796a4.918 4.918 0 0 0 4.92 4.914 4.93 4.93 0 0 0 .617-.045h14.42c2.305-.272 4.041-2.258 4.043-4.589v-.009a4.594 4.594 0 0 0-3.727-4.508 6.51 6.51 0 0 0-6.511-6.27z"
					fill="currentColor"
				/>
			</svg>
		),
	},
];

export type Account = (typeof accounts)[number];

export const contacts = [
	{
		name: "Emma Johnson",
		email: "emma.johnson@example.com",
	},
];

export type Contact = (typeof contacts)[number];

type Config = {
	selected: Mail["id"] | null;
};

const configAtom = atom<Config>({
	selected: mails[0].id,
});

export function useMail() {
	return useAtom(configAtom);
}
