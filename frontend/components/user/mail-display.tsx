import { addDays } from "date-fns/addDays";
import { addHours } from "date-fns/addHours";
import { format } from "date-fns/format";
import { nextSaturday } from "date-fns/nextSaturday";
import {
	Archive,
	ArchiveX,
	Clock,
	Copy,
	CornerDownLeft,
	Forward,
	Mic,
	MoreVertical,
	Paperclip,
	RefreshCcwIcon,
	Reply,
	ReplyAll,
	Trash2,
} from "lucide-react";

import {
	DropdownMenuContent,
	DropdownMenuItem,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
	DropdownMenu,
	DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Label } from "@/components/ui/label";
import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from "@/components/ui/popover";
import { Separator } from "@/components/ui/separator";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import {
	Tooltip,
	TooltipContent,
	TooltipTrigger,
} from "@/components/ui/tooltip";
import {
	ChatBubble,
	ChatBubbleAvatar,
	ChatBubbleMessage,
	ChatBubbleAction,
	ChatBubbleActionWrapper,
} from "@/components/ui/chat/chat-bubble";
import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { ChatInput } from "@/components/ui/chat/chat-input";
import { Mail } from "./temp";
import { IMessageResponse } from "@/types";
import React from "react";

interface Message {
	id: string;
	message: string;
	sender: string;
	isLoading?: boolean;
}

