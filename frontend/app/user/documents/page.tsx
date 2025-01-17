import { Documents } from "@/components/documents";
import { cookies } from "next/headers";

const DocumentsPage = () => {
	const layout = cookies().get("react-resizable-panels:layout:mail");
	const collapsed = cookies().get("react-resizable-panels:collapsed");
	return (
		<div className="h-screen">
			<Documents
				defaultLayout={layout ? JSON.parse(layout.value) : undefined}
				defaultCollapsed={collapsed ? JSON.parse(collapsed.value) : undefined}
				navCollapsedSize={4}
			/>
		</div>
	);
};

export default DocumentsPage;
