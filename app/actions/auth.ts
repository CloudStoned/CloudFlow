import { createSupabaseServer } from "@/lib/supabase/server";

export async function linkGmailAccount() {
  const supabase = await createSupabaseServer();
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (session?.provider_token) {
    const response = await fetch("http://localhost:8000/auth/link-gmail", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider_token: session.provider_token,
        refresh_token: session.refresh_token,
        user_id: session.user.id,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to link Gmail account");
    }

    return response.json();
  }

  throw new Error("No provider token available");
}
