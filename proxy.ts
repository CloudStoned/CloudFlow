import { NextResponse, type NextRequest } from "next/server";
import { createServerClient } from "@/lib/supabase/server";

export async function proxy(request: NextRequest) {
  let response = NextResponse.next({ request });

  const supabase = await createServerClient();

  const protectedRoutes = ["/dashboard"];
  const authRoutes = ["/login"];

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user && protectedRoutes.some((route) => request.nextUrl.pathname.startsWith(route))) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (user && authRoutes.some((route) => request.nextUrl.pathname.startsWith(route))) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return response;
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
