import { User } from "@supabase/supabase-js";

export type { User };

export interface Email {
  id: string;
  subject: string;
  sender: string;
  body?: string;
  created_at?: string;
}

export interface EmailAction {
  id: string;
  user_id: string;
  email_id: string;
  requires_action: boolean;
  waiting_on_someone: boolean;
  priority: "high" | "medium" | "low";
  tasks?: string[];
  emails?: Email;
  created_at?: string;
}

export interface DatabaseEmailAction {
  id: string;
  user_id: string;
  email_id: string;
  requires_action: boolean;
  waiting_on_someone: boolean;
  priority: "high" | "medium" | "low";
  tasks: string[];
  emails: Email;
}
