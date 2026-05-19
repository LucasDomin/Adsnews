import { useState, useEffect, useRef } from 'react';
import {
  LayoutDashboard, Search, TrendingUp, Newspaper, Zap, BarChart3,
  ArrowUpRight, PlusCircle, Play, X, AlertTriangle, CheckCircle,
  Code2, FlaskConical, Lightbulb, RefreshCw,
} from 'lucide-react';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const API = (import.meta as any).env?.VITE_API_URL || '';

async function fetchAds() {
  const res = await fetch(`${API}/ads/`);
  if (!res.ok) throw new Error('Erro ao buscar ads');
  const data = await res.json();
  return Array.isArray(data) ? data : data.items ?? data.ads ?? [];
}

async function fetchSummary() {
  const res = await fetch(`${API}/dashboard/summary`);
  if (!res.ok) return null;
  return res.json();
}

async function triggerRefresh() {
  const res = await fetch(`${API}/dashboard/refresh`, { method: 'POST' });
  if (!res.ok) throw new Error('Erro ao iniciar refresh');
  return res.json();
}

async function fetchRefreshStatus() {
  const res = await fetch(`${API}/dashboard/refresh/status`);
  if (!res.ok) return { running: false };
  return res.json();
}

async function fetchAnalyze(ad: any) {
  const res = await fetch(`${API}/ai/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      headline: ad.headline || ad.page_name || '',
      body: ad.body || ad.main_text || '',
      cta: ad.cta || '',
    }),
  });
  if (!res.ok) throw new Error('Erro ao analisar');
  return res.json();
}

const PERSPECTIVE_STYLES: Record<string, { icon: any; color: string; border: string; bg: string }> = {
  'Desenvolvedor Sênior': { icon: Code2, color: 'text-blue-400', border: 'border-blue-500/30', bg: 'bg-blue-500/5' },
  'Analista de Growth': { icon: TrendingUp, color: 'text-emerald-400', border: 'border-emerald-500/30', bg: 'bg-emerald-500/5' },
  'Cientista de Dados': { icon: FlaskConical, color: 'text-purple-400', border: 'border-purple-500/30', bg: 'bg-purple-500/5' },
  'Especialista Criativo': { icon: Lightbulb, color: 'text-amber-400', border: 'border-amber-500/30', bg: 'bg-amber-500/5' },
};

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [ads, setAds] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedAd, setSelectedAd] = useState<any>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [manualText, setManualText] = useState('');
  const [search, setSearch] = useState('');
  const [refreshing, setRefreshing] = useState(false);
  const [refreshMsg, setRefreshMsg] = useState('');
  const pollRef = useRef<any>(null);

  function loadData() {
    setLoading(true);
    Promise.all([fetchAds(), fetchSummary()])
      .then(([adsData, summaryData]) => {
        setAds(adsData);
        setSummary(summaryData);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }

  useEffect(() => { loadData(); }, []);

  async function handleRefresh() {
    setRefreshing(true);
    setRefreshMsg('Iniciando coleta...');
    try {
      await triggerRefresh();
      setRefreshMsg('Pipeline rodando em background...');
      pollRef.current = setInterval(async () => {
        const { running } = await fetchRefreshStatus();
        if (!running) {
          clearInterval(pollRef.current);
          setRefreshing(false);
          setRefreshMsg('Concluído! Atualizando dados...');
          loadData();
          setTimeout(() => setRefreshMsg(''), 3000);
        }
      }, 3000);
    } catch {
      setRefreshMsg('Erro ao iniciar pipeline');
      setRefreshing(false);
      setTimeout(() => setRefreshMsg(''), 3000);
    }
  }

  async function handleSelectAd(ad: any) {
    setSelectedAd(ad);
    setAnalysis(null);
    setAnalyzing(true);
    try {
      const result = await fetchAnalyze(ad);
      setAnalysis(result);
    } catch {
      setAnalysis({ error: 'Backend indisponível' });
    } finally {
      setAnalyzing(false);
    }
  }

  async function handleManualAnalyze() {
    if (!manualText.trim()) return;
    const fakeAd = { ad_id: '__manual__', page_name: 'Análise manual', headline: manualText, body: '', cta: '' };
    handleSelectAd(fakeAd);
    setActiveTab('feed');
  }

  const filteredAds = ads.filter(ad =>
    !search ||
    (ad.page_name || '').toLowerCase().includes(search.toLowerCase()) ||
    (ad.headline || '').toLowerCase().includes(search.toLowerCase()) ||
    (ad.body || ad.main_text || '').toLowerCase().includes(search.toLowerCase())
  );

  const countries = summary?.countries || {};
  const mediaTypes = summary?.media_distribution || ads.reduce((acc: any, a) => {
    const k = a.media_type || 'outro';
    acc[k] = (acc[k] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="flex h-screen bg-[#0A0A0B] text-slate-200 overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/5 bg-[#0D0D0F] p-6 flex flex-col gap-8 shrink-0">
        <div className="flex items-center gap-2 px-2">
          <div className="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Zap size={20} className="text-white fill-white" />
          </div>
          <span className="font-bold tracking-tight text-white text-lg">LATAM Creative</span>
        </div>

        <nav className="flex flex-col gap-1">
          <NavItem active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} icon={<LayoutDashboard size={18} />} label="Dashboard" />
          <NavItem active={activeTab === 'feed'} onClick={() => setActiveTab('feed')} icon={<Search size={18} />} label="Ads Feed" />
          <NavItem active={activeTab === 'trends'} onClick={() => setActiveTab('trends')} icon={<TrendingUp size={18} />} label="Trends TikTok" />
          <NavItem active={activeTab === 'news'} onClick={() => setActiveTab('news')} icon={<Newspaper size={18} />} label="News Sentiment" />
          <NavItem active={activeTab === 'patterns'} onClick={() => setActiveTab('patterns')} icon={<BarChart3 size={18} />} label="Winning Patterns" />
        </nav>

        <div className="mt-auto border-t border-white/5 pt-6 flex flex-col gap-3">
          {/* Refresh button */}
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="w-full py-2.5 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 transition-colors text-sm font-medium flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <RefreshCw size={14} className={refreshing ? 'animate-spin' : ''} />
            {refreshing ? 'Coletando...' : 'Atualizar Biblioteca'}
          </button>
          {refreshMsg && (
            <p className="text-[11px] text-center text-slate-500">{refreshMsg}</p>
          )}

          {/* Quick analyze */}
          <div className="px-3 py-4 bg-gradient-to-br from-blue-600/10 to-indigo-600/10 rounded-xl border border-blue-500/20">
            <p className="text-xs text-blue-400 font-semibold mb-1 uppercase tracking-wider">Análise Rápida</p>
            <p className="text-sm text-slate-400 mb-3 leading-snug">Cole um copy para analisar.</p>
            <input
              value={manualText}
              onChange={e => setManualText(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleManualAnalyze()}
              placeholder="Headline ou body..."
              className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-600 outline-none mb-2 focus:border-blue-500/50"
            />
            <button
              onClick={handleManualAnalyze}
              className="w-full py-2 bg-blue-600 hover:bg-blue-500 transition-colors text-white rounded-lg text-sm font-medium flex items-center justify-center gap-2"
            >
              <PlusCircle size={14} />
              Analisar
            </button>
          </div>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 overflow-y-auto overflow-x-hidden relative">
        <header className="h-16 border-b border-white/5 bg-[#0D0D0F]/80 backdrop-blur-md sticky top-0 z-10 flex items-center justify-between px-8">
          <h1 className="text-sm font-medium text-slate-400 uppercase tracking-[0.2em]">{activeTab.toUpperCase()}</h1>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-white/5 px-3 py-1.5 rounded-full border border-white/10">
              <div className={`h-2 w-2 rounded-full ${loading ? 'bg-amber-500' : 'bg-green-500 animate-pulse'}`} />
              <span className="text-xs font-medium text-slate-300 tracking-wide">
                {loading ? 'Carregando...' : `${ads.length} ads`}
              </span>
            </div>
            <div className="h-8 w-8 rounded-full bg-indigo-500 border border-white/20" />
          </div>
        </header>

        <div className="p-8">
          {activeTab === 'dashboard' && <DashboardContent ads={ads} countries={countries} mediaTypes={mediaTypes} summary={summary} onSelectAd={handleSelectAd} />}
          {activeTab === 'feed' && <AdsFeedContent ads={filteredAds} search={search} onSearch={setSearch} loading={loading} selectedAd={selectedAd} onSelectAd={handleSelectAd} />}
          {(activeTab === 'trends' || activeTab === 'news' || activeTab === 'patterns') && <PlaceholderContent tab={activeTab} />}
        </div>
      </main>

      {/* Analysis Panel */}
      <AnimatePresence>
        {selectedAd && (
          <motion.aside
            initial={{ x: 400, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 400, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="w-96 border-l border-white/5 bg-[#0D0D0F] flex flex-col shrink-0 overflow-y-auto"
          >
            <div className="p-6 border-b border-white/5 flex items-start justify-between">
              <div>
                <p className="text-xs text-slate-500 mb-1">Analisando</p>
                <p className="text-sm font-medium text-white">{selectedAd.page_name || '—'}</p>
              </div>
              <button onClick={() => setSelectedAd(null)} className="p-1.5 rounded-lg hover:bg-white/5 transition-colors text-slate-500 hover:text-white">
                <X size={16} />
              </button>
            </div>

            <div className="p-6 border-b border-white/5">
              <div className="bg-white/5 rounded-xl p-4 space-y-2">
                {selectedAd.headline && <p className="text-sm font-medium text-white">{selectedAd.headline}</p>}
                {(selectedAd.body || selectedAd.main_text) && <p className="text-xs text-slate-400 leading-relaxed">{selectedAd.body || selectedAd.main_text}</p>}
                {selectedAd.cta && <p className="text-xs text-blue-400 font-medium">CTA: {selectedAd.cta}</p>}
              </div>
            </div>

            <div className="p-6 flex-1">
              {analyzing && (
                <div className="flex flex-col items-center justify-center py-12 gap-3">
                  <div className="h-8 w-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
                  <p className="text-xs text-slate-500">Analisando criativo...</p>
                </div>
              )}
              {analysis?.error && (
                <div className="flex items-center gap-3 bg-red-500/10 border border-red-500/20 rounded-xl p-4">
                  <AlertTriangle size={16} className="text-red-400 shrink-0" />
                  <p className="text-sm text-red-400">{analysis.error}</p>
                </div>
              )}
              {analysis && !analysis.error && (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
                  <div className="flex items-center gap-4 bg-white/5 rounded-xl p-4 border border-white/5">
                    <ScoreRing score={analysis.score} />
                    <div>
                      <p className="text-2xl font-bold text-white">{analysis.tier}</p>
                      <p className="text-xs text-slate-500">Score de conversão</p>
                      <p className="text-xs text-slate-600 mt-1">{analysis.score}/100 pts</p>
                    </div>
                  </div>
                  {analysis.perspectives?.map((p: any, i: number) => {
                    const style = PERSPECTIVE_STYLES[p.label] || { icon: CheckCircle, color: 'text-slate-400', border: 'border-white/10', bg: 'bg-white/5' };
                    const Icon = style.icon;
                    return (
                      <div key={i} className={`rounded-xl border ${style.border} ${style.bg} p-4 space-y-3`}>
                        <div className="flex items-center gap-2">
                          <Icon size={15} className={style.color} />
                          <span className={`text-xs font-semibold uppercase tracking-wider ${style.color}`}>{p.label}</span>
                          {p.tier && <span className="ml-auto text-[10px] font-bold uppercase tracking-wider bg-white/10 text-slate-300 px-2 py-0.5 rounded-full">{p.tier}</span>}
                        </div>
                        {p.risks?.length > 0 && (
                          <div className="space-y-1.5">
                            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-medium">Riscos</p>
                            {p.risks.map((r: string, j: number) => <p key={j} className="text-xs text-slate-300 pl-3 border-l border-white/10 leading-relaxed">{r}</p>)}
                          </div>
                        )}
                        {p.suggestions?.length > 0 && (
                          <div className="space-y-1.5">
                            <p className="text-[10px] text-slate-500 uppercase tracking-widest font-medium">{p.label === 'Cientista de Dados' ? 'Breakdown' : 'Sugestões'}</p>
                            {p.suggestions.map((s: string, j: number) => <p key={j} className="text-xs text-slate-300 pl-3 border-l border-white/10 leading-relaxed">{s}</p>)}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </motion.div>
              )}
            </div>
          </motion.aside>
        )}
      </AnimatePresence>
    </div>
  );
};

function ScoreRing({ score }: { score: number }) {
  const r = 28, circ = 2 * Math.PI * r, dash = (score / 100) * circ;
  const color = score >= 60 ? '#10b981' : score >= 30 ? '#f59e0b' : '#ef4444';
  return (
    <svg width="72" height="72" viewBox="0 0 72 72" className="shrink-0">
      <circle cx="36" cy="36" r={r} fill="none" stroke="#1f2937" strokeWidth="6" />
      <circle cx="36" cy="36" r={r} fill="none" stroke={color} strokeWidth="6" strokeDasharray={`${dash} ${circ}`} strokeLinecap="round" transform="rotate(-90 36 36)" />
      <text x="36" y="40" textAnchor="middle" fontSize="14" fontWeight="600" fill={color}>{score}</text>
    </svg>
  );
}

const NavItem = ({ icon, label, active, onClick }: { icon: any; label: string; active: boolean; onClick: () => void }) => (
  <button onClick={onClick} className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${active ? 'bg-white/10 text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'}`}>
    <span className={active ? 'text-blue-500' : ''}>{icon}</span>
    {label}
  </button>
);

