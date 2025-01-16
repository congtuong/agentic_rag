"use client";

import * as React from "react";
import {
	Bot,
	Check,
	ChevronsUpDown,
	FileText,
	Layers,
	MessagesSquare,
	PlusCircleIcon,
	Search,
} from "lucide-react";

import { cn } from "@/lib/utils";
import { Input } from "@/components/ui/input";
import {
	ResizableHandle,
	ResizablePanel,
	ResizablePanelGroup,
} from "@/components/ui/resizable";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ChatDisplay } from "@/components/user/chat-display";
import { ConversationList } from "@/components/user/conversation-list";
import { Nav } from "@/components/user/nav";
import {
	Command,
	CommandEmpty,
	CommandGroup,
	CommandInput,
	CommandItem,
	CommandList,
} from "@/components/ui/command";
import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from "@/components/ui/popover";
import { Button } from "../ui/button";
import {
	IAPIResponse,
	IChatBotResponse,
	IConversationResponse,
	IMessageResponse,
} from "@/types";
import { fetchWithToken } from "@/api/auth";
import { useToast } from "@/hooks/use-toast";
import { NewConversation } from "./new-conversation";

interface ConversationProps {
	defaultLayout: number[] | undefined;
	defaultCollapsed?: boolean;
	navCollapsedSize: number;
}

