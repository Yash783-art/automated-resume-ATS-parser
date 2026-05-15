'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface ScoreBarProps {
  label: string;
  score: number;
  maxScore?: number;
}

export const ScoreBar = ({ label, score, maxScore = 100 }: ScoreBarProps) => {
  const percentage = Math.min(100, Math.max(0, (score / maxScore) * 100));
  
  const color = percentage >= 80 ? 'var(--color-success)' : percentage >= 50 ? 'var(--color-primary)' : 'var(--color-error)';

  return (
    <div className="w-full space-y-2">
      <div className="flex justify-between items-end">
        <span className="text-sm font-semibold text-[var(--color-text-main)]">{label}</span>
        <span className="text-sm font-bold" style={{ color }}>{Math.round(score)}%</span>
      </div>
      <div className="h-2 w-full bg-[var(--color-border)] rounded-full overflow-hidden opacity-30">
        <motion.div
          className="h-full rounded-full"
          style={{ backgroundColor: color }}
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
      </div>
    </div>
  );
};
