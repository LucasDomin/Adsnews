import { useState } from 'react';
import { 
  LayoutDashboard, 
  Search, 
  TrendingUp, 
  Newspaper, 
  Zap, 
  BarChart3, 
  ArrowUpRight,
  PlusCircle,
  Play
} from 'lucide-react';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { motion } from 'framer-motion';

// Mock Data para demonstração
const MOCK_ADS = [
  {
    id: 1,
    country: 'BR',
    page: 'Fintech Pro',
    headline: 'Dinheiro na mão em 24h',
    cta: 'Saiba Mais',
    score: 88,
    active_days: 12,
    img: 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=500&q=80',
    type: 'Financiamento'
  },
  {
    id: 2,
    country: 'AR',
    page: 'Crédito Ya',
    headline: 'Tu préstamo sin vueltas',
    cta: 'Solicitar',
    score: 92,
    active_days: 30,
    img: 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=500&q=80',
    type: 'Préstamo'
  },
  {
    id: 3,
    country: 'CO',
    page: 'RapiCrédito',
    headline: 'Aprobación inmediata hoje',
    cta: 'Ver Mais',
    score: 75,
    active_days: 5,
    img: 'https://images.unsplash.com/photo-1591033594798-33227a05780d?w=500&q=80',
    type: 'Tarjeta'
  }
];

const App = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="flex h-screen bg-[#0A0A0B] text-slate-200 overflow-hidden font-sans">
      {/* Sidebar Estilo Linear/Stripe */}
      <aside className="w-64 border-r border-white/5 bg-[#0D0D0F] p-6 flex flex-col gap-8">
        <div className="flex items-center gap-2 px-2">
          <div className="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Zap size={20} className="text-white fill-white" />
          </div>
          <span className="font-bold tracking-tight text-white text-lg">LATAM Creative</span>
        </div>

        <nav className="flex flex-col gap-1">
          <NavItem 
            active={activeTab === 'dashboard'} 
            onClick={() => setActiveTab('dashboard')} 
            icon={<LayoutDashboard size={18} />} 
            label="Dashboard" 
          />
          <NavItem 
            active={activeTab === 'feed'} 
            onClick={() => setActiveTab('feed')} 
            icon={<Search size={18} />} 
            label="Ads Feed" 
          />
          <NavItem 
            active={activeTab === 'trends'} 
            onClick={() => setActiveTab('trends')} 
            icon={<TrendingUp size={18} />} 
            label="Trends TikTok" 
          />
          <NavItem 
            active={activeTab === 'news'} 
            onClick={() => setActiveTab('news')} 
            icon={<Newspaper size={18} />} 
            label="News Sentiment" 
          />
          <NavItem 
            active={activeTab === 'patterns'} 
            onClick={() => setActiveTab('patterns')} 
            icon={<BarChart3 size={18} />} 
            label="Winning Patterns" 
          />
        </nav>

        <div className="mt-auto border-t border-white/5 pt-6 flex flex-col gap-4">
          <div className="px-3 py-4 bg-gradient-to-br from-blue-600/10 to-indigo-600/10 rounded-xl border border-blue-500/20">
            <p className="text-xs text-blue-400 font-semibold mb-1 uppercase tracking-wider">AI Generator</p>
            <p className="text-sm text-slate-400 mb-3 leading-snug">Gere hooks e scripts de alta performance.</p>
            <button className="w-full py-2 bg-blue-600 hover:bg-blue-500 transition-colors text-white rounded-lg text-sm font-medium flex items-center justify-center gap-2">
              <PlusCircle size={14} />
              Criar Script
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto overflow-x-hidden relative">
        <header className="h-16 border-b border-white/5 bg-[#0D0D0F]/80 backdrop-blur-md sticky top-0 z-10 flex items-center justify-between px-8">
          <h1 className="text-sm font-medium text-slate-400 uppercase tracking-[0.2em]">
            {activeTab.toUpperCase()}
          </h1>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-white/5 px-3 py-1.5 rounded-full border border-white/10">
              <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs font-medium text-slate-300 tracking-wide">Scraper Ativo</span>
            </div>
            <div className="h-8 w-8 rounded-full bg-indigo-500 border border-white/20" />
          </div>
        </header>

        <div className="p-8">
          {activeTab === 'dashboard' && <DashboardContent />}
          {activeTab === 'feed' && <AdsFeedContent />}
        </div>
      </main>
    </div>
  );
};

