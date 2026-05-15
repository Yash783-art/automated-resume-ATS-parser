import React from 'react';
import { Check, X } from 'lucide-react';

interface SkillTagProps {
  name: string;
  status?: 'matched' | 'missing' | 'neutral';
  className?: string;
}

export const SkillTag = ({ name, status = 'neutral', className = '' }: SkillTagProps) => {
  const baseStyles = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium transition-all select-none border';
  
  const variants = {
    matched: 'bg-[var(--color-success-subtle)] text-[var(--color-success)] border-[var(--color-success)]/20 shadow-sm',
    missing: 'bg-[var(--color-error-subtle)] text-[var(--color-error)] border-[var(--color-error)]/20',
    neutral: 'bg-[var(--color-bg-subtle)] text-[var(--color-text-muted)] border-[var(--color-border)]',
  };

  return (
    <div className={`${baseStyles} ${variants[status]} ${className}`}>
      {status === 'matched' && <Check className="w-3.5 h-3.5 stroke-[3]" />}
      {status === 'missing' && <X className="w-3.5 h-3.5 stroke-[3]" />}
      <span>{name}</span>
    </div>
  );
};
