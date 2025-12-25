"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
    Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
    Area, AreaChart, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer,
    RadialBarChart, RadialBar, Legend,
    LineChart, Line, PieChart, Pie, Cell,
    BarChart, Bar, ScatterChart, Scatter, ZAxis, Treemap,
    ComposedChart, ReferenceLine
} from 'recharts';
import { motion } from "framer-motion"
import {
    Activity, TrendingUp, DollarSign, Hexagon, Calendar,
    Thermometer, Wind, Gauge, Users, Award, AlertCircle, Coffee,
    Box, Truck, Zap, Percent, ShoppingBag, Target,
    RotateCcw, Search, Moon, AlertTriangle
} from "lucide-react"
import MascotStatus from "@/components/ui/mascot-status"
import { Button } from "@/components/ui/button"

// --- Mock Data ---

// TYPE-01: Roast Profile
const ROAST_PROFILE_DATA = [
    { time: '0:00', bt: 200, et: 200, ror: 0 },
    { time: '1:00', bt: 195, et: 210, ror: -5 },
    { time: '2:00', bt: 205, et: 240, ror: 10 },
    { time: '3:00', bt: 230, et: 280, ror: 15 },
    { time: '4:00', bt: 260, et: 310, ror: 18 },
    { time: '5:00', bt: 295, et: 340, ror: 20 },
    { time: '6:00', bt: 330, et: 365, ror: 15 },
    { time: '7:00', bt: 360, et: 385, ror: 12 },
    { time: '8:00', bt: 385, et: 400, ror: 8 },
    { time: '9:00', bt: 405, et: 410, ror: 5 },
    { time: '10:00', bt: 415, et: 415, ror: 3 },
];

// TYPE-04: Flavor Radar
const FLAVOR_DATA = [
    { subject: 'Body', A: 120, B: 110, fullMark: 150 },
    { subject: 'Acidity', A: 98, B: 130, fullMark: 150 },
    { subject: 'Sweetness', A: 86, B: 130, fullMark: 150 },
    { subject: 'Bitterness', A: 99, B: 100, fullMark: 150 },
    { subject: 'Aroma', A: 85, B: 90, fullMark: 150 },
    { subject: 'Aftertaste', A: 65, B: 85, fullMark: 150 },
];

// TYPE-07: Financial Area
const FINANCIAL_DATA = [
    { month: 'Jan', revenue: 4000, cost: 2400 },
    { month: 'Feb', revenue: 3000, cost: 1398 },
    { month: 'Mar', revenue: 2000, cost: 9800 },
    { month: 'Apr', revenue: 2780, cost: 3908 },
    { month: 'May', revenue: 1890, cost: 4800 },
    { month: 'Jul', revenue: 3490, cost: 4300 },
];

// TYPE-06: Sales Pie
const SALES_CATEGORY_DATA = [
    { name: 'Single Origin', value: 400 },
    { name: 'Blends', value: 300 },
    { name: 'Drip Bags', value: 300 },
    { name: 'Accessories', value: 200 },
];
const COLORS = ['#8D7B68', '#C8AA77', '#E6D5C3', '#A4907C', '#EF4444', '#10B981'];

// TYPE-05: QC Scatter
const QC_SCATTER_DATA = [
    { x: 100, y: 200, z: 200 },
    { x: 120, y: 100, z: 260 },
    { x: 170, y: 300, z: 400 },
    { x: 140, y: 250, z: 280 },
    { x: 150, y: 400, z: 500 },
    { x: 110, y: 280, z: 200 },
];

// TYPE-10: Funnel (Bar)
const FUNNEL_DATA = [
    { name: 'Page Views', value: 5000, fill: '#8D7B68' },
    { name: 'Add to Cart', value: 1200, fill: '#C8AA77' },
    { name: 'Checkout', value: 800, fill: '#D7BF9D' },
    { name: 'Purchase', value: 550, fill: '#E6D5C3' },
];

// TYPE-11: Customer Bubble
const CUSTOMER_BUBBLE_DATA = [
    { x: 10, y: 300, z: 200, name: 'Newbies' },
    { x: 40, y: 500, z: 800, name: 'Loyalists' },
    { x: 80, y: 100, z: 100, name: 'Slipping' },
    { x: 20, y: 800, z: 500, name: 'Whales' },
    { x: 50, y: 400, z: 300, name: 'Regulars' },
];