export function Conversations({
	defaultLayout = [20, 32, 48],
	defaultCollapsed = false,
	navCollapsedSize,
}: ConversationProps) {
	const [isCollapsed, setIsCollapsed] = React.useState(defaultCollapsed);
	const [open, setOpen] = React.useState(false);
	const [selectedConversation, setSelectedConversation] =
		React.useState<IConversationResponse | null>(null);
	const [conversations, setConversations] = React.useState<
		IConversationResponse[]
	>([]);
	const [chatbots, setChatbots] = React.useState<IChatBotResponse[]>([]);
	const [selectedChatbot, setSelectedChatbot] =
		React.useState<IChatBotResponse | null>(null);
	const [messages, setMessages] = React.useState<IMessageResponse[]>([]);

	const { toast } = useToast();
	React.useEffect(() => {
		const fetchChatbots = async () => {
			try {
				const response = await fetchWithToken(
					`${process.env.NEXT_PUBLIC_API_URL}/knowledges/chatbot/list`,
					"GET"
				);

				if (!response.ok) {
					toast({
						title: "Failed to fetch chatbots",
					});
					return;
				}

				const data: IAPIResponse<IChatBotResponse[]> = await response.json();

				setChatbots(data.data);
				setSelectedChatbot(data.data[0]);
			} catch (error) {
				toast({
					title: "Failed to fetch chatbots",
				});
			}
		};
		fetchChatbots();
	}, []);

	React.useEffect(() => {
		const fetchConversation = async () => {
			try {
				const response = await fetchWithToken(
					`${process.env.NEXT_PUBLIC_API_URL}/agents/${selectedChatbot?.id}/conversations/list`,
					"GET"
				);

				if (!response.ok) {
					toast({
						title: "Failed to fetch conversation",
					});
					return;
				}

				const data: IAPIResponse<IConversationResponse[]> =
					await response.json();

				setConversations(data.data);
				setSelectedConversation(data.data[0]);
				toast({
					title: "Fetched conversation",
				});
			} catch (error) {
				toast({
					title: "Failed to fetch conversation",
				});
			}
		};
		if (selectedChatbot) {
			fetchConversation();
		}
	}, [selectedChatbot]);

	React.useEffect(() => {
		const fetchMessages = async () => {
			try {
				const response = await fetchWithToken(
					`${process.env.NEXT_PUBLIC_API_URL}/agents/conversation/${selectedConversation?.id}`,
					"GET"
				);

				if (!response.ok) {
					toast({
						title: "Failed to fetch messages",
					});
					return;
				}

				const data: IAPIResponse<IMessageResponse[]> = await response.json();

				setMessages(data.data);
				toast({
					title: "Fetched messages",
				});
			} catch (error) {
				toast({
					title: "Failed to fetch messages",
				});
			}
		};
		if (selectedConversation) {
			fetchMessages();
		}
	}, [selectedConversation]);

	return (
		<TooltipProvider delayDuration={0}>
			<ResizablePanelGroup
				direction="horizontal"
				onLayout={(sizes: number[]) => {
					document.cookie = `react-resizable-panels:layout:mail=${JSON.stringify(
						sizes
					)}`;
				}}
				className="h-full max-h-svh items-stretch"
			>
				<ResizablePanel
					defaultSize={defaultLayout[0]}
					collapsedSize={navCollapsedSize}
					collapsible={true}
					minSize={15}
					maxSize={20}
					onCollapse={() => {
						setIsCollapsed(true);
						document.cookie = `react-resizable-panels:collapsed=${JSON.stringify(
							true
						)}`;
					}}
					onResize={() => {
						setIsCollapsed(false);
						document.cookie = `react-resizable-panels:collapsed=${JSON.stringify(
							false
						)}`;
					}}
					className={cn(
						isCollapsed &&
							"min-w-[50px] transition-all duration-300 ease-in-out"
					)}
				>
					<div
						className={cn(
							"flex h-[52px] items-center justify-center",
							isCollapsed ? "h-[52px]" : "px-2"
						)}
					>
						{/* <AccountSwitcher isCollapsed={isCollapsed} accounts={accounts} /> */}
					</div>
					<Separator />
					<Nav isCollapsed={isCollapsed} />
				</ResizablePanel>
				<ResizableHandle withHandle />
				<ResizablePanel defaultSize={defaultLayout[1]} minSize={30}>
					<Tabs defaultValue="all">
						<div className="flex items-center px-4 py-2">
							<h1 className="text-xl font-bold">Conversations</h1>
							<TabsList className="ml-auto">
								<Popover open={open} onOpenChange={setOpen}>
									<PopoverTrigger asChild>
										<Button
											variant="outline"
											role="combobox"
											aria-expanded={open}
											className="w-[200px] justify-between truncate"
										>
											{selectedChatbot
												? chatbots.find(
														(chatbot) => chatbot.id === selectedChatbot.id
												  )?.id
												: "Select chatbot..."}
											<ChevronsUpDown className="opacity-50" />
										</Button>
									</PopoverTrigger>
									<PopoverContent className="w-[200px] p-0">
										<Command>
											<CommandInput
												placeholder="Search chatbot..."
												className="h-9"
											/>
											<CommandList>
												<CommandEmpty>No chatbot found.</CommandEmpty>
												<CommandGroup>
													{chatbots.map((chatbot) => (
														<CommandItem
															key={chatbot.id}
															value={chatbot.id}
															onSelect={(currentValue) => {
																console.log(currentValue);
																setSelectedChatbot(
																	chatbots.find(
																		(chatbot) => chatbot.id === currentValue
																	) || null
																);
																setOpen(false);
															}}
														>
															{chatbot.id}
															<Check
																className={cn(
																	"ml-auto",
																	selectedChatbot?.id === chatbot.id
																		? "opacity-100"
																		: "opacity-0"
																)}
															/>
														</CommandItem>
													))}
												</CommandGroup>
											</CommandList>
										</Command>
									</PopoverContent>
								</Popover>
							</TabsList>
						</div>
						<Separator />
						<div className="bg-background/95 p-4 backdrop-blur supports-[backdrop-filter]:bg-background/60">
							<NewConversation
								chatbots={chatbots}
								setSelectedConversation={setSelectedConversation}
								setSelectedChatbot={setSelectedChatbot}
								setConversations={setConversations}
							/>
						</div>
						<Separator />
						<div className="bg-background/95 p-4 backdrop-blur supports-[backdrop-filter]:bg-background/60">
							<form>
								<div className="relative">
									<Search className="absolute left-2 top-2 h-4 w-4 text-muted-foreground" />
									<Input placeholder="Search" className="pl-8" />
								</div>
							</form>
						</div>
						<div>
							<TabsContent value="all" className="m-0">
								<ConversationList
									items={conversations}
									setSelectedConversation={setSelectedConversation}
									selectedConversation={selectedConversation}
								/>
							</TabsContent>
						</div>
					</Tabs>
				</ResizablePanel>
				<ResizableHandle withHandle />
				<ResizablePanel defaultSize={defaultLayout[2]} minSize={30}>
					<ChatDisplay
						items={messages}
						selectedConversation={selectedConversation}
					/>
				</ResizablePanel>
			</ResizablePanelGroup>
		</TooltipProvider>
	);
}
