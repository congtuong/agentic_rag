import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from "@/components/ui/popover";
import { Button } from "../ui/button";
import { Label } from "../ui/label";
import { Check, ChevronsUpDown, PlusCircleIcon } from "lucide-react";
import {
	Command,
	CommandEmpty,
	CommandGroup,
	CommandInput,
	CommandItem,
	CommandList,
} from "@/components/ui/command";
import { cn } from "@/lib/utils";
import { useState } from "react";
import { IAPIResponse, IChatBotResponse, IConversationResponse } from "@/types";
import { fetchWithToken } from "@/api/auth";
import { useToast } from "@/hooks/use-toast";

interface NewConversationProps {
	chatbots: IChatBotResponse[];
	setSelectedConversation: React.Dispatch<
		React.SetStateAction<IConversationResponse | null>
	>;
	setConversations: React.Dispatch<
		React.SetStateAction<IConversationResponse[]>
	>;
	setSelectedChatbot: React.Dispatch<
		React.SetStateAction<IChatBotResponse | null>
	>;
}

export function NewConversation({
	chatbots,
	setSelectedConversation,
	setConversations,
	setSelectedChatbot,
}: NewConversationProps) {
	const [open, setOpen] = useState(false);
	const [selectedBot, setSelectedBot] = useState<IChatBotResponse | null>(null);
	const { toast } = useToast();

	const handleNewConversation = async () => {
		if (!selectedBot) {
			return;
		}

		try {
			const response = await fetchWithToken(
				`${process.env.NEXT_PUBLIC_API_URL}/agents/conversation/create?chatbot_id=${selectedBot.id}`,
				"POST"
			);

			if (response.ok) {
				const data = await response.json();
				const conversation: IConversationResponse = {
					id: data.data.conversation_id,
					chatbot_id: selectedBot.id,
					user_id: data.data.username,
				};
				setSelectedConversation(conversation);
				setConversations((prev) => [conversation, ...prev]);
				setSelectedChatbot(selectedBot);
				setOpen(false);
			} else {
				const data = await response.json();
				toast({
					title: "Failed to start conversation",
					description: data.message,
				});
			}
		} catch (error) {
			toast({
				title: "Failed to start conversation",
				description: `${error}`,
			});
		}
	};
	return (
		<Popover>
			<PopoverTrigger asChild>
				<Button variant="default" className="w-full">
					<PlusCircleIcon className="h-4 w-4" />
				</Button>
			</PopoverTrigger>
			<PopoverContent className="w-80">
				<div className="grid gap-4">
					<div className="space-y-2">
						<h4 className="font-medium leading-none">New Conversation</h4>
						<p className="text-sm text-muted-foreground">
							Select the chatbot you want to start a conversation with.
						</p>
					</div>
					<div className="grid gap-2">
						<div className="grid grid-cols-3 items-center gap-4">
							<Popover open={open} onOpenChange={setOpen}>
								<PopoverTrigger asChild>
									<Button
										variant="outline"
										role="combobox"
										aria-expanded={open}
										className="justify-between truncate w-72"
									>
										{selectedBot
											? chatbots.find(
													(chatbot) => chatbot.id === selectedBot.id
											  )?.id
											: "Select chatbot..."}
										<ChevronsUpDown className="opacity-50" />
									</Button>
								</PopoverTrigger>
								<PopoverContent className="w-full p-0">
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
															setSelectedBot(
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
																selectedBot?.id === chatbot.id
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
						</div>
					</div>
					<div className="flex justify-end">
						<Button variant="default" onClick={handleNewConversation}>
							Start Conversation
						</Button>
					</div>
				</div>
			</PopoverContent>
		</Popover>
	);
}
