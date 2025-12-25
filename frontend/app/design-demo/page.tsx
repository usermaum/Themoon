'use client';

import { useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import {
  Coffee,
  Palette,
  Package,
  AlertTriangle,
  TrendingUp,
  Users,
  Calendar,
  CheckCircle2,
  XCircle,
  Info,
  Sparkles,
  Moon,
  Sun,
  Heart,
  Star,
  Zap,
  Award,
  Target,
  Filter,
  Search,
  Settings,
  Bell,
  BarChart3,
  PieChart,
  Activity,
  Layout,
  MousePointerClick,
  Tag,
  SquareStack,
  LayoutDashboard,
  BookOpen,
  Map,
  Utensils,
  CalendarDays,
  PackageCheck,
  ScrollText,
  LockKeyhole,
  ArrowRight,
} from 'lucide-react';

// --- Data from Design Sample ---
const components = [
  {
    title: 'Card',
    desc: 'Product displays, menu items, and rich content containers.',
    href: '/design-sample/card',
    icon: Layout,
    preview: 'Latte, Espresso, Paper Menu Styles',
    color: 'text-amber-700 bg-amber-50',
  },
  {
    title: 'Button',
    desc: 'Interactive elements for actions, navigation, and triggers.',
    href: '/design-sample/button',
    icon: MousePointerClick,
    preview: 'Primary, Secondary, Icon Buttons',
    color: 'text-blue-700 bg-blue-50',
  },
  {
    title: 'Badge',
    desc: 'Status indicators, labels, and categorization tags.',
    href: '/design-sample/badge',
    icon: Tag,
    preview: 'Roast Level, Flavors, Stock Status',
    color: 'text-green-700 bg-green-50',
  },
  {
    title: 'Tabs',
    desc: 'Content organization and switching between different views.',
    href: '/design-sample/tabs',
    icon: SquareStack,
    preview: 'Menu Categories, Subscriptions',
    color: 'text-purple-700 bg-purple-50',
  },
  {
    title: 'Alert Dialog',
    desc: 'Modal dialogs for important confirmations and warnings.',
    href: '/design-sample/alert-dialog',
    icon: AlertTriangle,
    preview: 'Delete, Checkout, Logout Confirmations',
    color: 'text-red-700 bg-red-50',
  },
  {
    title: 'Animation',
    desc: 'Motion primitives and complex interaction patterns.',
    href: '/design-sample/animation',
    icon: Sparkles,
    preview: 'Fade, Slide, Scale, Stagger',
    color: 'text-violet-700 bg-violet-50',
  },
];

const scenarios = [
  {
    title: 'Dashboard',
    desc: 'Barista morning overview with stats and switches.',
    href: '/design-sample/dashboard',
    icon: LayoutDashboard,
    preview: 'Stats, Switch, Avatar, Notifications',
    color: 'text-orange-700 bg-orange-50',
  },
  {
    title: 'Roast Journal',
    desc: 'Detailed input form for cupping notes.',
    href: '/design-sample/journal',
    icon: BookOpen,
    preview: 'Slider, Input, Textarea, Form Layout',
    color: 'text-stone-700 bg-stone-50',
  },
  {
    title: 'Bean Origins',
    desc: 'Storytelling page with expandable details.',
    href: '/design-sample/origins',
    icon: Map,
    preview: 'Accordion, Split Layout, Hero Image',
    color: 'text-emerald-700 bg-emerald-50',
  },
  {
    title: 'Settings',
    desc: 'User preferences and account management.',
    href: '/design-sample/settings',
    icon: Settings,
    preview: 'Switch, Avatar, List Groups',
    color: 'text-slate-700 bg-slate-50',
  },
  {
    title: 'Seasonal Menu',
    desc: 'Visual menu grid with detailed popovers.',
    href: '/design-sample/menu',
    icon: Utensils,
    preview: 'Popover, Grid, Rich Cards',
    color: 'text-pink-700 bg-pink-50',
  },
];

const extended = [
  {
    title: 'Workshops',
    desc: 'Class booking system with calendar integration.',
    href: '/design-sample/workshops',
    icon: CalendarDays,
    preview: 'Calendar, Grid Layout, Booking Status',
    color: 'text-indigo-700 bg-indigo-50',
  },
  {
    title: 'Subscription',
    desc: 'Multi-step wizard for building custom bean orders.',
    href: '/design-sample/subscription',
    icon: PackageCheck,
    preview: 'Progress, Radio Group, Wizard Flow',
    color: 'text-cyan-700 bg-cyan-50',
  },
  {
    title: 'Order History',
    desc: 'Data tables for managing coffee orders and invoices.',
    href: '/design-sample/orders',
    icon: ScrollText,
    preview: 'Table, Filters, Badge, Select',
    color: 'text-gray-700 bg-gray-50',
  },
  {
    title: 'Guest Book',
    desc: 'Community reviews in a masonry layout.',
    href: '/design-sample/reviews',
    icon: Users,
    preview: 'Masonry Cards, Avatar, Ratings',
    color: 'text-yellow-700 bg-yellow-50',
  },
  {
    title: 'Member Login',
    desc: 'Aesthetic authentication page split layout.',
    href: '/design-sample/auth',
    icon: LockKeyhole,
    preview: 'Form, Checkbox, Split Screen',
    color: 'text-rose-700 bg-rose-50',
  },
  {
    title: 'The Green Bean Vault',
    desc: 'Concept page for raw material inventory.',
    href: '/design-sample/green-bean-vault',
    icon: Map,
    preview: 'Texture Sidebar, Hero Overlay, Inventory Cards',
    color: 'text-emerald-800 bg-emerald-100',
  },
];

function SampleCard({ sample }: { sample: any }) {
  return (
    <Link href={sample.href} className="group">
      <Card className="h-full border-latte-200 hover:border-latte-400 hover:shadow-xl transition-all duration-300 bg-white overflow-hidden relative">
        <div
          className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity ${sample.color} rounded-bl-[2rem]`}
        >
          <sample.icon size={64} />
        </div>
        <CardHeader>
          <div
            className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${sample.color}`}
          >
            <sample.icon size={24} />
          </div>
          <CardTitle className="font-serif text-2xl text-latte-900 group-hover:text-latte-700 transition-colors">
            {sample.title}
          </CardTitle>
          <CardDescription className="text-latte-500 text-sm min-h-[40px]">
            {sample.desc}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {sample.preview.split(', ').map((tag: string) => (
              <Badge
                key={tag}
                variant="secondary"
                className="bg-latte-50 text-latte-600 font-normal border border-latte-100"
              >
                {tag}
              </Badge>
            ))}
          </div>
        </CardContent>
        <CardFooter className="pt-2">
          <Button
            variant="ghost"
            className="p-0 text-latte-600 hover:text-latte-900 hover:bg-transparent group-hover:translate-x-2 transition-all"
          >
            View Demo <ArrowRight className="ml-2 w-4 h-4" />
          </Button>
        </CardFooter>
      </Card>
    </Link>
  );
}
// ----------------------------

