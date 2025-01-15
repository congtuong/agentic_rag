import { Toaster } from "@/components/ui/toaster";
import { AuthProvider } from "@/hooks/use-auth";
import { Metadata } from "next";

export const metadata: Metadata = {
	title: "User",
};

export default function AuthenLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<html lang="en">
			<body>
				<AuthProvider>
					<div className="flex-grow">{children}</div>
					<Toaster />
				</AuthProvider>
			</body>
		</html>
	);
}
