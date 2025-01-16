"use client";

import { Nav } from "@/components/user/nav";
import { cookies } from "next/headers";
import { useState } from "react";
import {
	ResizableHandle,
	ResizablePanel,
	ResizablePanelGroup,
} from "@/components/ui/resizable";
import { TooltipProvider } from "@radix-ui/react-tooltip";
import { Separator } from "@radix-ui/react-separator";
import { cn } from "@/lib/utils";

interface ChatbotsProps {
	defaultLayout: number[] | undefined;
	defaultCollapsed?: boolean;
	navCollapsedSize: number;
}

const ChatbotsPage = ({
	defaultLayout = [20, 80],
	defaultCollapsed = false,
	navCollapsedSize,
}: ChatbotsProps) => {
	const [isCollapsed, setIsCollapsed] = useState(false);
	return (
		<div>
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
						<Nav isCollapsed={isCollapsed} current={"Knowledge"} />
						<Separator />
					</ResizablePanel>
					<ResizableHandle withHandle />
					<ResizablePanel
						defaultSize={defaultLayout[1]}
						minSize={30}
					></ResizablePanel>
				</ResizablePanelGroup>
			</TooltipProvider>
		</div>
	);
};

export default ChatbotsPage;
