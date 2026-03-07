"use server";

import { createSupabaseServer } from "@/lib/supabase/server";
import { EmailAction } from "@/lib/types";

export async function loadEmails(userId: string): Promise<EmailAction[]> {
  const supabase = await createSupabaseServer();
  const { data, error } = await supabase.from("email_actions").select("*, emails(*)").eq("user_id", userId);

  if (error) {
    throw new Error("Failed to load emails");
  }

  return data || [];
}

export async function fetchNewEmails(userId: string) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/emails/fetch/${userId}`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch new emails");
  }

  return response.json();
}
