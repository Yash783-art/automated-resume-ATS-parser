import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'flat' | 'elevated' | 'glass';
}

export const Card = ({ className = '', variant = 'flat', ...props }: CardProps) => {
  const baseStyles = 'rounded-[var(--radius-lg)] border border-[var(--color-border)] p-6 transition-all overflow-hidden';
  const variants = {
    flat: 'bg-[var(--color-bg-card)]',
    elevated: 'bg-[var(--color-bg-card)] shadow-[var(--shadow-md)] hover:shadow-[var(--shadow-lg)]',
    glass: 'bg-white/70 backdrop-blur-md border-white/20 shadow-sm',
  };

  return <div className={`${baseStyles} ${variants[variant]} ${className}`} {...props} />;
};

export const CardHeader = ({ className = '', ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={`mb-4 flex items-center justify-between ${className}`} {...props} />
);

export const CardTitle = ({ className = '', ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3 className={`text-lg font-semibold text-[var(--color-text-main)] ${className}`} {...props} />
);

export const CardDescription = ({ className = '', ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
  <p className={`text-sm text-[var(--color-text-muted)] ${className}`} {...props} />
);

export const CardContent = ({ className = '', ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={`${className}`} {...props} />
);

export const CardFooter = ({ className = '', ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={`mt-6 pt-4 border-t border-[var(--color-border)] ${className}`} {...props} />
);