function DashboardContent({ ads, countries, mediaTypes, summary, onSelectAd }: any) {
  const topAds = [...ads].sort((a, b) => (b.score || 0) - (a.score || 0)).slice(0, 3);
  const countryList = Object.entries(countries).length > 0
    ? Object.entries(countries).sort((a: any, b: any) => b[1] - a[1]).slice(0, 3)
    : [['BR', 0], ['AR', 0], ['CO', 0]];

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {countryList.map(([c, count]: any) => (
          <div key={c} className="bg-[#0D0D0F] border border-white/5 rounded-2xl p-5 hover:border-white/10 transition-colors">
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center gap-2">
                <div className="h-6 w-6 rounded-md flex items-center justify-center bg-white/5 text-[10px] font-bold">{String(c).substring(0, 2).toUpperCase()}</div>
                <span className="text-slate-400 text-sm font-medium">{c}</span>
              </div>
              <ArrowUpRight size={14} className="text-slate-600" />
            </div>
            <div className="flex items-end justify-between">
              <div>
                <p className="text-2xl font-bold text-white tracking-tight">{count}</p>
                <p className="text-xs text-slate-500 font-medium tracking-wide mt-1">ADS COLETADOS</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-slate-300">{Object.keys(mediaTypes)[0] || 'video'}</p>
                <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">EM ALTA</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {topAds.length > 0 && (
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-white">Top Criativos</h2>
            <span className="text-xs text-slate-500">Por score</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {topAds.map((ad: any, i: number) => <AdCard key={ad.ad_id || i} ad={ad} onClick={() => onSelectAd(ad)} />)}
          </div>
        </section>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-[#0D0D0F] border border-white/5 rounded-2xl p-6">
          <h3 className="text-lg font-medium text-white mb-6">Volume de Ads por País</h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={[
                { name: 'Seg', br: 400, ar: 240, co: 240 }, { name: 'Ter', br: 300, ar: 139, co: 221 },
                { name: 'Qua', br: 200, ar: 980, co: 229 }, { name: 'Qui', br: 278, ar: 390, co: 200 },
                { name: 'Sex', br: 189, ar: 480, co: 218 }, { name: 'Sab', br: 239, ar: 380, co: 250 },
                { name: 'Dom', br: 349, ar: 430, co: 210 },
              ]}>
                <defs>
                  <linearGradient id="colorBr" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563eb" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }} itemStyle={{ color: '#fff' }} />
                <Area type="monotone" dataKey="br" stroke="#2563eb" fillOpacity={1} fill="url(#colorBr)" strokeWidth={2} />
                <Area type="monotone" dataKey="ar" stroke="#ef4444" fillOpacity={0} strokeWidth={2} strokeDasharray="5 5" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-[#0D0D0F] border border-white/5 rounded-2xl p-6">
          <h3 className="text-lg font-medium text-white mb-4">Tipos de Mídia</h3>
          <div className="space-y-4">
            {Object.entries(mediaTypes).slice(0, 5).map(([type, count]: any) => {
              const total = Object.values(mediaTypes).reduce((a: any, b: any) => a + b, 0) as number;
              const pct = Math.round((count / total) * 100);
              return (
                <div key={type} className="space-y-2">
                  <div className="flex justify-between text-xs font-medium">
                    <span className="text-slate-400 capitalize">{type}</span>
                    <span className="text-white">{pct}%</span>
                  </div>
                  <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                    <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }} transition={{ duration: 1, ease: 'easeOut' }} className="h-full bg-blue-500" />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function AdsFeedContent({ ads, search, onSearch, loading, selectedAd, onSelectAd }: any) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
        <div className="relative w-full md:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
          <input value={search} onChange={e => onSearch(e.target.value)} placeholder="Filtrar por headline, página ou país..." className="w-full bg-[#0D0D0F] border border-white/5 rounded-xl py-2 pl-10 pr-4 text-sm focus:ring-1 focus:ring-blue-500 outline-none" />
        </div>
      </div>
      {loading ? (
        <div className="text-slate-500 text-sm">Carregando ads...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {ads.map((ad: any, i: number) => <AdCard key={ad.ad_id || i} ad={ad} onClick={() => onSelectAd(ad)} selected={selectedAd?.ad_id === ad.ad_id} />)}
        </div>
      )}
    </motion.div>
  );
}

function AdCard({ ad, onClick, selected }: { ad: any; onClick: () => void; selected?: boolean }) {
  const score = ad.score ?? null;
  return (
    <motion.div whileHover={{ y: -4 }} onClick={onClick} className={`bg-[#0D0D0F] border rounded-2xl overflow-hidden group shadow-2xl shadow-black/40 cursor-pointer transition-colors ${selected ? 'border-blue-500/50' : 'border-white/5 hover:border-white/10'}`}>
      {ad.image_url ? (
        <div className="aspect-[4/5] relative overflow-hidden bg-slate-900">
          <img src={ad.image_url} alt={ad.headline} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-90" onError={(e: any) => { e.target.style.display = 'none'; }} />
          <div className="absolute top-4 left-4 flex gap-2">
            {ad.country && <span className="bg-black/60 backdrop-blur-md text-white text-[10px] px-2 py-1 rounded-md font-bold uppercase tracking-wider">{ad.country}</span>}
            {ad.media_type && <span className="bg-blue-600/80 backdrop-blur-md text-white text-[10px] px-2 py-1 rounded-md font-bold uppercase tracking-wider">{ad.media_type}</span>}
          </div>
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-60" />
          <button className="absolute bottom-4 right-4 h-10 w-10 bg-white/10 backdrop-blur-xl border border-white/20 rounded-full flex items-center justify-center text-white hover:bg-white hover:text-black transition-all">
            <Play size={16} fill="currentColor" />
          </button>
        </div>
      ) : (
        <div className="h-20 bg-gradient-to-br from-blue-900/20 to-indigo-900/20 flex items-center justify-center">
          <Zap size={20} className="text-blue-500/30" />
        </div>
      )}
      <div className="p-5 space-y-4">
        <div className="flex justify-between items-start">
          <div className="space-y-1 flex-1 mr-3">
            <p className="text-[10px] text-blue-500 font-bold uppercase tracking-[0.2em]">{ad.page_name || '—'}</p>
            <h4 className="text-white font-semibold leading-snug line-clamp-2 text-sm">{ad.headline || 'Sem headline'}</h4>
          </div>
          {score != null && (
            <div className="h-10 w-10 flex flex-col items-center justify-center border border-white/5 rounded-lg bg-white/5 shrink-0">
              <span className="text-xs font-bold text-white leading-none">{Math.round(score)}</span>
              <span className="text-[8px] text-slate-500 uppercase font-medium mt-1">Score</span>
            </div>
          )}
        </div>
        <div className="flex items-center justify-between pt-4 border-t border-white/5">
          <div className="flex items-center gap-1.5">
            <div className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
            <span className="text-[10px] text-slate-400 font-medium">{ad.media_type || 'Coletado'}</span>
          </div>
          {ad.cta && <span className="text-[11px] font-bold text-white uppercase tracking-widest border-b border-blue-500 pb-0.5">{ad.cta}</span>}
        </div>
      </div>
    </motion.div>
  );
}

function PlaceholderContent({ tab }: { tab: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-24 gap-4 text-slate-600">
      <BarChart3 size={40} />
      <p className="text-sm font-medium">
        {tab === 'trends' && 'Trends TikTok — em breve'}
        {tab === 'news' && 'News Sentiment — em breve'}
        {tab === 'patterns' && 'Winning Patterns — em breve'}
      </p>
    </div>
  );
}

export default App;