export function ChatDisplay({ items }: { items: IMessageResponse[] }) {
	const [messages, setMessages] = React.useState<Message[]>([]);

	React.useEffect(() => {
		setMessages(
			items.map((item) => ({
				id: item.id,
				message: item.content,
				sender: item.type === "user" ? "user" : "bot",
			}))
		);
	}, [items]);

	console.log(messages);

	const actionIcons = [
		{ icon: Copy, type: "Copy" },
		{ icon: RefreshCcwIcon, type: "Regenerate" },
	];

	return (
		<div className="flex h-full flex-col">
			{/* <div className="flex items-center p-2">
				<div className="flex items-center gap-2">
					<Tooltip>
						<TooltipTrigger asChild>
							<Button variant="ghost" size="icon" disabled={!mail}>
								<Archive className="h-4 w-4" />
								<span className="sr-only">Archive</span>
							</Button>
						</TooltipTrigger>
						<TooltipContent>Archive</TooltipContent>
					</Tooltip>
					<Tooltip>
						<TooltipTrigger asChild>
							<Button variant="ghost" size="icon" disabled={!mail}>
								<ArchiveX className="h-4 w-4" />
								<span className="sr-only">Move to junk</span>
							</Button>
						</TooltipTrigger>
						<TooltipContent>Move to junk</TooltipContent>
					</Tooltip>
					<Tooltip>
						<TooltipTrigger asChild>
							<Button variant="ghost" size="icon" disabled={!mail}>
								<Trash2 className="h-4 w-4" />
								<span className="sr-only">Move to trash</span>
							</Button>
						</TooltipTrigger>
						<TooltipContent>Move to trash</TooltipContent>
					</Tooltip>
					<Separator orientation="vertical" className="mx-1 h-6" />
					<Tooltip>
						<Popover>
							<PopoverTrigger asChild>
								<TooltipTrigger asChild>
									<Button variant="ghost" size="icon" disabled={!mail}>
										<Clock className="h-4 w-4" />
										<span className="sr-only">Snooze</span>
									</Button>
								</TooltipTrigger>
							</PopoverTrigger>
							<PopoverContent className="flex w-[535px] p-0">
								<div className="flex flex-col gap-2 border-r px-2 py-4">
									<div className="px-4 text-sm font-medium">Snooze until</div>
									<div className="grid min-w-[250px] gap-1">
										<Button
											variant="ghost"
											className="justify-start font-normal"
										>
											Later today{" "}
											<span className="ml-auto text-muted-foreground">
												{format(addHours(today, 4), "E, h:m b")}
											</span>
										</Button>
										<Button
											variant="ghost"
											className="justify-start font-normal"
										>
											Tomorrow
											<span className="ml-auto text-muted-foreground">
												{format(addDays(today, 1), "E, h:m b")}
											</span>
										</Button>
										<Button
											variant="ghost"
											className="justify-start font-normal"
										>
											This weekend
											<span className="ml-auto text-muted-foreground">
												{format(nextSaturday(today), "E, h:m b")}
											</span>
										</Button>
										<Button
											variant="ghost"
											className="justify-start font-normal"
										>
											Next week
											<span className="ml-auto text-muted-foreground">
												{format(addDays(today, 7), "E, h:m b")}
											</span>
										</Button>
									</div>
								</div>
								<div className="p-2">
									<Calendar />
								</div>
							</PopoverContent>
						</Popover>
						<TooltipContent>Snooze</TooltipContent>
					</Tooltip>
				</div>
				<div className="ml-auto flex items-center gap-2">
					<Tooltip>
						<TooltipTrigger asChild>
							<Button variant="ghost" size="icon" disabled={!mail}>
								<Reply className="h-4 w-4" />
								<span className="sr-only">Reply</span>
							</Button>
						</TooltipTrigger>
						<TooltipContent>Reply</TooltipContent>
					</Tooltip>
					<Tooltip>
						<TooltipTrigger asChild>
							<Button variant="ghost" size="icon" disabled={!mail}>
								<ReplyAll className="h-4 w-4" />
								<span className="sr-only">Reply all</span>
							</Button>
						</TooltipTrigger>
						<TooltipContent>Reply all</TooltipContent>
					</Tooltip>
					<Tooltip>
						<TooltipTrigger asChild>
							<Button variant="ghost" size="icon" disabled={!mail}>
								<Forward className="h-4 w-4" />
								<span className="sr-only">Forward</span>
							</Button>
						</TooltipTrigger>
						<TooltipContent>Forward</TooltipContent>
					</Tooltip>
				</div>
				<Separator orientation="vertical" className="mx-2 h-6" />
				<DropdownMenu>
					<DropdownMenuTrigger asChild>
						<Button variant="ghost" size="icon" disabled={!mail}>
							<MoreVertical className="h-4 w-4" />
							<span className="sr-only">More</span>
						</Button>
					</DropdownMenuTrigger>
					<DropdownMenuContent align="end">
						<DropdownMenuItem>Mark as unread</DropdownMenuItem>
						<DropdownMenuItem>Star thread</DropdownMenuItem>
						<DropdownMenuItem>Add label</DropdownMenuItem>
						<DropdownMenuItem>Mute thread</DropdownMenuItem>
					</DropdownMenuContent>
				</DropdownMenu>
			</div> */}
			<Separator />

			<ChatMessageList>
				{messages.map((message, index) => {
					const variant = message.sender === "user" ? "sent" : "received";
					return (
						<ChatBubble key={message.id} variant={variant}>
							<ChatBubbleAvatar fallback={variant === "sent" ? "US" : "AI"} />
							<ChatBubbleMessage isLoading={message.isLoading}>
								{message.message}
							</ChatBubbleMessage>
							{/* Action Icons */}
							<ChatBubbleActionWrapper>
								{actionIcons.map(({ icon: Icon, type }) => (
									<ChatBubbleAction
										className="size-7"
										key={type}
										icon={<Icon className="size-4" />}
										onClick={() =>
											console.log(
												"Action " + type + " clicked for message " + index
											)
										}
									/>
								))}
							</ChatBubbleActionWrapper>
						</ChatBubble>
					);
				})}
			</ChatMessageList>

			<form className="relative rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring p-1">
				<ChatInput
					placeholder="Type your message here..."
					className="min-h-12 resize-none rounded-lg bg-background border-0 p-3 shadow-none focus-visible:ring-0"
				/>
				<div className="flex items-center p-3 pt-0">
					<Button variant="ghost" size="icon">
						<Paperclip className="size-4" />
						<span className="sr-only">Attach file</span>
					</Button>

					<Button variant="ghost" size="icon">
						<Mic className="size-4" />
						<span className="sr-only">Use Microphone</span>
					</Button>

					<Button size="sm" className="ml-auto gap-1.5">
						Send Message
						<CornerDownLeft className="size-3.5" />
					</Button>
				</div>
			</form>
		</div>
	);
}
