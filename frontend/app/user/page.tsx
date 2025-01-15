import { Mail } from "@/components/user/mail";
import { cookies } from "next/headers";
import { accounts, mails } from "@/components/user/temp";

const UserPage = () => {
	const layout = cookies().get("react-resizable-panels:layout:mail");
	const collapsed = cookies().get("react-resizable-panels:collapsed");
	const defaultLayout = layout ? JSON.parse(layout.value) : undefined;
	const defaultCollapsed = collapsed ? JSON.parse(collapsed.value) : undefined;
	return (
		<div>
			<Mail
				accounts={accounts}
				mails={mails}
				defaultLayout={defaultLayout}
				defaultCollapsed={defaultCollapsed}
				navCollapsedSize={4}
			/>
		</div>
	);
};

export default UserPage;
