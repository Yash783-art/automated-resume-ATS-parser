'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Briefcase, Plus } from 'lucide-react';
import Link from 'next/link';

export default function JDsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Job Descriptions</h1>
          <p className="text-slate-500">Manage your job requirements and templates.</p>
        </div>
        <Link href="/dashboard/upload">
          <Button>
            <Plus className="mr-2 w-4 h-4" />
            Create New JD
          </Button>
        </Link>
      </div>

      <Card>
        <CardContent className="flex flex-col items-center justify-center py-12">
          <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mb-4">
            <Briefcase className="w-6 h-6 text-slate-400" />
          </div>
          <h3 className="text-lg font-semibold">No Job Descriptions Yet</h3>
          <p className="text-slate-500 text-center max-w-sm mb-6">
            Create your first job description to start matching it against candidate resumes.
          </p>
          <Link href="/dashboard/upload">
            <Button variant="outline">Get Started</Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}
