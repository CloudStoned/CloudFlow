export async function getCurrentUser() {
  try {
    const res = await fetch("http://localhost:8000/auth/me", {
      credentials: "include",
    });

    if (res.status === 401) {
      return null;
    }

    if (!res.ok) {
      throw new Error("Failed to fetch user");
    }

    const data = await res.json();
    if (!data) {
      return null;
    }

    return {
      id: data.user.id,
      email: data.user.email,
      name: data.user.user_metadata?.name || data.user.user_metadata?.full_name,
      avatar_url: data.user.user_metadata?.avatar_url || data.user.user_metadata?.picture,
      full_name: data.user.user_metadata?.full_name,
      picture: data.user.user_metadata?.picture,
    };
  } catch (error) {
    console.error("Error fetching user:", error);
    return null;
  }
}

export async function signOut() {
  try {
    await fetch("http://localhost:8000/auth/logout", {
      method: "POST",
      credentials: "include",
      redirect: "manual",
    });

    window.location.href = "http://localhost:3000/login";
  } catch (error) {
    console.error("Error signing out:", error);
    throw error;
  }
}
