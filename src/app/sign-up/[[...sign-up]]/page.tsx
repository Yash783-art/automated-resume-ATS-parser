import { SignUp } from "@clerk/nextjs";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Create Account",
  description: "Create your ATS Parser account to start analysing resumes instantly.",
};

export default function SignUpPage() {
  return (
    <main
      id="main-content"
      className="min-h-screen flex items-center justify-center px-4"
      style={{ background: "var(--color-bg)" }}
    >
      {/* Background accent blobs */}
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 overflow-hidden"
      >
        <div
          className="absolute -top-32 -right-32 w-96 h-96 rounded-full opacity-10"
          style={{ background: "var(--color-primary)" }}
        />
        <div
          className="absolute -bottom-24 left-1/4 w-72 h-72 rounded-full opacity-5"
          style={{ background: "var(--color-match)" }}
        />
      </div>

      <div className="relative z-10 flex flex-col items-center gap-6">
        {/* Wordmark */}
        <a href="/" className="flex items-center gap-1 text-xl font-semibold" style={{ color: "var(--color-text-head)" }}>
          ATS<span style={{ color: "var(--color-primary)" }}>Parser</span>
        </a>

        <SignUp
          appearance={{
            variables: {
              colorPrimary: "#6366F1",
              colorBackground: "#FFFFFF",
              colorText: "#0F172A",
              colorTextSecondary: "#475569",
              colorInputBackground: "#F8FAFC",
              colorInputText: "#0F172A",
              borderRadius: "10px",
              fontFamily: "var(--font-sans)",
            },
          }}
        />
      </div>
    </main>
  );
}
