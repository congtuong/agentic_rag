"use client";

import { Nav } from "@/components/user/nav";
import { useEffect, useState } from "react";
import {
	ResizableHandle,
	ResizablePanel,
	ResizablePanelGroup,
} from "@/components/ui/resizable";
import { ColumnDef } from "@tanstack/react-table";

import { Expense } from "@/components/ui/data-table-components/schema";
import { DataTableColumnHeader } from "@/components/ui/data-table-components/data-table-column-header";
import { DataTableRowActions } from "@/components/ui/data-table-components/data-table-row-actions";
import { TrendingUp, TrendingDown, User, Users } from "lucide-react";
import { TooltipProvider } from "@radix-ui/react-tooltip";
import { Separator } from "@radix-ui/react-separator";
import { cn } from "@/lib/utils";
import { DataTable } from "@/components/ui/data-table-components/data-table";
import { IAPIResponse, IChatBotResponse, IKnowledgesResponse } from "@/types";
import { fetchWithToken } from "@/api/auth";
import { useToast } from "@/hooks/use-toast";
import { Checkbox } from "./ui/checkbox";
import { useAuth } from "@/hooks/use-auth";

interface KnowledgesProps {
	defaultLayout: number[] | undefined;
	defaultCollapsed?: boolean;
	navCollapsedSize: number;
}

export const columns: ColumnDef<Expense>[] = [
	{
		id: "select",
		header: ({ table }) => (
			<Checkbox
				checked={
					table.getIsAllPageRowsSelected() ||
					(table.getIsSomePageRowsSelected() && "indeterminate")
				}
				onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
				aria-label="Select all"
				className="translate-y-0.5"
			/>
		),
		cell: ({ row }) => (
			<Checkbox
				checked={row.getIsSelected()}
				onCheckedChange={(value) => row.toggleSelected(!!value)}
				aria-label="Select row"
				className="translate-y-0.5"
			/>
		),
		enableSorting: false,
		enableHiding: false,
	},
	{
		accessorKey: "id",
		header: ({ column }) => (
			<DataTableColumnHeader column={column} title="ID" />
		),
		cell: ({ row }) => (
			<div className="w-[150px] capitalize">{row.getValue("id")}</div>
		),
		enableSorting: false,
		enableHiding: false,
	},
	{
		accessorKey: "user_id",
		header: ({ column }) => (
			<DataTableColumnHeader column={column} title="User ID" />
		),

		cell: ({ row }) => {
			return (
				<div className="flex space-x-2">
					<span className="max-w-[500px] truncate font-medium capitalize">
						{row.getValue("user_id")}
					</span>
				</div>
			);
		},
	},
	{
		accessorKey: "name",
		header: ({ column }) => (
			<DataTableColumnHeader column={column} title="Name" />
		),

		cell: ({ row }) => {
			return (
				<div className="flex space-x-2">
					<span className="max-w-[500px] truncate font-medium capitalize">
						{row.getValue("name")}
					</span>
				</div>
			);
		},
	},

	// {
	// 	accessorKey: "category",
	// 	header: ({ column }) => (
	// 		<DataTableColumnHeader column={column} title="Category" />
	// 	),
	// 	cell: ({ row }) => {
	// 		return (
	// 			<div className="flex w-[100px] items-center">
	// 				<span className="capitalize"> {row.getValue("category")}</span>
	// 			</div>
	// 		);
	// 	},
	// 	filterFn: (row, id, value) => {
	// 		return value.includes(row.getValue(id));
	// 	},
	// },

	// {
	// 	accessorKey: "type",
	// 	header: ({ column }) => (
	// 		<DataTableColumnHeader column={column} title="Type" />
	// 	),
	// 	cell: ({ row }) => {
	// 		const type = row.getValue("type");
	// 		return (
	// 			<div className="flex w-[100px] items-center">
	// 				{type === "private" ? (
	// 					<User size={20} className="mr-2 text-green-500" />
	// 				) : (
	// 					<Users size={20} className="mr-2 text-red-500" />
	// 				)}

	// 				<span className="capitalize"> {row.getValue("type")}</span>
	// 			</div>
	// 		);
	// 	},
	// 	filterFn: (row, id, value) => {
	// 		return value.includes(row.getValue(id));
	// 	},
	// },

	{
		accessorKey: "created_at",
		header: ({ column }) => (
			<DataTableColumnHeader column={column} title="Created Date" />
		),
		cell: ({ row }) => {
			const date = new Date(row.getValue("created_at"));
			const formattedDate = date.toLocaleDateString("en-US", {
				day: "2-digit",

				month: "short",

				year: "numeric",
			});
			return (
				<div className="flex w-[100px] items-center">
					<span className="capitalize">{formattedDate}</span>
				</div>
			);
		},

		filterFn: (row, id, value) => {
			const rowDate = new Date(row.getValue(id));
			const [startDate, endDate] = value;
			return rowDate >= startDate && rowDate <= endDate;
		},
	},

	{
		accessorKey: "updated_at",
		header: ({ column }) => (
			<DataTableColumnHeader column={column} title="Updated Date" />
		),
		cell: ({ row }) => {
			const date = new Date(row.getValue("updated_at"));
			const formattedDate = date.toLocaleDateString("en-US", {
				day: "2-digit",

				month: "short",

				year: "numeric",
			});
			return (
				<div className="flex w-[100px] items-center">
					<span className="capitalize">{formattedDate}</span>
				</div>
			);
		},

		filterFn: (row, id, value) => {
			const rowDate = new Date(row.getValue(id));
			const [startDate, endDate] = value;
			return rowDate >= startDate && rowDate <= endDate;
		},
	},
	{
		id: "actions",
		cell: ({ row }) => <DataTableRowActions row={row} />,
	},
];

export function Knowledges({
	defaultLayout = [20, 80],
	defaultCollapsed = false,
	navCollapsedSize,
}: KnowledgesProps) {
	const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);
	const [knowledges, setKnowledges] = useState<IKnowledgesResponse[]>([]);
	const { toast } = useToast();
	const { accessToken } = useAuth();

	useEffect(() => {
		const fetchKnowledges = async () => {
			try {
				const response = await fetchWithToken(
					`${process.env.NEXT_PUBLIC_API_URL}/knowledges/knowledge/list`,
					"GET"
				);

				if (!response.ok) {
					toast({
						title: "Failed to fetch chatbots",
					});
					return;
				}

				const data: IAPIResponse<IKnowledgesResponse[]> = await response.json();

				setKnowledges(data.data);
			} catch (error) {
				toast({
					title: "Failed to fetch chatbots",
				});
			}
		};
		fetchKnowledges();
	}, [accessToken]);

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
					maxSize={15}
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
					{/* <div
						className={cn(
							"flex h-[52px] items-center justify-center",
							isCollapsed ? "h-[52px]" : "px-2"
						)}
					>
						<AccountSwitcher isCollapsed={isCollapsed} accounts={accounts} />
					</div> */}
					<Nav isCollapsed={isCollapsed} current={"Knowledge"} />
					<Separator />
				</ResizablePanel>
				<ResizableHandle withHandle />
				<ResizablePanel defaultSize={defaultLayout[1]} minSize={30}>
					<DataTable data={knowledges} columns={columns} filterShow={true} />
				</ResizablePanel>
			</ResizablePanelGroup>
		</TooltipProvider>
	);
}
