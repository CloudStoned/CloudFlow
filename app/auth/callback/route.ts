import { createSupabaseServer } from "@/lib/supabase/server";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");

  if (code) {
    const supabase = await createSupabaseServer();

    const {
      data: { session },
      error,
    } = await supabase.auth.exchangeCodeForSession(code);
    if (session?.provider_token) {
      await fetch("http://localhost:8000/auth/token", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: session.user.id,
          provider_token: session.provider_token,
          provider_refresh_token: session.provider_refresh_token,
        }),
      });
    }
  }

  return NextResponse.redirect(new URL("/dashboard", request.url));
}
