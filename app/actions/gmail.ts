import { api } from "@/lib/api";

export async function testGmailConnection(userId: string) {
  return fetch(api(`/gmail/test/${userId}`)).then((r) => r.json());
}

export async function saveRefreshToken(user_id: string, refresh_token: string) {
  return fetch(api("/gmail/save-refresh-token"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id, refresh_token }),
  }).then((r) => r.json());
}
