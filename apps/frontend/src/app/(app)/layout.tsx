import { Sidebar } from "@/components/layout/Sidebar";
import { Topbar } from "@/components/layout/Topbar";
import { GoalProvider } from "@/components/GoalContext";

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <GoalProvider>
      <div className="flex h-screen w-full flex-col overflow-hidden bg-background">
        <Topbar />
        <div className="flex flex-1 overflow-hidden">
          <Sidebar />
          <main className="flex-1 overflow-y-auto p-8">{children}</main>
        </div>
      </div>
    </GoalProvider>
  );
}
