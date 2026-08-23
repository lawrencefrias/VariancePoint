import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "VariancePoint",
  description: "Technology Futures Intelligence Platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>{children}</body>
    </html>
  );
}
