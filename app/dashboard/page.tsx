import getUser from "@/lib/get-user";
import { GmailButton } from "@/components/dashboard/GmailButton";

export default async function DashboardPage() {
  const user = await getUser();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg h-96 flex items-center justify-center">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900 mb-4">Welcome to CloudFlow Dashboard</h1>
              <p className="text-gray-600 mb-2">Logged in as: {user.email}</p>
              <p className="text-sm text-gray-500">Day 1-2 setup complete! Ready for Gmail integration.</p>
              <div className="mt-4">
                <GmailButton userId={user.id} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
