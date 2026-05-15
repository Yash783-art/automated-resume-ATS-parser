'use client';

import React from 'react';
import { motion, useSpring, useTransform, animate } from 'framer-motion';

interface ScoreRingProps {
  score: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
}

export const ScoreRing = ({ score, size = 120, strokeWidth = 8, label }: ScoreRingProps) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  
  // Spring animation for the score value
  const springConfig = { damping: 20, stiffness: 60 };
  const animatedScore = useSpring(0, springConfig);
  
  React.useEffect(() => {
    animatedScore.set(score);
  }, [score, animatedScore]);

  // Transform spring value to percentage for SVG dashoffset
  const dashOffset = useTransform(
    animatedScore,
    [0, 100],
    [circumference, 0]
  );

  // Dynamic color based on score
  const color = score >= 80 ? 'var(--color-success)' : score >= 50 ? 'var(--color-primary)' : 'var(--color-error)';

  return (
    <div className="relative flex flex-col items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="-rotate-90">
        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--color-border)"
          strokeWidth={strokeWidth}
          className="opacity-20"
        />
        {/* Progress stroke */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          style={{ strokeDashoffset: dashOffset }}
          strokeLinecap="round"
          transition={{ duration: 1.2, ease: "easeOut" }}
        />
      </svg>
      
      {/* Center Text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <motion.span 
          className="text-2xl font-bold text-[var(--color-text-main)]"
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          {Math.round(score)}%
        </motion.span>
        {label && <span className="text-[10px] uppercase tracking-wider text-[var(--color-text-muted)] font-bold">{label}</span>}
      </div>
    </div>
  );
};
