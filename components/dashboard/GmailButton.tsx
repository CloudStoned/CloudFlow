"use client";

import { Button } from "@/components/ui/button";
import { testGmailConnection } from "@/app/actions/gmail";

interface GmailButtonProps {
  userId: string;
}

export function GmailButton({ userId }: GmailButtonProps) {
  const fetchGmailData = async () => {
    const response = await testGmailConnection(userId);
    console.log("RESPONSE", response);
  };

  return <Button onClick={fetchGmailData}>Get Gmail Data</Button>;
}
