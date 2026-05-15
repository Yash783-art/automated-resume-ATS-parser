import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import { Toaster } from "sonner";
import "./globals.css";

/* ─── Fonts ──────────────────────────────────────────────────────────────────
   Geist Sans  →  --font-sans  (body / UI text)
   Geist Mono  →  --font-mono  (scores / percentages)
──────────────────────────────────────────────────────────────────────────────*/
const geistSans = Geist({
  variable: "--font-sans",
  subsets: ["latin"],
  display: "swap",
});

const geistMono = Geist_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "ATS Parser — Resume Analysis & Match Scoring",
    template: "%s | ATS Parser",
  },
  description:
    "Upload a PDF resume, paste a job description, and get an instant ATS match score with keyword-level insights. Built for HR teams, founders, and job seekers.",
  keywords: ["ATS", "resume parser", "job match score", "hiring", "HR", "recruitment"],
  authors: [{ name: "ATS Parser" }],
  openGraph: {
    title: "ATS Parser — Resume Analysis & Match Scoring",
    description:
      "Instant ATS resume analysis. Upload a PDF, paste a JD, get a match score in under 15 seconds.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html
        lang="en"
        className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
      >
        <body
          className="min-h-full flex flex-col"
          style={{
            background: "var(--color-bg)",
            color: "var(--color-text-body)",
            fontFamily: "var(--font-sans)",
          }}
        >
          {/* Skip-to-main — WCAG 2.4.1 */}
          <a href="#main-content" className="skip-to-main">
            Skip to main content
          </a>
          {children}
          <Toaster position="top-center" richColors />
        </body>
      </html>
    </ClerkProvider>
  );
}
