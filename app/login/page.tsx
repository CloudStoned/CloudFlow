"use client";
import { useState } from "react";
import { createSupabaseBrowser } from "@/lib/supabase/client";
import { useRouter } from "next/navigation";
import { GoogleIcon } from "@/components/icons/GoogleIcon";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function handleLogin() {
    setLoading(true);
    const supabase = createSupabaseBrowser();
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      alert(error.message);
      setLoading(false);
      return;
    }
    router.push("/dashboard");
  }

  async function handleSignup() {
    setLoading(true);
    const supabase = createSupabaseBrowser();
    const { error } = await supabase.auth.signUp({ email, password });
    if (error) {
      alert(error.message);
      setLoading(false);
      return;
    }
    alert("Check your email to confirm your account!");
    setLoading(false);
  }

  async function handleGoogleLogin() {
    setLoading(true);
    window.location.href = "http://localhost:8000/auth/google";
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-6 text-center">CloudFlow</h1>
        <input
          className="w-full border p-2 rounded mb-3"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="w-full border p-2 rounded mb-4"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="w-full bg-blue-600 text-white p-2 rounded mb-2" onClick={handleLogin} disabled={loading}>
          {loading ? "Loading..." : "Login"}
        </button>
        <button className="w-full border p-2 rounded" onClick={handleSignup} disabled={loading}>
          Create Account
        </button>

        {/* Divider */}
        <div className="flex items-center gap-2 mb-4">
          <div className="flex-1 h-px bg-gray-200" />
          <span className="text-sm text-gray-400">or</span>
          <div className="flex-1 h-px bg-gray-200" />
        </div>

        <button
          className="w-full border p-2 rounded flex items-center justify-center gap-3"
          onClick={handleGoogleLogin}
          disabled={loading}
        >
          <GoogleIcon />
          <span className="text-sm font-medium">Sign in with Google</span>
        </button>
      </div>
    </div>
  );
}
