import { Bot, FileText, Layers, MessageSquare } from "lucide-react";

export const NavElements = [
	{
		title: "Conversations",
		// label: "128",
		icon: MessageSquare,
		variant: "default" as "default",
		href: "/user/chat",
	},
	{
		title: "Chatbot",
		// label: "9",
		icon: Bot,
		variant: "ghost" as "ghost",
		href: "/user/chatbots",
	},
	{
		title: "Knowledge",
		// label: "",
		icon: Layers,
		variant: "ghost" as "ghost",
		href: "/user/knowledge",
	},
	{
		title: "Documents",
		// label: "23",
		icon: FileText,
		variant: "ghost" as "ghost",
		href: "/user/documents",
	},
];
