CREATE TABLE user_tokens (
  user_id UUID REFERENCES auth.users(id) PRIMARY KEY,
  google_refresh_token TEXT,
  updated_at TIMESTAMP DEFAULT NOW()
);