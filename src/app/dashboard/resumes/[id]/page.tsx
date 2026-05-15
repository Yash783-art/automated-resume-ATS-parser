'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Badge } from '@/components/ui/Badge';
import { ScoreRing } from '@/components/ui/ScoreRing';
import { ScoreBar } from '@/components/ui/ScoreBar';
import { SkillTag } from '@/components/ui/SkillTag';
import { 
  Download, 
  Mail, 
  Phone, 
  MapPin, 
  Calendar,
  Briefcase,
  GraduationCap,
  Sparkles,
  ArrowLeft
} from 'lucide-react';
import Link from 'next/link';
import { useApi } from '@/hooks/use-api';

export default function ResumeReportPage() {
  const { id } = useParams();
  // Fetch resume details directly if no specific match exists yet
  const { data: resume, isLoading, isError } = useApi(`/api/resume/${id}/details`);

  const handleExportPDF = () => {
    const matchId = resume?.match_id;
    if (matchId) {
      // Create a temporary link and trigger download to bypass popup blockers
      const link = document.createElement('a');
      link.href = `/api/export/pdf/${matchId}`;
      link.target = '_blank';
      link.download = `Analysis_Report_${id}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const handleContact = () => {
    const email = resume?.parsed_data?.contact?.email;
    const candidateName = resume?.parsed_data?.contact?.name;
    if (email) {
      const subject = encodeURIComponent(`Regarding your application for ${resume.best_job_title || "the position"}`);
      const body = encodeURIComponent(`Hi ${candidateName || "there"},\n\nI reviewed your profile on ATSParser and would like to discuss next steps...`);
      window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
    }
  };

  if (isLoading) return (
    <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
      <div className="w-12 h-12 border-4 border-indigo-200 border-t-indigo-600 rounded-full animate-spin"></div>
      <p className="text-slate-500 font-medium animate-pulse">Analyzing your real data...</p>
    </div>
  );
  
  if (isError || !resume) return (
    <div className="p-8 text-center bg-rose-50 rounded-xl border border-rose-100">
      <h3 className="text-rose-800 font-bold mb-2">Report Not Found</h3>
      <p className="text-rose-600">We couldn't find the data for this resume. Try uploading it again.</p>
      <Link href="/dashboard/resumes">
        <Button variant="outline" className="mt-4 border-rose-200 text-rose-700 hover:bg-rose-100">Go Back</Button>
      </Link>
    </div>
  );

  const activeMatch = {
    overall_score: (resume.overall_score || 0) * (resume.overall_score < 1 ? 100 : 1),
    skills_score: (resume.skills_score || 0) * (resume.skills_score < 1 ? 100 : 1),
    experience_score: (resume.experience_score || 0) * (resume.experience_score < 1 ? 100 : 1),
    education_score: (resume.education_score || 0) * (resume.education_score < 1 ? 100 : 1),
    candidate: {
      name: resume.parsed_data?.contact?.name || "Processing...",
      email: resume.parsed_data?.contact?.email || "N/A",
      phone: resume.parsed_data?.contact?.phone || "N/A",
      location: resume.parsed_data?.contact?.location || "N/A"
    },
    matched_skills: (resume.matched_skills && resume.matched_skills.length > 0) ? resume.matched_skills : (resume.parsed_data?.skills || []),
    missing_skills: resume.missing_skills || [],
    experience: resume.parsed_data?.experience || [],
    profession_mismatch: resume.profession_mismatch || false
  };

  if (isLoading) return <div className="p-8 text-center">Loading Report...</div>;

  return (
    <div className="space-y-8 pb-12">
      {/* Header / Actions */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
        <Link href="/dashboard/resumes">
          <Button variant="ghost" size="sm" className="mb-2">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Resumes
          </Button>
        </Link>
        <div className="flex gap-3">
          <Button variant="outline" size="sm" onClick={handleContact}>
            <Mail className="w-4 h-4 mr-2" />
            Contact Candidate
          </Button>
          <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700" onClick={handleExportPDF}>
            <Download className="w-4 h-4 mr-2" />
            Export PDF
          </Button>
        </div>
      </div>

      {/* Hero Section */}
      <Card variant="flat" className="bg-white overflow-visible">
        <div className="flex flex-col md:flex-row gap-8 items-center p-2">
          {activeMatch.profession_mismatch ? (
            <div className="text-red-500 font-semibold max-w-[160px] text-center">
              ⚠ Profession Mismatch — Candidate domain does not match the job requirement.
            </div>
          ) : (
            <ScoreRing score={activeMatch.overall_score} label="Match Score" size={160} />
          )}
          <div className="flex-1 space-y-4 text-center md:text-left">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">{activeMatch.candidate.name}</h1>
              <p className="text-slate-500 font-medium">Senior Software Engineer Candidate</p>
            </div>
            <div className="flex flex-wrap justify-center md:justify-start gap-4 text-sm text-slate-600">
              <span className="flex items-center gap-1.5"><Mail className="w-4 h-4 text-slate-400" />{activeMatch.candidate.email}</span>
              <span className="flex items-center gap-1.5"><Phone className="w-4 h-4 text-slate-400" />{activeMatch.candidate.phone}</span>
              <span className="flex items-center gap-1.5"><MapPin className="w-4 h-4 text-slate-400" />{activeMatch.candidate.location}</span>
            </div>
            <div className="flex flex-wrap justify-center md:justify-start gap-2 pt-2">
              <Badge variant="success">Available Now</Badge>
              <Badge variant="primary">98% Data Confidence</Badge>
            </div>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Score Breakdown */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Match Breakdown</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <ScoreBar label="Skill Alignment" score={activeMatch.skills_score} />
              <ScoreBar label="Experience Depth" score={activeMatch.experience_score} />
              <ScoreBar label="Education Match" score={activeMatch.education_score} />
              
              <div className="pt-4 border-t border-slate-100">
                <div className="flex gap-4 p-4 bg-amber-50 border border-amber-100 rounded-[var(--radius-md)]">
                  <Sparkles className="w-6 h-6 text-amber-500 shrink-0" />
                  <div>
                    <p className="text-xs font-bold text-amber-900 uppercase tracking-widest mb-1">AI Insight</p>
                    <p className="text-xs text-amber-800 leading-relaxed">
                      Candidate {activeMatch.overall_score >= 70 ? "is a strong match" : "has some potential"} 
                      with {activeMatch.skills_score.toFixed(0)}% skill alignment. 
                      They excel in {activeMatch.matched_skills.slice(0, 3).join(", ") || "their core field"}, 
                      {activeMatch.missing_skills.length > 0 
                        ? ` but could improve on ${activeMatch.missing_skills[0]}.` 
                        : " and meets all key requirements."}
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Analysis Tabs/Sections */}
        <div className="lg:col-span-2 space-y-8">
          {/* Skill Gap Analysis */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Skill Gap Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-widest text-emerald-600 mb-3">
                    {activeMatch.overall_score > 0 ? "Matched Skills" : "Skills Found"}
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {activeMatch.matched_skills.length > 0 
                      ? activeMatch.matched_skills.map((s: string) => <SkillTag key={s} name={s} status="matched" />)
                      : <p className="text-sm text-slate-400 italic">No skills identified yet.</p>
                    }
                  </div>
                </div>
                {activeMatch.overall_score > 0 && activeMatch.missing_skills.length > 0 && (
                  <div>
                    <h4 className="text-xs font-bold uppercase tracking-widest text-rose-600 mb-3">Missing Requirements</h4>
                    <div className="flex flex-wrap gap-2">
                      {activeMatch.missing_skills.map((s: string) => <SkillTag key={s} name={s} status="missing" />)}
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Professional Experience */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Briefcase className="w-5 h-5 text-slate-400" />
                Relevant Experience
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-8 relative before:absolute before:left-[11px] before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-100">
                {activeMatch.experience.map((exp: any, i: number) => (
                  <div key={i} className="relative pl-8">
                    <div className="absolute left-0 top-1.5 w-[24px] h-[24px] bg-white border-2 border-indigo-500 rounded-full flex items-center justify-center">
                      <div className="w-2 h-2 bg-indigo-500 rounded-full" />
                    </div>
                    <div className="flex flex-col md:flex-row md:items-center justify-between mb-2 gap-1">
                      <h4 className="font-bold text-slate-900">{exp.role || exp.text || "Professional Experience"}</h4>
                      <span className="text-xs font-bold text-slate-400 flex items-center uppercase tracking-wider">
                        <Calendar className="w-3 h-3 mr-1" /> {exp.period || "Period N/A"}
                      </span>
                    </div>
                    {exp.company && <p className="text-sm font-medium text-indigo-600 mb-2">{exp.company}</p>}
                    <p className="text-sm text-slate-600 leading-relaxed">{exp.description || (exp.text && !exp.role ? "" : exp.text)}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
