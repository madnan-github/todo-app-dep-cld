"use client";

import { useState, useEffect, useCallback } from "react";
import { signIn, signUp, signOut, useSession } from "better-auth/react";
import type { SignUpFormData, SignInFormData } from "@/types";

export function useAuth() {
  const { data: session, isLoading } = useSession();
  const [error, setError] = useState<string | null>(null);

  const signInWithEmail = useCallback(
    async (data: SignInFormData) => {
      setError(null);
      try {
        const result = await signIn({
          email: data.email,
          password: data.password,
        });
        return result;
      } catch (err: any) {
        setError(err.message || "Sign in failed");
        throw err;
      }
    },
    []
  );

  const signUpWithEmail = useCallback(
    async (data: SignUpFormData) => {
      setError(null);
      try {
        const result = await signUp({
          email: data.email,
          password: data.password,
          name: data.name,
        });
        return result;
      } catch (err: any) {
        setError(err.message || "Sign up failed");
        throw err;
      }
    },
    []
  );

  const logout = useCallback(async () => {
    setError(null);
    try {
      await signOut();
    } catch (err: any) {
      setError(err.message || "Sign out failed");
      throw err;
    }
  }, []);

  return {
    user: session?.user,
    isAuthenticated: !!session,
    isLoading,
    error,
    signIn: signInWithEmail,
    signUp: signUpWithEmail,
    signOut: logout,
  };
}
