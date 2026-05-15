import React from 'react';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'slate';
}

export const Badge = ({ className = '', variant = 'slate', ...props }: BadgeProps) => {
  const baseStyles = 'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2';
  const variants = {
    primary: 'bg-[var(--color-primary-subtle)] text-[var(--color-primary)] hover:bg-[var(--color-primary-subtle)]/80',
    secondary: 'bg-[var(--color-secondary-subtle)] text-[var(--color-secondary)] hover:bg-[var(--color-secondary-subtle)]/80',
    success: 'bg-[var(--color-success-subtle)] text-[var(--color-success)] hover:bg-[var(--color-success-subtle)]/80',
    warning: 'bg-[var(--color-warning-subtle)] text-[var(--color-warning)] hover:bg-[var(--color-warning-subtle)]/80',
    error: 'bg-[var(--color-error-subtle)] text-[var(--color-error)] hover:bg-[var(--color-error-subtle)]/80',
    slate: 'bg-[var(--color-bg-subtle)] text-[var(--color-text-muted)] hover:bg-[var(--color-bg-subtle)]/80',
  };

  return <span className={`${baseStyles} ${variants[variant]} ${className}`} {...props} />;
};
