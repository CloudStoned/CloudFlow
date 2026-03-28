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

export async function getEmails(userId: string) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/emails/list/${userId}`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to get emails");
  }

  return response.json();
}
