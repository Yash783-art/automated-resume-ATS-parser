'use client';

import React from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { 
  Plus, 
  Search, 
  History, 
  TrendingUp, 
  Briefcase,
  Upload
} from 'lucide-react';
import Link from 'next/link';
import { useApi } from '@/hooks/use-api';

export default function DashboardPage() {
  const { data: resumes, isLoading: resumesLoading } = useApi('/api/resume/list');
  const { data: statsData, isLoading: statsLoading } = useApi('/api/analytics/stats');
  const { data: jdsData } = useApi('/api/jd/list');
  
  const stats = [
    { 
      label: 'Total Resumes', 
      value: statsData?.total_candidates?.toString() || '0', 
      icon: Upload, 
      color: 'text-indigo-600', 
      bg: 'bg-indigo-50' 
    },
    { 
      label: 'Avg Match Score', 
      value: `${statsData?.average_match_score || 0}%`, 
      icon: TrendingUp, 
      color: 'text-emerald-600', 
      bg: 'bg-emerald-50' 
    },
    { 
      label: 'Active Jobs', 
      value: jdsData?.length?.toString() || '0', 
      icon: Briefcase, 
      color: 'text-amber-600', 
      bg: 'bg-amber-50' 
    },
  ];

  const recentMatches = (resumes || []).slice(0, 3).map((r: any) => ({
    id: r.id,
    name: r.candidate_name || r.filename,
    jd: r.best_job_title || "Pending Analysis",
    score: r.best_score || 0,
    date: new Date(r.created_at).toLocaleDateString()
  }));

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Dashboard</h1>
          <p className="text-slate-500">Track and optimize your candidate pipeline.</p>
        </div>
        <div className="flex gap-3">
          <Link href="/dashboard/upload">
            <Button className="shadow-lg">
              <Plus className="mr-2 w-4 h-4" />
              New Resume
            </Button>
          </Link>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat) => (
          <Card key={stat.label} variant="elevated">
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-xl ${stat.bg}`}>
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
              <div>
                <p className="text-sm font-medium text-slate-500">{stat.label}</p>
                <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Matches */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <div className="flex items-center gap-2">
              <History className="w-5 h-5 text-slate-400" />
              <CardTitle>Recent Match Activity</CardTitle>
            </div>
            <Link href="/dashboard/resumes">
              <Button variant="ghost" size="sm">View All</Button>
            </Link>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentMatches.map((match, i) => (
                <div 
                  key={i}
                  className="flex items-center justify-between p-3 rounded-[var(--radius-md)] border border-transparent hover:border-[var(--color-border)] hover:bg-[var(--color-bg-subtle)] transition-all cursor-pointer group"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-lg bg-slate-100 flex items-center justify-center group-hover:bg-white transition-colors">
                      <Search className="w-5 h-5 text-slate-400" />
                    </div>
                    <div>
                      <p className="font-semibold text-slate-900">{match.name}</p>
                      <p className="text-sm text-slate-500">Matched with <span className="font-medium text-slate-700">{match.jd}</span></p>
                    </div>
                  </div>
                  <div className="text-right">
                    <Badge variant={match.score >= 80 ? 'success' : 'primary'}>
                      {match.score}% Match
                    </Badge>
                    <p className="text-[10px] uppercase font-bold text-slate-400 mt-1">{match.date}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions / Help */}
        <div className="space-y-6">
          <Card variant="flat" className="bg-indigo-600 text-white border-none shadow-indigo-200">
            <CardTitle className="text-white mb-2">Power User Tip</CardTitle>
            <p className="text-indigo-100 text-sm mb-4">
              Use "Batch Upload" to compare up to 10 candidates against the same job description simultaneously.
            </p>
            <Button variant="outline" size="sm" className="bg-white/10 border-white/20 text-white hover:bg-white/20">
              Learn More
            </Button>
          </Card>
          
          <Card>
            <CardTitle className="text-base mb-4">Quick Links</CardTitle>
            <div className="grid grid-cols-2 gap-3">
              <Link href="/dashboard/jds" className="w-full">
                <Button variant="outline" size="sm" className="justify-start w-full">
                  <Search className="mr-2 w-3 h-3" />
                  Find JDs
                </Button>
              </Link>
              <Link href="/dashboard/jds" className="w-full">
                <Button variant="outline" size="sm" className="justify-start w-full">
                  <Briefcase className="mr-2 w-3 h-3" />
                  Templates
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
