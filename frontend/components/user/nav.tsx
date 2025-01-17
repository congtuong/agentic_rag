"use client";

import Link from "next/link";

import { cn } from "@/lib/utils";
import { buttonVariants } from "@/components/ui/button";
import {
	Tooltip,
	TooltipContent,
	TooltipTrigger,
} from "@/components/ui/tooltip";
import { NavElements } from "@/constants";
import { LucideIcon, Settings } from "lucide-react";

interface NavProps {
	isCollapsed: boolean;
	links?: {
		title: string;
		label?: string;
		icon: LucideIcon;
		variant: "default" | "ghost";
		href: string;
	}[];
	current?: string;
}

export function Nav({
	links = NavElements,
	isCollapsed,
	current = "Conversations",
}: NavProps) {
	links = links.map((link) => ({
		...link,
		variant: link.title === current ? "default" : "ghost",
	}));

	return (
		<div className="flex flex-col justify-between h-full">
			<div
				data-collapsed={isCollapsed}
				className="group flex flex-col gap-4 py-2 data-[collapsed=true]:py-2 justify-"
			>
				<nav className="grid gap-1 px-2 group-[[data-collapsed=true]]:justify-center group-[[data-collapsed=true]]:px-2">
					{links.map((link, index) =>
						isCollapsed ? (
							<Tooltip key={index} delayDuration={0}>
								<TooltipTrigger asChild>
									<Link
										href={link.href}
										className={cn(
											buttonVariants({ variant: link.variant, size: "icon" }),
											"h-9 w-9",
											link.variant === "default" &&
												"dark:bg-muted dark:text-muted-foreground dark:hover:bg-muted dark:hover:text-white"
										)}
									>
										<link.icon className="h-4 w-4" />
										<span className="sr-only">{link.title}</span>
									</Link>
								</TooltipTrigger>
								<TooltipContent
									side="right"
									className="flex items-center gap-4"
								>
									{link.title}
									{/* {link.label && (
									<span className="ml-auto text-muted-foreground">
										{link.label}
									</span>
								)} */}
								</TooltipContent>
							</Tooltip>
						) : (
							<Link
								key={index}
								href={link.href}
								className={cn(
									buttonVariants({ variant: link.variant, size: "sm" }),
									link.variant === "default" &&
										"dark:bg-muted dark:text-white dark:hover:bg-muted dark:hover:text-white",
									"justify-start"
								)}
							>
								<link.icon className="mr-2 h-4 w-4" />
								{link.title}
								{/* {link.label && (
								<span
									className={cn(
										"ml-auto",
										link.variant === "default" &&
											"text-background dark:text-white"
									)}
								>
									{link.label}
								</span>
							)} */}
							</Link>
						)
					)}
				</nav>
			</div>
			<div className="grid gap-1 px-2 group-[[data-collapsed=true]]:justify-center group-[[data-collapsed=true]]:px-2 py-2 data-[collapsed=true]:py-2">
				{isCollapsed ? (
					<Tooltip delayDuration={0}>
						<TooltipTrigger asChild>
							<Link
								href={"#"}
								className={cn(
									buttonVariants({
										variant: current === "Settings" ? "default" : "ghost",
										size: "icon",
									}),
									"h-9 w-9",
									(current === "Settings" ? "default" : "ghost") ===
										"default" &&
										"dark:bg-muted dark:text-muted-foreground dark:hover:bg-muted dark:hover:text-white"
								)}
							>
								<Settings className="h-4 w-4" />
								<span className="sr-only">Settings</span>
							</Link>
						</TooltipTrigger>
						<TooltipContent side="right" className="flex items-center gap-4">
							{"Settings"}
							{/* {link.label && (
									<span className="ml-auto text-muted-foreground">
										{link.label}
									</span>
								)} */}
						</TooltipContent>
					</Tooltip>
				) : (
					<Link
						key={-1}
						href={"#"}
						className={cn(
							buttonVariants({
								variant: current === "Settings" ? "default" : "ghost",
								size: "sm",
							}),
							(current === "Settings" ? "default" : "ghost") === "default" &&
								"dark:bg-muted dark:text-white dark:hover:bg-muted dark:hover:text-white",
							"justify-start",
							"group-[[data-collapsed=true]]:hidden"
						)}
					>
						<Settings className="mr-2 h-4 w-4" />
						{"Settings"}
						{/* {link.label && (
										<span
											className={cn(
												"ml-auto",
												link.variant === "default" &&
													"text-background dark:text-white"
											)}
										>
											{link.label}
										</span>
									)} */}
					</Link>
				)}
			</div>
		</div>
	);
}
