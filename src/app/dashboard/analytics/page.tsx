'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { BarChart3 } from 'lucide-react';
import { useApi } from '@/hooks/use-api';

export default function AnalyticsPage() {
  const { data: stats, isLoading } = useApi('/api/analytics/stats');

  if (isLoading) return <div className="p-8 text-center animate-pulse">Calculating metrics...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Analytics</h1>
        <p className="text-slate-500">Track performance metrics and hiring trends.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-slate-500">Total Candidates</p>
            <p className="text-3xl font-bold">{stats?.total_candidates || 0}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-slate-500">Average Match</p>
            <p className="text-3xl font-bold">{stats?.average_match_score || 0}%</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-sm text-slate-500">Parsing Success</p>
            <p className="text-3xl font-bold">{stats?.parsing_success_rate || 0}%</p>
          </CardContent>
        </Card>
      </div>

      <Card className="h-64 flex items-center justify-center bg-slate-50 border-dashed border-2">
        <CardContent className="flex flex-col items-center text-center">
          <BarChart3 className="w-12 h-12 text-slate-300 mb-4" />
          <h3 className="text-lg font-medium text-slate-400">Trend data will appear after 10+ scans</h3>
        </CardContent>
      </Card>
    </div>
  );
}
