"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { useRouter } from "next/navigation";
import { User, EmailAction } from "@/lib/types";

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [emails, setEmails] = useState<EmailAction[]>([]);
  const [tab, setTab] = useState<"action" | "waiting" | "fyi">("action");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    async function saveGmailToken() {
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (session?.provider_token) {
        setUser(session.user);
        await fetch("http://localhost:8000/auth/link-gmail", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            provider_token: session.provider_token,
            refresh_token: session.refresh_token,
            user_id: session.user.id,
          }),
        });
      }
    }
    saveGmailToken();
  }, []);

  async function loadEmails(userId: string) {
    const { data } = await supabase.from("email_actions").select("*, emails(*)").eq("user_id", userId);
    setEmails(data || []);
  }

  async function fetchNewEmails() {
    const {
      data: { session },
    } = await supabase.auth.getSession();
    const userId = session?.user?.id;

    if (!userId) return;
    setLoading(true);
    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/emails/fetch/${userId}`, { method: "POST" });
    await loadEmails(userId);
    setLoading(false);
  }

  const filtered = emails.filter((e) => {
    if (tab === "action") return e.requires_action;
    if (tab === "waiting") return e.waiting_on_someone;
    return !e.requires_action && !e.waiting_on_someone;
  });

  const tabs = [
    ["action", "Needs Action"],
    ["waiting", "Waiting On"],
    ["fyi", "FYI"],
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">CloudFlow</h1>
          <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={fetchNewEmails} disabled={loading}>
            {loading ? "Fetching..." : "Fetch Emails"}
          </button>
        </div>

        <div className="flex gap-2 mb-4">
          {tabs.map(([id, label]) => (
            <button
              key={id}
              className={`px-4 py-2 rounded ${tab === id ? "bg-blue-600 text-white" : "bg-white border"}`}
            >
              {label}
            </button>
          ))}
        </div>

        <div className="space-y-3">
          {filtered.map((item) => (
            <div key={item.id} className="bg-white p-4 rounded-lg shadow-sm border">
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-medium">{item.emails?.subject || "No subject"}</p>
                  <p className="text-sm text-gray-500">{item.emails?.sender}</p>
                </div>
                <span
                  className={`text-xs px-2 py-1 rounded ${
                    {
                      high: "bg-red-100 text-red-700",
                      medium: "bg-yellow-100 text-yellow-700",
                      low: "bg-green-100 text-green-700",
                    }[item.priority]
                  }`}
                >
                  {item.priority}
                </span>
              </div>
              {item.tasks && item.tasks.length > 0 && (
                <ul className="mt-2 text-sm text-gray-600">
                  {item.tasks.map((t, i) => (
                    <li key={i}>• {t}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
          {filtered.length === 0 && <p className="text-gray-400 text-center py-8">No emails in this category</p>}
        </div>
      </div>
    </div>
  );
}
