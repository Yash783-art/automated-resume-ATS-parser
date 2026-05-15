'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { UserButton } from '@clerk/nextjs';
import { 
  LayoutDashboard, 
  FileText, 
  Briefcase, 
  BarChart3, 
  PlusCircle,
  Menu,
  X
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const NAV_ITEMS = [
  { label: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { label: 'My Resumes', href: '/dashboard/resumes', icon: FileText },
  { label: 'Job Descriptions', href: '/dashboard/jds', icon: Briefcase },
  { label: 'Analytics', href: '/dashboard/analytics', icon: BarChart3 },
];

export const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  return (
    <div className="flex h-screen bg-[var(--color-bg-subtle)] overflow-hidden">
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex w-64 flex-col bg-white border-r border-[var(--color-border)] shadow-sm">
        <div className="p-6">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-xl font-bold tracking-tight">
              ATS<span className="text-[var(--color-primary)]">Parser</span>
            </span>
          </Link>
        </div>
        
        <nav className="flex-1 px-4 space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`
                  flex items-center gap-3 px-3 py-2 rounded-[var(--radius-md)] text-sm font-medium transition-all
                  ${isActive 
                    ? 'bg-[var(--color-primary-subtle)] text-[var(--color-primary)]' 
                    : 'text-[var(--color-text-muted)] hover:bg-[var(--color-bg-subtle)] hover:text-[var(--color-text-main)]'}
                `}
              >
                <item.icon className={`w-4 h-4 ${isActive ? 'text-[var(--color-primary)]' : ''}`} />
                {item.label}
                {isActive && (
                  <motion.div 
                    layoutId="active-pill"
                    className="ml-auto w-1 h-4 bg-[var(--color-primary)] rounded-full"
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
                )}
              </Link>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-[var(--color-border)] flex items-center justify-between">
          <UserButton afterSignOutUrl="/" showName />
        </div>
      </aside>

      {/* Mobile Header */}
      <div className="flex flex-col flex-1 overflow-hidden">
        <header className="md:hidden flex items-center justify-between p-4 bg-white border-b border-[var(--color-border)]">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-lg font-bold tracking-tight">
              ATS<span className="text-[var(--color-primary)]">Parser</span>
            </span>
          </Link>
          <button 
            onClick={() => setIsMobileMenuOpen(true)}
            className="p-2 text-[var(--color-text-muted)]"
          >
            <Menu className="w-6 h-6" />
          </button>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-4 md:p-8">
          <div className="max-w-6xl mx-auto animate-in fade-in duration-500">
            {children}
          </div>
        </main>
      </div>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsMobileMenuOpen(false)}
              className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 md:hidden"
            />
            <motion.div 
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed right-0 top-0 bottom-0 w-3/4 bg-white z-50 p-6 md:hidden shadow-2xl"
            >
              <div className="flex justify-between items-center mb-8">
                <span className="text-xl font-bold">Menu</span>
                <button onClick={() => setIsMobileMenuOpen(false)}>
                  <X className="w-6 h-6 text-[var(--color-text-muted)]" />
                </button>
              </div>
              <nav className="space-y-4">
                {NAV_ITEMS.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className="flex items-center gap-4 p-3 rounded-lg hover:bg-[var(--color-bg-subtle)]"
                  >
                    <item.icon className="w-5 h-5 text-[var(--color-primary)]" />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                ))}
              </nav>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
};
