import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { 
  Zap, 
  Shield, 
  Search, 
  ArrowRight, 
  CheckCircle2,
  Cpu,
  BarChart4,
  Layers
} from 'lucide-react';
import Navbar from '@/components/layout/Navbar';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="container mx-auto px-6 text-center">
          <Badge variant="primary" className="mb-6 animate-in fade-in slide-in-from-bottom-3 duration-700">
            Next-Gen AI Parser
          </Badge>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-slate-900 mb-8 max-w-4xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-800">
            Stop Guessing. <br />
            <span className="text-[var(--color-primary)]">Optimize Your Career</span> with AI.
          </h1>
          <p className="text-lg md:text-xl text-slate-600 mb-10 max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-5 duration-900">
            Our state-of-the-art ATS parser uses semantic intelligence to match your resume against job descriptions with 98% accuracy.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-in fade-in slide-in-from-bottom-6 duration-1000">
            <Link href="/dashboard/upload">
              <Button size="lg" className="h-14 px-8 text-lg group">
                Get Started Free
                <ArrowRight className="ml-2 w-5 h-5 transition-transform group-hover:translate-x-1" />
              </Button>
            </Link>
            <Link href="#features">
              <Button variant="outline" size="lg" className="h-14 px-8 text-lg">
                View Demo
              </Button>
            </Link>
          </div>
          
          {/* Abstract Background Elements */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 -z-10 w-full max-w-5xl opacity-20 blur-3xl">
            <div className="aspect-square bg-gradient-to-tr from-indigo-500 to-purple-500 rounded-full animate-pulse" />
          </div>
        </div>
      </section>

      {/* Bento Feature Grid */}
      <section id="features" className="py-24 bg-slate-50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">Precision-Engineered Features</h2>
            <p className="text-slate-600 max-w-xl mx-auto text-lg">
              Everything you need to beat the ATS and get your resume seen by human recruiters.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card variant="elevated" className="md:col-span-2">
              <div className="flex flex-col h-full">
                <div className="p-3 bg-indigo-50 w-fit rounded-lg mb-6">
                  <Cpu className="w-6 h-6 text-indigo-600" />
                </div>
                <h3 className="text-2xl font-bold mb-4">Semantic NER Extraction</h3>
                <p className="text-slate-600 text-lg mb-8">
                  Our Named Entity Recognition (NER) models don't just find keywords; they understand the context of your achievements, skills, and experience.
                </p>
                <div className="mt-auto pt-4 border-t border-slate-100 flex gap-4 overflow-hidden whitespace-nowrap opacity-50">
                  <Badge>Python</Badge>
                  <Badge>React</Badge>
                  <Badge>Docker</Badge>
                  <Badge>NLP</Badge>
                  <Badge>AWS</Badge>
                </div>
              </div>
            </Card>
            
            <Card variant="elevated">
              <div className="p-3 bg-emerald-50 w-fit rounded-lg mb-6">
                <Shield className="w-6 h-6 text-emerald-600" />
              </div>
              <h3 className="text-xl font-bold mb-4">Privacy First</h3>
              <p className="text-slate-600">
                Encrypted storage with Cloudflare R2 and automatic 30-day data purging. Your career data belongs to you.
              </p>
            </Card>
            
            <Card variant="elevated">
              <div className="p-3 bg-amber-50 w-fit rounded-lg mb-6">
                <Search className="w-6 h-6 text-amber-600" />
              </div>
              <h3 className="text-xl font-bold mb-4">OCR Fallback</h3>
              <p className="text-slate-600">
                Scanned PDF? No problem. Our Tesseract 5 pipeline ensures no data is left behind, regardless of format.
              </p>
            </Card>
            
            <Card variant="elevated" className="md:col-span-2">
              <div className="flex flex-col md:flex-row gap-8 items-center h-full">
                <div className="flex-1">
                  <div className="p-3 bg-purple-50 w-fit rounded-lg mb-6">
                    <BarChart4 className="w-6 h-6 text-purple-600" />
                  </div>
                  <h3 className="text-2xl font-bold mb-4">Match Analytics</h3>
                  <p className="text-slate-600 text-lg">
                    Get detailed score breakdowns by skill alignment, experience depth, and education relevance.
                  </p>
                </div>
                <div className="flex-1 flex justify-center">
                  <div className="w-32 h-32 rounded-full border-8 border-indigo-500 border-t-transparent animate-spin duration-1000 flex items-center justify-center">
                    <span className="text-2xl font-bold animate-none -rotate-45">85%</span>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="py-20 bg-white border-y border-slate-100">
        <div className="container mx-auto px-6 text-center">
          <p className="text-sm uppercase tracking-widest text-slate-400 font-bold mb-10">Optimized For Modern ATS Platforms</p>
          <div className="flex flex-wrap justify-center gap-12 opacity-30 grayscale">
            <span className="text-2xl font-bold italic">Workday</span>
            <span className="text-2xl font-bold italic">Greenhouse</span>
            <span className="text-2xl font-bold italic">Lever</span>
            <span className="text-2xl font-bold italic">BambooHR</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-white text-slate-500 border-t border-slate-100">
        <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-2">
            <span className="text-xl font-bold text-slate-900">
              ATS<span className="text-[var(--color-primary)]">Parser</span>
            </span>
          </div>
          <div className="flex gap-8 text-sm">
            <Link href="#" className="hover:text-slate-900">Terms</Link>
            <Link href="#" className="hover:text-slate-900">Privacy</Link>
            <Link href="#" className="hover:text-slate-900">Support</Link>
          </div>
          <p className="text-sm">© 2026 ATS Parser. Powered by DeepMind.</p>
        </div>
      </footer>
    </div>
  );
}
