"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { createSupabaseBrowser } from "@/lib/supabase/client";

export default function AuthCallback() {
  const router = useRouter();
  const supabase = createSupabaseBrowser();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const accessToken = params.get("access_token");
    const refreshToken = params.get("refresh_token");

    if (accessToken && refreshToken) {
      // Restore the session on the frontend Supabase client
      supabase.auth
        .setSession({
          access_token: accessToken,
          refresh_token: refreshToken,
        })
        .then(({ error }) => {
          if (error) {
            router.push("/login?error=session_failed");
          } else {
            router.push("/dashboard");
          }
        });
    } else {
      router.push("/login?error=missing_tokens");
    }
  }, []);
}
