'use client';

import React from 'react';
import { UploadZone } from '@/components/ui/UploadZone';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Badge } from '@/components/ui/Badge';
import { 
  FileText, 
  ArrowRight, 
  CheckCircle2, 
  AlertCircle,
  Clock
} from 'lucide-react';
import { toast } from 'sonner';
import { apiUpload, apiPost } from '@/hooks/use-api';
import { useAuth } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';

export default function UploadPage() {
  const { userId } = useAuth();
  const router = useRouter();
  const [isUploading, setIsUploading] = React.useState(false);
  const [jdContent, setJdContent] = React.useState('');
  const [isProcessing, setIsProcessing] = React.useState(false);

  const handleUpload = async (files: File[]) => {
    if (!userId) return;
    if (!jdContent.trim()) {
      toast.error("Please provide a job description first.");
      return;
    }

    setIsUploading(true);
    const toastId = toast.loading(`Uploading ${files.length} resumes...`);

    try {
      // 1. Process JD first
      const jdResult = await apiPost('/api/jd/process', {
        content: jdContent,
        title: "New Analysis"
      }, userId);

      // 2. Upload Resumes
      const formData = new FormData();
      files.forEach(file => formData.append('files', file));
      
      const uploadResults = await apiUpload('/api/resume/batch-upload', formData, userId);
      
      toast.success("Resumes uploaded successfully!", { id: toastId });
      
      // 3. Start processing (In a real app, we'd show a progress list and poll)
      // For this MVP, we'll just redirect to the first result or dashboard
      setIsProcessing(true);
      toast.info("Analyzing resumes... this may take a few seconds.");
      
      // Simulate delay for parsing
      setTimeout(() => {
        router.push('/dashboard/resumes');
      }, 3000);

    } catch (error) {
      toast.error("Failed to process resumes. Please try again.", { id: toastId });
      console.error(error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">Analyze Resumes</h1>
        <p className="text-slate-500">Upload candidates and match them against your job requirements.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Side: JD Input */}
        <div className="lg:col-span-1 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Job Description</CardTitle>
            </CardHeader>
            <CardContent>
              <textarea
                placeholder="Paste the job requirements here..."
                className="w-full h-64 p-4 rounded-[var(--radius-md)] border border-[var(--color-border)] bg-[var(--color-bg-subtle)] text-sm focus:outline-none focus:ring-2 focus:ring-[var(--color-primary)] transition-all resize-none"
                value={jdContent}
                onChange={(e) => setJdContent(e.target.value)}
              />
              <div className="mt-2 flex justify-between items-center">
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">{jdContent.length} chars</span>
                <Button 
                  size="xs" 
                  variant={jdContent.length > 100 ? "primary" : "outline"}
                  disabled={jdContent.length < 100}
                  onClick={() => toast.success("JD Captured! Now drop your resumes on the right.")}
                >
                  {jdContent.length > 100 ? <><CheckCircle2 className="w-3 h-3 mr-1" /> Ready</> : "Min 100 chars"}
                </Button>
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-slate-900 text-white border-none">
            <h4 className="font-bold text-sm mb-2">How it works</h4>
            <ul className="space-y-3 text-xs text-slate-400">
              <li className="flex items-start gap-2">
                <div className="mt-0.5"><CheckCircle2 className="w-3 h-3 text-emerald-500" /></div>
                <span>Paste the JD to extract key requirements and skills.</span>
              </li>
              <li className="flex items-start gap-2">
                <div className="mt-0.5"><CheckCircle2 className="w-3 h-3 text-emerald-500" /></div>
                <span>Upload one or more PDF resumes (max 10MB each).</span>
              </li>
              <li className="flex items-start gap-2">
                <div className="mt-0.5"><CheckCircle2 className="w-3 h-3 text-emerald-500" /></div>
                <span>AI scores each candidate and identifies gaps.</span>
              </li>
            </ul>
          </Card>
        </div>

        {/* Right Side: Upload Zone */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Resume Upload</CardTitle>
              <CardDescription>Drag and drop up to 10 PDF resumes at once.</CardDescription>
            </CardHeader>
            <CardContent>
              <UploadZone 
                onUpload={handleUpload} 
                isUploading={isUploading} 
              />
            </CardContent>
          </Card>

          {isProcessing && (
            <div className="flex items-center gap-3 p-4 bg-indigo-50 border border-indigo-100 rounded-[var(--radius-md)] animate-pulse">
              <Clock className="w-5 h-5 text-indigo-600 animate-spin-slow" />
              <div className="flex-1">
                <p className="text-sm font-bold text-indigo-900">Analysis in progress...</p>
                <p className="text-xs text-indigo-600">Our AI is extracting skills and scoring candidates.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
