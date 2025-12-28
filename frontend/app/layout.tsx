import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { authClient } from "@/lib/auth";
import { AuthProvider } from "better-auth/react";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TaskFlow - Manage Your Tasks Efficiently",
  description: "A modern todo application built with Next.js and FastAPI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen bg-gray-50 dark:bg-gray-900`}
      >
        <AuthProvider client={authClient}>{children}</AuthProvider>
      </body>
    </html>
  );
}
