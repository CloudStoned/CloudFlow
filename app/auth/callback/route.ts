import { createServerClient } from "@/lib/supabase/server";
import { saveRefreshToken } from "@/app/actions/gmail";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  console.log("REQUEST", request.url);
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");

  if (code) {
    const supabase = await createServerClient();
    const {
      data: { session },
      error,
    } = await supabase.auth.exchangeCodeForSession(code);

    if (session?.provider_refresh_token) {
      await saveRefreshToken(session.user.id, session.provider_refresh_token);
    }

    if (!error) {
      return NextResponse.redirect(new URL("/dashboard", request.url));
    }
  }

  return NextResponse.redirect(new URL("/login", request.url));
}
