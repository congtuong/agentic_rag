import { ComponentProps } from "react";

import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { IConversationResponse } from "@/types";

export function ConversationList({
	items,
	setSelectedConversation,
	selectedConversation,
}: {
	items: IConversationResponse[];
	setSelectedConversation: React.Dispatch<
		React.SetStateAction<IConversationResponse | null>
	>;
	selectedConversation: IConversationResponse | null;
}) {
	return (
		<ScrollArea className="h-screen max-h-[calc(100vh-7rem)]">
			<div className="flex flex-col gap-2 p-4 pt-0">
				{items.map((item) => (
					<button
						key={item.id}
						className={cn(
							"flex flex-col items-start gap-2 rounded-lg border p-3 text-left text-sm transition-all hover:bg-accent",
							selectedConversation?.id === item.id && "bg-muted"
						)}
						onClick={() => {
							if (selectedConversation?.id !== item.id) {
								setSelectedConversation((prev) =>
									prev?.id === item.id ? null : item
								);
							}
						}}
					>
						<div className="flex w-full flex-col gap-1">
							<div className="flex items-center">
								<div className="flex items-center gap-2">
									<div className="font-semibold">{item.id}</div>
								</div>
							</div>
							{/* <div className="text-xs font-medium">{item.user_id}</div> */}
						</div>
						<div className="line-clamp-2 text-xs text-muted-foreground">
							{item.user_id}
						</div>
					</button>
				))}
			</div>
		</ScrollArea>
	);
}

function getBadgeVariantFromLabel(
	label: string
): ComponentProps<typeof Badge>["variant"] {
	if (["work"].includes(label.toLowerCase())) {
		return "default";
	}

	if (["personal"].includes(label.toLowerCase())) {
		return "outline";
	}

	return "secondary";
}
