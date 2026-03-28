"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";
import { fetchNewEmails } from "@/app/actions/emails";

export default function Dashboard() {
  const { user, loading, signOut } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [user, loading]);

  if (loading) return <div>Loading...</div>;
  if (!user) return null;

  const handleFetchEmails = async () => {
    console.log("Fetching emails...");
    await fetchNewEmails(user.id);
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center space-x-4">
          {user.avatar_url && <img src={user.avatar_url} alt="Profile" className="w-10 h-10 rounded-full" />}
          <div>
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <p className="text-gray-600">Welcome, {user.name || user.full_name || user.email}</p>
          </div>
        </div>
        <Button onClick={signOut} variant="outline">
          Sign Out
        </Button>
      </div>
      <Button style={{ cursor: "pointer" }} onClick={handleFetchEmails}>
        Fetch Emails
      </Button>
    </div>
  );
}
