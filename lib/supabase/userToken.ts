import { google } from "googleapis";
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

export async function getGmailClient(user_id: string) {
  const { data: tokens } = await supabaseAdmin
    .from("user_tokens")
    .select("google_refresh_token")
    .eq("user_id", user_id)
    .single();

  if (!tokens?.google_refresh_token) {
    throw new Error("No refresh token found for user");
  }

  const oauth2Client = new google.auth.OAuth2();
  oauth2Client.setCredentials({
    refresh_token: tokens.google_refresh_token,
  });

  return google.gmail({ version: "v1", auth: oauth2Client });
}

export async function testGmailConnection(user_id: string) {
  const gmail = await getGmailClient(user_id);
  const { data } = await gmail.users.labels.list({
    userId: "me",
  });
  return data;
}