const NavItem = ({ icon, label, active, onClick }: { icon: any, label: string, active: boolean, onClick: () => void }) => (
  <button 
    onClick={onClick}
    className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
      active 
        ? 'bg-white/10 text-white shadow-sm shadow-black/5' 
        : 'text-slate-400 hover:text-white hover:bg-white/5'
    }`}
  >
    <span className={active ? 'text-blue-500' : ''}>{icon}</span>
    {label}
  </button>
);

const DashboardContent = () => (
  <motion.div 
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    className="space-y-8"
  >
    {/* Resumo LATAM */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard country="Brasil" sentiment="82%" topic="Crédito Online" />
      <StatCard country="Argentina" sentiment="45%" topic="Microcrédito" />
      <StatCard country="Colômbia" sentiment="68%" topic="Cartão de Crédito" />
    </div>

    {/* Insights Automáticos */}
    <section>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-white">Insights Automáticos</h2>
        <span className="text-xs text-slate-500">Atualizado há 14m</span>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <InsightCard 
          icon={<Zap className="text-amber-400" size={18} />}
          text="Ads azuis com aprovação imediata cresceram 40% no Brasil nos últimos 7 dias."
        />
        <InsightCard 
          icon={<TrendingUp className="text-emerald-400" size={18} />}
          text="Argentina apresenta aumento de ads com urgência extrema (ex: HOY MISMO)."
        />
      </div>
    </section>

    {/* Gráfico de Performance */}
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 bg-[#0D0D0F] border border-white/5 rounded-2xl p-6">
        <h3 className="text-lg font-medium text-white mb-6">Volume de Ads por País</h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={[
              { name: 'Seg', br: 400, ar: 240, co: 240 },
              { name: 'Ter', br: 300, ar: 139, co: 221 },
              { name: 'Qua', br: 200, ar: 980, co: 229 },
              { name: 'Qui', br: 278, ar: 390, co: 200 },
              { name: 'Sex', br: 189, ar: 480, co: 218 },
              { name: 'Sab', br: 239, ar: 380, co: 250 },
              { name: 'Dom', br: 349, ar: 430, co: 210 },
            ]}>
              <defs>
                <linearGradient id="colorBr" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#2563eb" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
              <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }}
                itemStyle={{ color: '#fff' }}
              />
              <Area type="monotone" dataKey="br" stroke="#2563eb" fillOpacity={1} fill="url(#colorBr)" strokeWidth={2} />
              <Area type="monotone" dataKey="ar" stroke="#ef4444" fillOpacity={0} strokeWidth={2} strokeDasharray="5 5" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-[#0D0D0F] border border-white/5 rounded-2xl p-6 flex flex-col justify-between">
        <div>
          <h3 className="text-lg font-medium text-white mb-4">Emoções Dominantes</h3>
          <div className="space-y-4">
            <EmotionBar label="Urgência" value={85} color="bg-red-500" />
            <EmotionBar label="Alívio" value={62} color="bg-emerald-500" />
            <EmotionBar label="Confiança" value={45} color="bg-blue-500" />
            <EmotionBar label="Medo" value={28} color="bg-amber-500" />
          </div>
        </div>
        <div className="mt-6 pt-6 border-t border-white/5 text-center">
          <p className="text-xs text-slate-500 mb-2 underline cursor-pointer">Ver Relatório Completo</p>
        </div>
      </div>
    </div>
  </motion.div>
);

const AdsFeedContent = () => (
  <motion.div 
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    className="space-y-6"
  >
    <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
      <div className="relative w-full md:w-96">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
        <input 
          placeholder="Filtrar por headline, página ou país..." 
          className="w-full bg-[#0D0D0F] border border-white/5 rounded-xl py-2 pl-10 pr-4 text-sm focus:ring-1 focus:ring-blue-500 outline-none"
        />
      </div>
      <div className="flex gap-2 w-full md:w-auto overflow-x-auto pb-2 md:pb-0">
        <FilterButton label="Brasil" />
        <FilterButton label="Argentina" />
        <FilterButton label="Colômbia" />
        <FilterButton label="Vídeo" />
        <FilterButton label="Imagem" />
      </div>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {MOCK_ADS.map(ad => (
        <AdCard key={ad.id} ad={ad} />
      ))}
    </div>
  </motion.div>
);

const StatCard = ({ country, sentiment, topic }: { country: string, sentiment: string, topic: string }) => {
  return (
    <div className="bg-[#0D0D0F] border border-white/5 rounded-2xl p-5 hover:border-white/10 transition-colors">
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-center gap-2">
          <div className={`h-6 w-6 rounded-md flex items-center justify-center bg-white/5 text-[10px] font-bold`}>
            {country.substring(0,2).toUpperCase()}
          </div>
          <span className="text-slate-400 text-sm font-medium">{country}</span>
        </div>
        <ArrowUpRight size={14} className="text-slate-600" />
      </div>
      <div className="flex items-end justify-between">
        <div>
          <p className="text-2xl font-bold text-white tracking-tight">{sentiment}</p>
          <p className="text-xs text-slate-500 font-medium tracking-wide mt-1">SENTIMENTO SOCIAL</p>
        </div>
        <div className="text-right">
          <p className="text-sm font-medium text-slate-300">{topic}</p>
          <p className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">EM ALTA</p>
        </div>
      </div>
    </div>
  );
};

const InsightCard = ({ icon, text }: { icon: any, text: string }) => (
  <div className="bg-[#0D0D0F] border border-white/5 rounded-xl p-4 flex gap-3 items-start group hover:border-white/20 transition-all">
    <div className="mt-1 p-2 bg-white/5 rounded-lg group-hover:scale-110 transition-transform">
      {icon}
    </div>
    <p className="text-sm leading-relaxed text-slate-300 italic">"{text}"</p>
  </div>
);

const EmotionBar = ({ label, value, color }: { label: string, value: number, color: string }) => (
  <div className="space-y-2">
    <div className="flex justify-between text-xs font-medium">
      <span className="text-slate-400">{label}</span>
      <span className="text-white">{value}%</span>
    </div>
    <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
      <motion.div 
        initial={{ width: 0 }}
        animate={{ width: `${value}%` }}
        transition={{ duration: 1, ease: "easeOut" }}
        className={`h-full ${color}`} 
      />
    </div>
  </div>
);

const FilterButton = ({ label }: { label: string }) => (
  <button className="whitespace-nowrap px-4 py-1.5 rounded-full border border-white/5 bg-white/5 text-xs font-medium text-slate-400 hover:text-white hover:border-white/10 transition-all">
    {label}
  </button>
);

const AdCard = ({ ad }: { ad: any }) => (
  <motion.div 
    whileHover={{ y: -4 }}
    className="bg-[#0D0D0F] border border-white/5 rounded-2xl overflow-hidden group shadow-2xl shadow-black/40"
  >
    <div className="aspect-[4/5] relative overflow-hidden bg-slate-900">
      <img src={ad.img} alt={ad.headline} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-90" />
      <div className="absolute top-4 left-4 flex gap-2">
        <span className="bg-black/60 backdrop-blur-md text-white text-[10px] px-2 py-1 rounded-md font-bold uppercase tracking-wider">
          {ad.country}
        </span>
        <span className="bg-blue-600/80 backdrop-blur-md text-white text-[10px] px-2 py-1 rounded-md font-bold uppercase tracking-wider">
          {ad.type}
        </span>
      </div>
      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-60" />
      <button className="absolute bottom-4 right-4 h-10 w-10 bg-white/10 backdrop-blur-xl border border-white/20 rounded-full flex items-center justify-center text-white hover:bg-white hover:text-black transition-all">
        <Play size={16} fill="currentColor" />
      </button>
    </div>
    <div className="p-5 space-y-4">
      <div className="flex justify-between items-start">
        <div className="space-y-1">
          <p className="text-[10px] text-blue-500 font-bold uppercase tracking-[0.2em]">{ad.page}</p>
          <h4 className="text-white font-semibold leading-snug line-clamp-2">{ad.headline}</h4>
        </div>
        <div className="h-10 w-10 flex flex-col items-center justify-center border border-white/5 rounded-lg bg-white/5">
          <span className="text-xs font-bold text-white leading-none">{ad.score}</span>
          <span className="text-[8px] text-slate-500 uppercase font-medium mt-1">Score</span>
        </div>
      </div>
      
      <div className="flex items-center justify-between pt-4 border-t border-white/5">
        <div className="flex items-center gap-1.5">
          <div className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
          <span className="text-[10px] text-slate-400 font-medium">Ativo por {ad.active_days} dias</span>
        </div>
        <button className="text-[11px] font-bold text-white uppercase tracking-widest border-b border-blue-500 pb-0.5 hover:text-blue-400 hover:border-blue-400 transition-all">
          {ad.cta}
        </button>
      </div>
    </div>
  </motion.div>
);

export default App;