// TYPE-12: Inventory Treemap
const TREEMAP_DATA = [
    {
        name: 'Green Beans',
        children: [
            { name: 'Ethiopia', size: 2000 },
            { name: 'Colombia', size: 1500 },
            { name: 'Brazil', size: 3000 },
        ],
    },
    {
        name: 'Roasted',
        children: [
            { name: 'House Blend', size: 1000 },
            { name: 'Espresso', size: 800 },
        ],
    },
];

// TYPE-13: Bullet Chart (Target vs Actual)
const BULLET_DATA = [
    { name: 'Roasting', target: 5000, actual: 4200 },
    { name: 'Sales', target: 8000, actual: 8500 },
    { name: 'New Cust.', target: 100, actual: 85 },
];

// TYPE-14: Warehouse Stacked
const WAREHOUSE_DATA = [
    { name: 'WH-A', Green: 4000, Roasted: 2400, Packaging: 2400 },
    { name: 'WH-B', Green: 3000, Roasted: 1398, Packaging: 2210 },
    { name: 'Store', Green: 2000, Roasted: 9800, Packaging: 2290 },
];

// TYPE-15: Profit/Margin
const PROFIT_DATA = [
    { name: 'Mon', revenue: 4000, profit: 2400, margin: 60 },
    { name: 'Tue', revenue: 3000, profit: 1398, margin: 46 },
    { name: 'Wed', revenue: 2000, profit: 9800, margin: -20 }, // Loss example
    { name: 'Thu', revenue: 2780, profit: 3908, margin: 80 },
    { name: 'Fri', revenue: 1890, profit: 4800, margin: 80 },
];

// TYPE-18: Daily P&L
const PNL_DATA = [
    { name: 'Mon', uv: 4000, pv: 2400, amt: 2400 },
    { name: 'Tue', uv: -3000, pv: 1398, amt: 2210 },
    { name: 'Wed', uv: -2000, pv: -9800, amt: 2290 },
    { name: 'Thu', uv: 2780, pv: 3908, amt: 2000 },
    { name: 'Fri', uv: 1890, pv: 4800, amt: 2181 },
];

// TYPE-19: Schedule (Gantt Mock)
const SCHEDULE_DATA = [
    { machine: 'Loring S15', task: 'Ethiopia Washed', start: 9, end: 11, color: 'bg-amber-200' },
    { machine: 'Loring S15', task: 'Maintenance', start: 11, end: 12, color: 'bg-red-100' },
    { machine: 'Loring S15', task: 'Brazil Natural', start: 13, end: 17, color: 'bg-amber-400' },
    { machine: 'Probat P12', task: 'House Blend', start: 9, end: 15, color: 'bg-latte-300' },
];

// Heatmap Mock
const HEATMAP_DATA = Array.from({ length: 364 }, (_, i) => ({
    date: new Date(2025, 0, 1 + i),
    count: Math.random() > 0.7 ? Math.floor(Math.random() * 5) : 0
}));


// Helper for headers
const TypeBadge = ({ type, title }: { type: string, title: string }) => (
    <div className="flex justify-between items-start mb-4">
        <h3 className="font-bold text-latte-800 flex items-center gap-2">
            {title}
        </h3>
        <span className="bg-latte-100 text-latte-600 text-[10px] px-2 py-0.5 rounded font-mono font-bold">{type}</span>
    </div>
)

