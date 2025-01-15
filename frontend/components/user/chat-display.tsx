import {
	Copy,
	CornerDownLeft,
	Mic,
	Paperclip,
	RefreshCcwIcon,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
	ChatBubble,
	ChatBubbleAvatar,
	ChatBubbleMessage,
	ChatBubbleAction,
	ChatBubbleActionWrapper,
} from "@/components/ui/chat/chat-bubble";
import { ChatMessageList } from "@/components/ui/chat/chat-message-list";
import { ChatInput } from "@/components/ui/chat/chat-input";
import {
	IAPIResponse,
	IChatResponse,
	IConversationResponse,
	IMessageResponse,
} from "@/types";
import React from "react";
import { ScrollArea } from "../ui/scroll-area";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { ChatFormProps } from "@/types/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { fetchWithToken } from "@/api/auth";
import { useToast } from "@/hooks/use-toast";
import { Form, FormControl, FormField, FormItem } from "../ui/form";
import { Input } from "../ui/input";

interface Message {
	id: string;
	message: string;
	sender: string;
	isLoading?: boolean;
}

export function ChatDisplay({
	items,
	selectedConversation,
}: {
	items: IMessageResponse[];
	selectedConversation: IConversationResponse | null;
}) {
	const { toast } = useToast();
	const [messages, setMessages] = React.useState<Message[]>([]);
	const actionIcons = [
		{ icon: Copy, type: "Copy" },
		{ icon: RefreshCcwIcon, type: "Regenerate" },
	];
	const form = useForm<z.infer<typeof ChatFormProps>>({
		resolver: zodResolver(ChatFormProps),
		defaultValues: {
			query: "",
		},
	});
	const chatContainerRef = React.useRef<HTMLDivElement>(null);

	const scrollToBottom = () => {
		chatContainerRef.current?.scrollIntoView(false);
	};

	React.useEffect(() => {
		scrollToBottom();
	}, [messages]);

	React.useEffect(() => {
		scrollToBottom();
	}, []);

	React.useEffect(() => {
		setMessages(
			items.map((item) => ({
				id: item.id,
				message: item.content,
				sender: item.type === "user" ? "user" : "bot",
			}))
		);
	}, [items]);

	const handleChat = async (values: z.infer<typeof ChatFormProps>) => {
		if (!selectedConversation) {
			toast({
				title: "No conversation selected",
			});
			return;
		}
		if (messages[messages.length - 1].isLoading) {
			toast({
				title: "Please wait for the bot to respond",
			});
			return;
		}

		try {
			form.reset();
			const tempID = Math.random().toString(36).substring(7);
			const tempBotID = Math.random().toString(36).substring(7);
			setMessages((prev) => [
				...prev,
				{
					id: tempID,
					message: values.query,
					sender: "user",
				},
				{
					id: tempBotID,
					message: "...",
					sender: "bot",
					isLoading: true,
				},
			]);

			const response = await fetchWithToken(
				`${process.env.NEXT_PUBLIC_API_URL}/agents/conversation/chat`,
				"POST",
				{
					query: values.query,
					conversation_id: selectedConversation?.id,
				}
			);

			if (!response.ok) {
				toast({
					title: "Failed to send message",
				});
				return;
			}

			const data: IAPIResponse<IChatResponse> = await response.json();

			setMessages((prev) =>
				prev.map((message) => {
					if (message.id === tempBotID) {
						return {
							id: data.data.response.id,
							message: data.data.response.content,
							sender: "bot",
						};
					}
					if (message.id === tempID) {
						return {
							id: data.data.query.id,
							message: data.data.query.content,
							sender: "user",
						};
					}
					return message;
				})
			);
		} catch (error) {
			toast({
				title: "Failed to send message",
			});
		}
	};

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

			<ScrollArea className="flex-1">
				<div ref={chatContainerRef}>
					<ChatMessageList>
						{messages.map((message, index) => {
							const variant = message.sender === "user" ? "sent" : "received";
							return (
								<ChatBubble key={message.id} variant={variant}>
									<ChatBubbleAvatar
										fallback={variant === "sent" ? "US" : "AI"}
									/>
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
				</div>
			</ScrollArea>
			<Form {...form}>
				<form
					className="relative rounded-lg border bg-background focus-within:ring-1 focus-within:ring-ring p-1"
					onSubmit={form.handleSubmit(handleChat)}
				>
					<FormField
						control={form.control}
						name="query"
						render={({ field }) => (
							<FormItem>
								<FormControl>
									<ChatInput
										id="query"
										placeholder="Type your message here..."
										className="min-h-12 resize-none rounded-lg bg-background border-0 p-3 shadow-none focus-visible:ring-0"
										required
										{...field}
									/>
								</FormControl>
							</FormItem>
						)}
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

						<Button size="sm" className="ml-auto gap-1.5" type="submit">
							Send Message
							<CornerDownLeft className="size-3.5" />
						</Button>
					</div>
				</form>
			</Form>
		</div>
	);
}
