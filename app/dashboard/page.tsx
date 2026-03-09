"use client";

import { useState } from "react";
import { createSupabaseBrowser } from "@/lib/supabase/client";
import { EmailAction } from "@/lib/types";
import { loadEmails, fetchNewEmails } from "@/app/actions/emails";

export default function Dashboard() {
  const [emails, setEmails] = useState<EmailAction[]>([]);
  const [tab, setTab] = useState<"action" | "waiting" | "fyi">("action");
  const [loading, setLoading] = useState(false);

  async function handleFetchNewEmails() {
    const supabase = createSupabaseBrowser();
    const {
      data: { session },
    } = await supabase.auth.getSession();
    const userId = session?.user?.id;

    if (!userId) return;

    try {
      setLoading(true);
      await fetchNewEmails(userId);
      const emails = await loadEmails(userId);
      console.log("Emails:", emails);
      setEmails(emails);
    } catch (error) {
      console.error("Error fetching emails:", error);
    } finally {
      setLoading(false);
    }
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
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded"
            onClick={handleFetchNewEmails}
            disabled={loading}
          >
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
