import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EdgeCase",
  description:
    "Conflict-aware assurance for security, ethics, and energy trade-offs in agentic systems.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
