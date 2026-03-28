"use server";

export async function fetchNewEmails(userId: string) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/emails/fetch/${userId}`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch new emails");
  }

  return response.json();
}
