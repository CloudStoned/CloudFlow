import { supabaseAdmin } from "./admin";

export async function saveRefreshToken(userId: string, refreshToken: string) {
  const { error } = await supabaseAdmin.from("user_tokens").upsert({
    user_id: userId,
    google_refresh_token: refreshToken,
    updated_at: new Date(),
  });

  if (error) {
    throw error;
  }
}
