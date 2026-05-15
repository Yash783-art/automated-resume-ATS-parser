'use client';

import React from 'react';
import { UploadCloud, File, X, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from './Button';

interface UploadZoneProps {
  onUpload: (files: File[]) => void;
  maxFiles?: number;
  accept?: string;
  isUploading?: bool;
}

export const UploadZone = ({ 
  onUpload, 
  maxFiles = 10, 
  accept = ".pdf",
  isUploading = false 
}: UploadZoneProps) => {
  const [isDragging, setIsDragging] = React.useState(false);
  const [selectedFiles, setSelectedFiles] = React.useState<File[]>([]);
  const fileInputRef = React.useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      addFiles(Array.from(e.target.files));
    }
  };

  const addFiles = (newFiles: File[]) => {
    const validFiles = newFiles.filter(f => f.type === "application/pdf" || f.name.endsWith(".pdf"));
    setSelectedFiles(prev => [...prev, ...validFiles].slice(0, maxFiles));
  };

  const removeFile = (index: number) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUploadClick = () => {
    if (selectedFiles.length > 0) {
      onUpload(selectedFiles);
    }
  };

  return (
    <div className="w-full space-y-4">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`
          relative border-2 border-dashed rounded-[var(--radius-lg)] p-12
          flex flex-col items-center justify-center text-center cursor-pointer
          transition-all duration-200
          ${isDragging 
            ? 'border-[var(--color-primary)] bg-[var(--color-primary-subtle)]/30 scale-[1.01]' 
            : 'border-[var(--color-border)] hover:border-[var(--color-primary)] bg-white hover:bg-[var(--color-bg-subtle)]'}
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple={maxFiles > 1}
          accept={accept}
          onChange={handleFileChange}
          className="hidden"
        />
        
        <div className="p-4 rounded-full bg-[var(--color-primary-subtle)] mb-4">
          <UploadCloud className="w-8 h-8 text-[var(--color-primary)]" />
        </div>
        
        <h3 className="text-lg font-bold text-[var(--color-text-main)] mb-1">
          Drop PDF resume here
        </h3>
        <p className="text-sm text-[var(--color-text-muted)]">
          or click to browse from your computer
        </p>
        <p className="mt-4 text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
          PDF · max 10MB · batch up to {maxFiles}
        </p>
      </div>

      {/* Selected Files List */}
      <AnimatePresence>
        {selectedFiles.length > 0 && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="space-y-2"
          >
            {selectedFiles.map((file, index) => (
              <div 
                key={`${file.name}-${index}`}
                className="flex items-center justify-between p-3 bg-white border border-[var(--color-border)] rounded-[var(--radius-md)] shadow-sm"
              >
                <div className="flex items-center gap-3">
                  <File className="w-4 h-4 text-[var(--color-primary)]" />
                  <span className="text-sm font-medium truncate max-w-[200px]">{file.name}</span>
                  <span className="text-xs text-[var(--color-text-muted)]">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
                </div>
                <button 
                  onClick={(e) => { e.stopPropagation(); removeFile(index); }}
                  className="p-1 hover:bg-slate-100 rounded-full text-slate-400 hover:text-slate-600 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            ))}
            
            <div className="pt-4 flex justify-end">
              <Button 
                onClick={handleUploadClick} 
                isLoading={isUploading}
                className="w-full md:w-auto min-w-[150px]"
              >
                Upload {selectedFiles.length} {selectedFiles.length === 1 ? 'Resume' : 'Resumes'}
              </Button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