export default function DesignDemoPage() {
  const [selectedTab, setSelectedTab] = useState<
    'components' | 'scenarios' | 'extended' | 'showcase'
  >('showcase');
  const [notification, setNotification] = useState<string | null>(null);

  const showNotification = (message: string) => {
    setNotification(message);
    setTimeout(() => setNotification(null), 3000);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
      },
    },
  };

  const floatingAnimation = {
    y: [0, -10, 0],
    transition: {
      duration: 3,
      repeat: Infinity,
    },
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-latte-50 via-white to-latte-100">
      {/* Hero Section with Animated Background */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="relative overflow-hidden bg-gradient-to-r from-latte-900 via-latte-800 to-latte-900 text-white"
      >
        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              rotate: [0, 90, 0],
              opacity: [0.1, 0.2, 0.1],
            }}
            transition={{ duration: 20, repeat: Infinity }}
            className="absolute -top-1/2 -left-1/2 w-full h-full bg-latte-400/10 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              scale: [1.2, 1, 1.2],
              rotate: [90, 0, 90],
              opacity: [0.2, 0.1, 0.2],
            }}
            transition={{ duration: 15, repeat: Infinity }}
            className="absolute -bottom-1/2 -right-1/2 w-full h-full bg-latte-300/10 rounded-full blur-3xl"
          />
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-center"
          >
            <motion.div animate={floatingAnimation} className="inline-block mb-6">
              <div className="p-4 bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 inline-block">
                <Coffee className="w-16 h-16 text-latte-200" />
              </div>
            </motion.div>

            <h1 className="font-serif text-6xl md:text-7xl font-bold mb-6 tracking-tight">
              TheMoon Design System
            </h1>

            <p className="text-xl md:text-2xl text-latte-200 max-w-3xl mx-auto leading-relaxed font-light mb-8">
              A complete collection of components, scenarios, and style guides.
            </p>

            <div className="flex gap-4 justify-center">
              <Button
                size="lg"
                className="text-lg bg-white text-latte-900 hover:bg-latte-50 shadow-xl hover:shadow-2xl transform hover:-translate-y-0.5 transition-all"
                onClick={() => setSelectedTab('showcase')}
              >
                <Sparkles className="w-5 h-5 mr-2" />
                Showcase
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="text-lg bg-white/10 border-white/30 text-white hover:bg-white/20 backdrop-blur-md"
                onClick={() => setSelectedTab('components')}
              >
                <Layout className="w-5 h-5 mr-2" />
                Samples
              </Button>
            </div>
          </motion.div>
        </div>

        {/* Decorative Wave */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 120" className="w-full h-auto">
            <path
              fill="#FFF8F0"
              d="M0,64L48,69.3C96,75,192,85,288,80C384,75,480,53,576,48C672,43,768,53,864,64C960,75,1056,85,1152,80C1248,75,1344,53,1392,42.7L1440,32L1440,120L1392,120C1344,120,1248,120,1152,120C1056,120,960,120,864,120C768,120,672,120,576,120C480,120,384,120,288,120C192,120,96,120,48,120L0,120Z"
            />
          </svg>
        </div>
      </motion.div>

      {/* Notification Toast */}
      <AnimatePresence>
        {notification && (
          <motion.div
            initial={{ opacity: 0, y: -50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.9 }}
            className="fixed top-4 right-4 z-50 bg-latte-900 text-white px-6 py-4 rounded-2xl shadow-2xl border border-latte-700"
          >
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-5 h-5 text-green-400" />
              <p className="font-medium">{notification}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Tab Navigation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mb-12"
        >
          <div className="bg-white rounded-3xl shadow-lg border border-latte-200 p-2 inline-flex flex-wrap gap-2">
            {[
              { id: 'showcase' as const, label: 'Main Showcase', icon: Sparkles },
              { id: 'components' as const, label: 'UI Components', icon: Package },
              { id: 'scenarios' as const, label: 'Scenarios', icon: Layout },
              { id: 'extended' as const, label: 'Extended Features', icon: Zap },
            ].map((tab) => (
              <Button
                key={tab.id}
                variant={selectedTab === tab.id ? 'default' : 'ghost'}
                className={`text-base px-6 py-6 rounded-2xl transition-all ${
                  selectedTab === tab.id ? 'bg-latte-800 text-white shadow-lg' : 'hover:bg-latte-50'
                }`}
                onClick={() => setSelectedTab(tab.id)}
              >
                <tab.icon className="w-5 h-5 mr-2" />
                {tab.label}
              </Button>
            ))}
          </div>
        </motion.div>

        {/* --- SHOWCASE CONTENT --- */}
        {selectedTab === 'showcase' && (
          <motion.div
            key="showcase"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-12"
          >
            {/* Statistics Cards */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6 flex items-center gap-3">
                <Activity className="w-8 h-8 text-latte-600" />
                통계 카드 데모
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                  { icon: Coffee, label: '총 원두', value: '48', unit: '종류', color: 'latte' },
                  { icon: Palette, label: '블렌드', value: '23', unit: '레시피', color: 'latte' },
                  {
                    icon: TrendingUp,
                    label: '매출',
                    value: '₩2.4M',
                    unit: '이번 달',
                    color: 'green',
                  },
                  { icon: Users, label: '고객', value: '1,234', unit: '명', color: 'blue' },
                ].map((stat, idx) => (
                  <motion.div
                    key={idx}
                    whileHover={{ scale: 1.03, y: -5 }}
                    transition={{ type: 'spring', stiffness: 300 }}
                  >
                    <Card className="border-latte-200 hover:border-latte-400 hover:shadow-xl transition-all">
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div
                            className={`p-3 rounded-2xl bg-${stat.color === 'latte' ? 'latte' : stat.color}-100`}
                          >
                            <stat.icon
                              className={`w-6 h-6 text-${stat.color === 'latte' ? 'latte' : stat.color}-600`}
                            />
                          </div>
                          <Badge variant="secondary" className="bg-latte-50">
                            <TrendingUp className="w-3 h-3 mr-1" />
                            +12%
                          </Badge>
                        </div>
                        <p className="text-latte-600 text-sm font-medium mb-1">{stat.label}</p>
                        <p className="text-3xl font-bold text-latte-900">
                          {stat.value}
                          <span className="text-base text-latte-400 ml-2 font-normal">
                            {stat.unit}
                          </span>
                        </p>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.section>

            {/* Alert Badges */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6 flex items-center gap-3">
                <Bell className="w-8 h-8 text-latte-600" />
                알림 배지 스타일
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                  {
                    icon: CheckCircle2,
                    title: '성공',
                    desc: '작업이 완료되었습니다',
                    color: 'green',
                    bg: 'green-50',
                    border: 'green-200',
                  },
                  {
                    icon: AlertTriangle,
                    title: '경고',
                    desc: '재고가 부족합니다',
                    color: 'amber',
                    bg: 'amber-50',
                    border: 'amber-200',
                  },
                  {
                    icon: XCircle,
                    title: '오류',
                    desc: '연결에 실패했습니다',
                    color: 'red',
                    bg: 'red-50',
                    border: 'red-200',
                  },
                ].map((alert, idx) => (
                  <motion.div
                    key={idx}
                    whileHover={{ scale: 1.02 }}
                    transition={{ type: 'spring', stiffness: 400 }}
                  >
                    <Card
                      className={`border-${alert.border} bg-${alert.bg}/50 hover:shadow-lg transition-all`}
                    >
                      <CardContent className="p-6">
                        <div className="flex items-start gap-4">
                          <div className={`p-3 rounded-2xl bg-${alert.color}-100`}>
                            <alert.icon className={`w-6 h-6 text-${alert.color}-600`} />
                          </div>
                          <div className="flex-1">
                            <h3 className={`text-lg font-bold text-${alert.color}-900 mb-1`}>
                              {alert.title}
                            </h3>
                            <p className={`text-${alert.color}-600 text-sm`}>{alert.desc}</p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.section>
          </motion.div>
        )}

        {/* --- COMPONENTS TAB --- */}
        {selectedTab === 'components' && (
          <motion.div
            key="components"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-12"
          >
            <motion.section variants={itemVariants}>
              <div className="text-center mb-10">
                <h2 className="text-3xl font-serif font-bold text-latte-900 mb-4">
                  Base UI Components
                </h2>
                <p className="text-latte-600">
                  Fundamental building blocks for the application interface.
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {components.map((sample) => (
                  <SampleCard key={sample.title} sample={sample} />
                ))}
              </div>
            </motion.section>
          </motion.div>
        )}

        {/* --- SCENARIOS TAB --- */}
        {selectedTab === 'scenarios' && (
          <motion.div
            key="scenarios"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-12"
          >
            <motion.section variants={itemVariants}>
              <div className="text-center mb-10">
                <h2 className="text-3xl font-serif font-bold text-latte-900 mb-4">
                  Real-world Scenarios
                </h2>
                <p className="text-latte-600">Full page layouts representing common user flows.</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {scenarios.map((sample) => (
                  <SampleCard key={sample.title} sample={sample} />
                ))}
              </div>
            </motion.section>
          </motion.div>
        )}

        {/* --- EXTENDED TAB --- */}
        {selectedTab === 'extended' && (
          <motion.div
            key="extended"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-12"
          >
            <motion.section variants={itemVariants}>
              <div className="text-center mb-10">
                <h2 className="text-3xl font-serif font-bold text-latte-900 mb-4">
                  Extended Features
                </h2>
                <p className="text-latte-600">
                  Advanced/Complex layouts and experimental features.
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {extended.map((sample) => (
                  <SampleCard key={sample.title} sample={sample} />
                ))}
              </div>
            </motion.section>
          </motion.div>
        )}
      </div>
    </div>
  );
}
