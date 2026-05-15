"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { UserButton } from "@clerk/nextjs";
import { IconFileText } from "@tabler/icons-react";

const NAV_LINKS = [
  { href: "/dashboard/upload",     label: "Dashboard" },
  { href: "/dashboard/batch",      label: "Candidates" },
  { href: "/dashboard/templates",  label: "Job Descriptions" },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header
      className="sticky top-0 z-50 w-full"
      style={{
        background: "var(--color-surface)",
        borderBottom: "0.5px solid var(--color-border)",
        boxShadow: "var(--shadow-card)",
      }}
    >
      <nav
        className="mx-auto flex max-w-7xl items-center gap-4 px-6 h-14"
        aria-label="Main navigation"
      >
        {/* ── Wordmark ── */}
        <Link
          href="/"
          className="flex items-center gap-1.5 text-[15px] font-semibold shrink-0 mr-2"
          style={{ color: "var(--color-text-head)" }}
        >
          <IconFileText
            size={18}
            stroke={1.8}
            style={{ color: "var(--color-primary)" }}
            aria-hidden="true"
          />
          ATS<span style={{ color: "var(--color-primary)" }}>Parser</span>
        </Link>

        {/* ── Nav links ── */}
        <div className="hidden sm:flex items-center gap-1 flex-1">
          {NAV_LINKS.map(({ href, label }) => {
            const isActive = pathname?.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className="text-[13px] px-3 py-1.5 rounded-[8px] transition-colors duration-150"
                style={{
                  color: isActive ? "var(--color-primary)" : "var(--color-text-muted)",
                  background: isActive ? "rgba(99,102,241,0.08)" : "transparent",
                  fontWeight: isActive ? 500 : 400,
                }}
              >
                {label}
              </Link>
            );
          })}
        </div>

        {/* ── Right side ── */}
        <div className="flex items-center gap-3 ml-auto">
          <Link
            href="/dashboard/upload"
            className="hidden sm:inline-flex items-center gap-1.5 text-[13px] font-medium px-4 py-2 rounded-[10px] transition-colors duration-150"
            style={{
              background: "var(--color-primary)",
              color: "#fff",
            }}
            onMouseEnter={(e) => {
              (e.currentTarget as HTMLAnchorElement).style.background = "var(--color-primary-dark)";
            }}
            onMouseLeave={(e) => {
              (e.currentTarget as HTMLAnchorElement).style.background = "var(--color-primary)";
            }}
          >
            Upload Resume
          </Link>

          <UserButton
            afterSignOutUrl="/"
            appearance={{
              variables: {
                colorPrimary: "#6366F1",
                borderRadius: "10px",
              },
            }}
          />
        </div>
      </nav>
    </header>
  );
}
