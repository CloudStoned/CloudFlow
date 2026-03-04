"use client";

import { Button } from "@/components/ui/button";
import { createClient } from "@/lib/supabase/client";
export function GoogleSignInButton() {
  const handleGoogleSignIn = async () => {
    const supabase = createClient();

    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${location.origin}/auth/callback`,
        scopes: "https://www.googleapis.com/auth/gmail.readonly email profile",
        queryParams: {
          access_type: "offline",
          prompt: "consent",
        },
      },
    });

    if (error) {
      console.error("Google sign-in error:", error.message);
    }
  };

  return (
    <Button onClick={handleGoogleSignIn} className="w-full">
      Sign in with Google
    </Button>
  );
}
