import { cookies } from "next/headers";
import { ChatBots } from "@/components/chatbots";

const ChatbotsPage = () => {
	const layout = cookies().get("react-resizable-panels:layout:mail");
	const collapsed = cookies().get("react-resizable-panels:collapsed");
	return (
		<div className="h-screen">
			<ChatBots
				defaultLayout={layout ? JSON.parse(layout.value) : undefined}
				defaultCollapsed={collapsed ? JSON.parse(collapsed.value) : undefined}
				navCollapsedSize={4}
			/>
		</div>
	);
};

export default ChatbotsPage;
