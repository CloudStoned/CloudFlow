"use client";

import { Button } from "@/components/ui/button";

interface GmailButtonProps {
  userId: string;
}

export function GmailButton({ userId }: GmailButtonProps) {
  const fetchGmailData = async () => {
    const response = await fetch(`/api/gmail?userId=${userId}`);
    console.log("RESPONSE", response);
  };

  return <Button onClick={fetchGmailData}>Get Gmail Data</Button>;
}
