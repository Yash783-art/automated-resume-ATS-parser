import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className = '', label, error, icon, ...props }, ref) => {
    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label className="text-sm font-medium text-[var(--color-text-main)]">
            {label}
          </label>
        )}
        <div className="relative group">
          {icon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)] transition-colors group-focus-within:text-[var(--color-primary)]">
              {icon}
            </div>
          )}
          <input
            ref={ref}
            className={`
              flex h-10 w-full rounded-[var(--radius-md)] border border-[var(--color-border)] 
              bg-[var(--color-bg-card)] px-3 py-2 text-sm ring-offset-background 
              file:border-0 file:bg-transparent file:text-sm file:font-medium 
              placeholder:text-[var(--color-text-muted)] 
              focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] focus:ring-offset-1
              disabled:cursor-not-allowed disabled:opacity-50 
              transition-all
              ${icon ? 'pl-10' : ''}
              ${error ? 'border-[var(--color-error)] focus:ring-[var(--color-error)]' : ''}
              ${className}
            `}
            {...props}
          />
        </div>
        {error && (
          <p className="text-xs text-[var(--color-error)] font-medium">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
