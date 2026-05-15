'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { FileText, Search, Filter, Download } from 'lucide-react';
import Link from 'next/link';
import { useApi } from '@/hooks/use-api';

export default function ResumesListPage() {
  const { data: resumes, isLoading, isError } = useApi('/api/resume/list');
  
  console.log("📂 Resumes Data:", resumes);
  if (isError) console.error("❌ API Error on Resume List:", isError);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">My Resumes</h1>
          <p className="text-slate-500">View and manage your candidate pool.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">
            <Filter className="mr-2 w-4 h-4" />
            Filter
          </Button>
          <Link href="/dashboard/upload">
            <Button size="sm">
              <FileText className="mr-2 w-4 h-4" />
              Upload New
            </Button>
          </Link>
        </div>
      </div>

      <Card>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-500 uppercase bg-slate-50 border-b">
                <tr>
                  <th className="px-6 py-4 font-medium">Candidate / File</th>
                  <th className="px-6 py-4 font-medium">Top Match</th>
                  <th className="px-6 py-4 font-medium">Status</th>
                  <th className="px-6 py-4 font-medium">Date</th>
                  <th className="px-6 py-4 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {resumes?.length > 0 ? (
                  resumes.map((resume: any) => (
                    <tr key={resume.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded bg-indigo-50 flex items-center justify-center">
                            <FileText className="w-4 h-4 text-indigo-600" />
                          </div>
                          <div>
                            <p className="font-semibold text-slate-900">{resume.filename}</p>
                            <p className="text-xs text-slate-400">{resume.candidate_name || 'Processing...'}</p>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        {resume.best_score ? (
                          <div className="flex items-center gap-2">
                            <Badge variant={resume.best_score >= 80 ? 'success' : 'primary'}>
                              {resume.best_score}%
                            </Badge>
                            <span className="text-xs text-slate-500 truncate max-w-[120px]">
                              {resume.best_job_title}
                            </span>
                          </div>
                        ) : (
                          <span className="text-slate-400">N/A</span>
                        )}
                      </td>
                      <td className="px-6 py-4">
                        <Badge variant="secondary" className="capitalize">
                          {resume.status}
                        </Badge>
                      </td>
                      <td className="px-6 py-4 text-slate-500">
                        {new Date(resume.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-right">
                        <Link href={`/dashboard/resumes/${resume.id}`}>
                          <Button variant="ghost" size="sm">View Report</Button>
                        </Link>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="px-6 py-12 text-center text-slate-500">
                      {isLoading ? 'Loading resumes...' : 'No resumes found. Start by uploading one!'}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