export default function DashboardDemoPage() {
    return (
        <div className="min-h-screen bg-[#F8F5F2] p-8 font-sans text-latte-900">

            {/* Header */}
            <div className="max-w-[1800px] mx-auto mb-10">
                <h1 className="text-4xl font-serif font-bold text-latte-900 mb-2">Dashboard Gallery (Massive)</h1>
                <p className="text-latte-500 text-lg">20+ Visualization Types for comprehensive roastery management.</p>
            </div>

            <div className="max-w-[1800px] mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-6">

                {/* --- ROW 1: Operations Real-time --- */}

                {/* TYPE-01: Live Roast Profile */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="col-span-1 md:col-span-2 lg:col-span-4 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-01" title="Live Roast Profile (Complex Line)" />
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={ROAST_PROFILE_DATA}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="time" stroke="#9CA3AF" />
                                <YAxis yAxisId="left" stroke="#EF4444" domain={[0, 500]} />
                                <YAxis yAxisId="right" orientation="right" stroke="#3B82F6" domain={[-20, 30]} />
                                <Tooltip />
                                <Legend />
                                <Line yAxisId="left" type="monotone" dataKey="bt" stroke="#EF4444" strokeWidth={3} name="Bean Temp" dot={false} />
                                <Line yAxisId="left" type="monotone" dataKey="et" stroke="#F59E0B" strokeWidth={2} name="Env Temp" dot={false} />
                                <Line yAxisId="right" type="monotone" dataKey="ror" stroke="#3B82F6" strokeWidth={2} name="RoR" dot={false} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>

                {/* TYPE-02: Airflow Gauge */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="col-span-1 bg-white rounded-2xl border border-latte-200 shadow-sm p-6 flex flex-col items-center justify-center relative">
                    <div className="absolute top-4 right-4"><span className="text-[10px] font-mono bg-latte-100 px-1 rounded">TYPE-02</span></div>
                    <Wind className="w-8 h-8 text-latte-400 mb-2" />
                    <div className="text-2xl font-bold">75%</div>
                    <div className="text-xs text-latte-400">Airflow</div>
                    <svg className="w-24 h-24 transform -rotate-90 mt-2">
                        <circle cx="48" cy="48" r="40" stroke="#f3f4f6" strokeWidth="8" fill="none" />
                        <circle cx="48" cy="48" r="40" stroke="#3B82F6" strokeWidth="8" fill="none" strokeDasharray="251" strokeDashoffset="60" />
                    </svg>
                </motion.div>

                {/* TYPE-03: Drum Speed */}
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="col-span-1 bg-white rounded-2xl border border-latte-200 shadow-sm p-6 flex flex-col items-center justify-center relative">
                    <div className="absolute top-4 right-4"><span className="text-[10px] font-mono bg-latte-100 px-1 rounded">TYPE-03</span></div>
                    <Gauge className="w-8 h-8 text-latte-400 mb-2" />
                    <div className="text-2xl font-bold">52 RPM</div>
                    <div className="text-xs text-latte-400">Drum Speed</div>
                    <svg className="w-24 h-24 transform -rotate-90 mt-2">
                        <circle cx="48" cy="48" r="40" stroke="#f3f4f6" strokeWidth="8" fill="none" />
                        <circle cx="48" cy="48" r="40" stroke="#F59E0B" strokeWidth="8" fill="none" strokeDasharray="251" strokeDashoffset="100" />
                    </svg>
                </motion.div>


                {/* --- ROW 2: Quality & Analysis --- */}

                {/* TYPE-04: Sensory Radar */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-04" title="Sensory Analysis (Radar)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <RadarChart cx="50%" cy="50%" outerRadius="70%" data={FLAVOR_DATA}>
                                <PolarGrid />
                                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10 }} />
                                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                                <Radar name="A" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                                <Radar name="B" dataKey="B" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                                <Legend />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* TYPE-05: QC Scatter */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-05" title="QC Correlation (Scatter)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                                <CartesianGrid />
                                <XAxis type="number" dataKey="x" name="Time" unit="s" />
                                <YAxis type="number" dataKey="y" name="Score" unit="pts" />
                                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                                <Scatter name="Batches" data={QC_SCATTER_DATA} fill="#8884d8" />
                            </ScatterChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* TYPE-20: Flavor Word Cloud (Mock) */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6 flex flex-col">
                    <TypeBadge type="TYPE-20" title="Flavor Word Cloud (Mock)" />
                    <div className="flex-1 flex flex-wrap gap-2 content-center items-center justify-center p-4">
                        {['Chocolate', 'Berry', 'Citrus', 'Nutty', 'Floral', 'Spicy', 'Caramel', 'Stone Fruit', 'Jasmine', 'Honey'].map((word, i) => (
                            <span key={i} className="px-3 py-1 rounded-full bg-latte-100 text-latte-800" style={{ fontSize: `${Math.max(0.8, Math.random() * 2)}rem`, opacity: Math.max(0.4, Math.random() + 0.2) }}>
                                {word}
                            </span>
                        ))}
                    </div>
                </div>


                {/* --- ROW 3: Sales & KPI --- */}

                {/* TYPE-06: Sales Pie */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-06" title="Sales Distribution (Pie)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie data={SALES_CATEGORY_DATA} cx="50%" cy="50%" outerRadius={80} fill="#8884d8" dataKey="value" label>
                                    {SALES_CATEGORY_DATA.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* TYPE-10: Funnel */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-10" title="Conversion Funnel (Bar)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart layout="vertical" data={FUNNEL_DATA} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
                                <XAxis type="number" hide />
                                <YAxis dataKey="name" type="category" width={80} />
                                <Tooltip />
                                <Bar dataKey="value" barSize={20} radius={[0, 4, 4, 0]}>
                                    {FUNNEL_DATA.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.fill} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* TYPE-11: Customer Bubble */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-11" title="Customer Segmentation (Bubble)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                                <CartesianGrid />
                                <XAxis type="number" dataKey="x" name="Recency" />
                                <YAxis type="number" dataKey="y" name="Frequency" />
                                <ZAxis type="number" dataKey="z" range={[50, 400]} name="LTV" />
                                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                                <Scatter name="Customers" data={CUSTOMER_BUBBLE_DATA} fill="#FF8042" />
                            </ScatterChart>
                        </ResponsiveContainer>
                    </div>
                </div>


                {/* --- ROW 4: Supply Chain --- */}

                {/* TYPE-12: Inventory Treemap */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-12" title="Inventory Value (Treemap)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <Treemap data={TREEMAP_DATA} dataKey="size" aspectRatio={4 / 3} stroke="#fff" fill="#8884d8" />
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* TYPE-14: Warehouse Stacked */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-14" title="Warehouse Capacity (Stacked)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={WAREHOUSE_DATA}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="Green" stackId="a" fill="#8884d8" />
                                <Bar dataKey="Roasted" stackId="a" fill="#82ca9d" />
                                <Bar dataKey="Packaging" stackId="a" fill="#ffc658" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* TYPE-17: Equipment Health Core */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6 flex flex-wrap justify-around items-center">
                    <TypeBadge type="TYPE-17" title="Equipment Health (Radial)" />
                    <div className="flex gap-4">
                        {[78, 92, 45].map((val, i) => (
                            <div key={i} className="relative w-24 h-24 flex items-center justify-center">
                                <svg className="w-full h-full transform -rotate-90">
                                    <circle cx="48" cy="48" r="36" stroke="#f3f4f6" strokeWidth="8" fill="none" />
                                    <circle cx="48" cy="48" r="36" stroke={val > 80 ? "#10B981" : val > 50 ? "#F59E0B" : "#EF4444"} strokeWidth="8" fill="none" strokeDasharray="226" strokeDashoffset={226 - (226 * val) / 100} />
                                </svg>
                                <div className="absolute font-bold">{val}%</div>
                            </div>
                        ))}
                    </div>
                    <div className="w-full text-center text-xs text-latte-400 mt-2">Filter • Afterburner • Chiller</div>
                </div>


                {/* --- ROW 5: Business Financials --- */}

                {/* TYPE-07: Financial Trends */}
                <div className="col-span-1 md:col-span-2 lg:col-span-3 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-07" title="Financial Trends (Area Gradient)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={FINANCIAL_DATA}>
                                <defs>
                                    <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#10B981" stopOpacity={0.8} />
                                        <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="month" />
                                <YAxis />
                                <Tooltip />
                                <Area type="monotone" dataKey="revenue" stroke="#10B981" fill="url(#colorRevenue)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* TYPE-15: Profit/Margin */}
                <div className="col-span-1 md:col-span-2 lg:col-span-3 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-15" title="Profit Margin (Composed)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <ComposedChart data={PROFIT_DATA}>
                                <CartesianGrid stroke="#f5f5f5" />
                                <XAxis dataKey="name" scale="band" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="revenue" barSize={20} fill="#413ea0" />
                                <Line type="monotone" dataKey="margin" stroke="#ff7300" />
                            </ComposedChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* TYPE-18: Daily P&L */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-18" title="Daily P&L (Pos/Neg)" />
                    <div className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={PNL_DATA}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <ReferenceLine y={0} stroke="#000" />
                                <Bar dataKey="uv" fill="#8884d8">
                                    {PNL_DATA.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.uv > 0 ? '#10B981' : '#EF4444'} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* TYPE-13: Bullet KPI */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6 flex flex-col gap-4">
                    <TypeBadge type="TYPE-13" title="KPI Targets (Bullet)" />
                    {BULLET_DATA.map((kpi, i) => (
                        <div key={i} className="mb-2">
                            <div className="flex justify-between text-sm mb-1">
                                <span>{kpi.name}</span>
                                <span>{Math.round((kpi.actual / kpi.target) * 100)}%</span>
                            </div>
                            <div className="h-4 bg-latte-100 rounded-full overflow-hidden relative">
                                <div className="absolute top-0 bottom-0 bg-latte-300 w-3/4"></div> {/* Target marker area */}
                                <div className="absolute top-0 bottom-0 bg-amber-500 rounded-full" style={{ width: `${Math.min(100, (kpi.actual / kpi.target) * 100)}%` }}></div>
                                <div className="absolute top-0 bottom-0 w-1 bg-black z-10" style={{ left: '75%' }}></div> {/* Target line */}
                            </div>
                        </div>
                    ))}
                </div>


                {/* --- ROW 6: Schedule & Activity --- */}

                {/* TYPE-19: Schedule Gantt */}
                <div className="col-span-1 md:col-span-2 lg:col-span-4 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-19" title="Roaster Schedule (Gantt)" />
                    <div className="relative h-[200px] bg-latte-50 rounded-lg p-4 overflow-hidden">
                        {/* Time ruler */}
                        <div className="flex justify-between text-xs text-latte-400 mb-2">
                            {[9, 10, 11, 12, 13, 14, 15, 16, 17].map(h => <span key={h}>{h}:00</span>)}
                        </div>
                        {/* Tasks */}
                        <div className="space-y-4">
                            {/* Machine 1 Row */}
                            <div className="flex items-center gap-4">
                                <div className="w-20 text-sm font-bold">Loring</div>
                                <div className="flex-1 h-8 bg-white relative rounded">
                                    {SCHEDULE_DATA.filter(t => t.machine === 'Loring S15').map((task, i) => (
                                        <div key={i} className={`absolute top-1 bottom-1 ${task.color} rounded text-[10px] flex items-center px-2 truncate`}
                                            style={{ left: `${(task.start - 9) * 12.5}%`, width: `${(task.end - task.start) * 12.5}%` }}>
                                            {task.task}
                                        </div>
                                    ))}
                                </div>
                            </div>
                            {/* Machine 2 Row */}
                            <div className="flex items-center gap-4">
                                <div className="w-20 text-sm font-bold">Probat</div>
                                <div className="flex-1 h-8 bg-white relative rounded">
                                    {SCHEDULE_DATA.filter(t => t.machine === 'Probat P12').map((task, i) => (
                                        <div key={i} className={`absolute top-1 bottom-1 ${task.color} rounded text-[10px] flex items-center px-2 truncate`}
                                            style={{ left: `${(task.start - 9) * 12.5}%`, width: `${(task.end - task.start) * 12.5}%` }}>
                                            {task.task}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* TYPE-09: Activity Heatmap */}
                <div className="col-span-1 md:col-span-2 lg:col-span-6 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-09" title="Annual Activity (Heatmap)" />
                    <div className="flex flex-wrap gap-1 justify-center">
                        {HEATMAP_DATA.slice(0, 180).map((day, i) => (
                            <div
                                key={i}
                                className={`
                        w-3 h-3 rounded-sm transition-all hover:scale-125
                        ${day.count === 0 ? 'bg-latte-100' : ''}
                        ${day.count === 1 ? 'bg-amber-200' : ''}
                        ${day.count === 2 ? 'bg-amber-300' : ''}
                        ${day.count >= 3 ? 'bg-amber-500' : ''}
                        `}
                                title={day.date.toLocaleDateString()}
                            />
                        ))}
                    </div>
                </div>

                {/* TYPE-16: Sparkline Grid (Tiny) */}
                <div className="col-span-1 md:col-span-2 bg-white/80 rounded-2xl border border-latte-200 shadow-sm p-6">
                    <TypeBadge type="TYPE-16" title="Sparkline Snapshots" />
                    <div className="grid grid-cols-2 gap-4">
                        {[1, 2, 3, 4].map(i => (
                            <div key={i} className="p-2 bg-latte-50 rounded">
                                <div className="text-xs text-latte-400">Metric {i}</div>
                                <div className="h-10">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <LineChart data={ROAST_PROFILE_DATA}>
                                            <Line type="monotone" dataKey="bt" stroke="#8884d8" strokeWidth={2} dot={false} />
                                        </LineChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>


                {/* --- ROW 7: Card Style Variants (User Request) --- */}

                {/* TYPE-21: Glassmorphism */}
                <div className="col-span-1 bg-white/30 backdrop-blur-md border border-white/50 shadow-lg rounded-2xl p-6 relative overflow-hidden">
                    <span className="absolute top-4 right-4 text-[10px] font-mono font-bold text-latte-900/50">TYPE-21</span>
                    <h3 className="text-latte-900 font-bold mb-1">Glassmorphism</h3>
                    <p className="text-xs text-latte-700 mb-4">Frosted glass effect for specialized overlays.</p>
                    <div className="flex items-end gap-2 text-latte-900">
                        <span className="text-3xl font-bold">2,405</span>
                        <span className="text-sm mb-1">Visitors</span>
                    </div>
                </div>

                {/* TYPE-22: Vivid Gradient */}
                <div className="col-span-1 bg-gradient-to-br from-amber-400 to-orange-600 text-white shadow-lg rounded-2xl p-6 relative">
                    <span className="absolute top-4 right-4 text-[10px] font-mono font-bold text-white/50">TYPE-22</span>
                    <h3 className="font-bold mb-1 text-white">Vivid Gradient</h3>
                    <p className="text-xs text-white/80 mb-4">High emphasis for critical Alerts or Heroes.</p>
                    <div className="flex items-center gap-2">
                        <AlertCircle className="w-8 h-8 opacity-80" />
                        <span className="text-2xl font-bold">Action Req.</span>
                    </div>
                </div>

                {/* TYPE-23: Border Accent */}
                <div className="col-span-1 bg-white border-l-4 border-l-green-500 shadow-sm rounded-r-xl p-6 relative">
                    <span className="absolute top-4 right-4 text-[10px] font-mono font-bold text-latte-300">TYPE-23</span>
                    <h3 className="text-latte-500 font-medium text-sm">Total Revenue</h3>
                    <div className="mt-2 flex items-baseline gap-2">
                        <span className="text-3xl font-bold text-latte-900">$45.2k</span>
                        <span className="text-xs text-green-600 font-bold flex items-center"><TrendingUp className="w-3 h-3" /> +12%</span>
                    </div>
                </div>

                {/* TYPE-24: Dark Theme */}
                <div className="col-span-1 bg-latte-900 text-latte-50 shadow-xl rounded-2xl p-6 relative">
                    <span className="absolute top-4 right-4 text-[10px] font-mono font-bold text-latte-700">TYPE-24</span>
                    <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 bg-latte-800 rounded-lg"><Coffee className="w-5 h-5 text-amber-400" /></div>
                        <div>
                            <h3 className="font-bold">Dark Mode</h3>
                            <p className="text-xs text-latte-400">Night shift optimized</p>
                        </div>
                    </div>
                    <div className="w-full bg-latte-800 h-1.5 rounded-full overflow-hidden">
                        <div className="bg-amber-400 w-2/3 h-full rounded-full shadow-[0_0_10px_rgba(251,191,36,0.5)]"></div>
                    </div>
                </div>

                {/* TYPE-25: Neumorphic (Soft) */}
                <div className="col-span-1 bg-[#F0EFEC] shadow-[8px_8px_16px_#d1cfcc,-8px_-8px_16px_#ffffff] rounded-2xl p-6 relative">
                    <span className="absolute top-4 right-4 text-[10px] font-mono font-bold text-latte-400">TYPE-25</span>
                    <h3 className="text-latte-600 font-bold mb-2">Neumorphic</h3>
                    <p className="text-xs text-latte-400 mb-4">Soft shadows, tactile feel.</p>
                    <button className="w-full py-2 rounded-xl bg-[#F0EFEC] shadow-[5px_5px_10px_#d1cfcc,-5px_-5px_10px_#ffffff] text-xs font-bold text-latte-600 active:shadow-[inset_5px_5px_10px_#d1cfcc,inset_-5px_-5px_10px_#ffffff] transition-all">
                        Press Me
                    </button>
                </div>

                {/* TYPE-26: Mesh/Image Bg */}
                <div className="col-span-1 relative rounded-2xl p-6 overflow-hidden text-white shadow-md">
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-700 z-0"></div>
                    <div className="absolute inset-0 opacity-30 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] z-0 mix-blend-overlay"></div>
                    <span className="absolute top-4 right-4 text-[10px] font-mono font-bold text-white/50 z-10">TYPE-26</span>

                    <div className="relative z-10">
                        <h3 className="font-bold text-lg mb-1">Mesh/Pattern</h3>
                        <p className="text-xs text-indigo-100 opacity-80">Texture & Depth</p>
                        <div className="mt-6 flex justify-between items-end">
                            <div className="text-3xl font-bold">89</div>
                            <Activity className="w-6 h-6 opacity-50" />
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}
