'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
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
  Activity
} from 'lucide-react'

export default function DesignShowcasePage() {
  const [selectedTab, setSelectedTab] = useState<'components' | 'layouts' | 'interactions'>('components')
  const [notification, setNotification] = useState<string | null>(null)

  const showNotification = (message: string) => {
    setNotification(message)
    setTimeout(() => setNotification(null), 3000)
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5
      }
    }
  }

  const floatingAnimation = {
    y: [0, -10, 0],
    transition: {
      duration: 3,
      repeat: Infinity
    }
  }

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
              opacity: [0.1, 0.2, 0.1]
            }}
            transition={{ duration: 20, repeat: Infinity }}
            className="absolute -top-1/2 -left-1/2 w-full h-full bg-latte-400/10 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              scale: [1.2, 1, 1.2],
              rotate: [90, 0, 90],
              opacity: [0.2, 0.1, 0.2]
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
            <motion.div
              animate={floatingAnimation}
              className="inline-block mb-6"
            >
              <div className="p-4 bg-white/10 backdrop-blur-md rounded-3xl border border-white/20 inline-block">
                <Coffee className="w-16 h-16 text-latte-200" />
              </div>
            </motion.div>

            <h1 className="font-serif text-6xl md:text-7xl font-bold mb-6 tracking-tight">
              TheMoon Design System
            </h1>

            <p className="text-xl md:text-2xl text-latte-200 max-w-3xl mx-auto leading-relaxed font-light mb-8">
              프리미엄 커피 로스팅 관리를 위한 세련된 디자인 언어
            </p>

            <div className="flex gap-4 justify-center">
              <Button
                size="lg"
                className="text-lg bg-white text-latte-900 hover:bg-latte-50 shadow-xl hover:shadow-2xl transform hover:-translate-y-0.5 transition-all"
                onClick={() => showNotification('환영합니다! 🎉')}
              >
                <Sparkles className="w-5 h-5 mr-2" />
                시작하기
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="text-lg bg-white/10 border-white/30 text-white hover:bg-white/20 backdrop-blur-md"
              >
                <Award className="w-5 h-5 mr-2" />
                더 알아보기
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
          <div className="bg-white rounded-3xl shadow-lg border border-latte-200 p-2 inline-flex gap-2">
            {[
              { id: 'components' as const, label: '컴포넌트', icon: Package },
              { id: 'layouts' as const, label: '레이아웃', icon: BarChart3 },
              { id: 'interactions' as const, label: '인터랙션', icon: Zap }
            ].map(tab => (
              <Button
                key={tab.id}
                variant={selectedTab === tab.id ? 'default' : 'ghost'}
                className={`text-base px-6 py-6 rounded-2xl transition-all ${
                  selectedTab === tab.id
                    ? 'bg-latte-800 text-white shadow-lg'
                    : 'hover:bg-latte-50'
                }`}
                onClick={() => setSelectedTab(tab.id)}
              >
                <tab.icon className="w-5 h-5 mr-2" />
                {tab.label}
              </Button>
            ))}
          </div>
        </motion.div>

        {/* Components Tab */}
        {selectedTab === 'components' && (
          <motion.div
            key="components"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-12"
          >
            {/* Statistics Cards */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6 flex items-center gap-3">
                <Activity className="w-8 h-8 text-latte-600" />
                통계 카드
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                  { icon: Coffee, label: '총 원두', value: '48', unit: '종류', color: 'latte' },
                  { icon: Palette, label: '블렌드', value: '23', unit: '레시피', color: 'latte' },
                  { icon: TrendingUp, label: '매출', value: '₩2.4M', unit: '이번 달', color: 'green' },
                  { icon: Users, label: '고객', value: '1,234', unit: '명', color: 'blue' }
                ].map((stat, idx) => (
                  <motion.div
                    key={idx}
                    whileHover={{ scale: 1.03, y: -5 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <Card className="border-latte-200 hover:border-latte-400 hover:shadow-xl transition-all">
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div className={`p-3 rounded-2xl bg-${stat.color === 'latte' ? 'latte' : stat.color}-100`}>
                            <stat.icon className={`w-6 h-6 text-${stat.color === 'latte' ? 'latte' : stat.color}-600`} />
                          </div>
                          <Badge variant="secondary" className="bg-latte-50">
                            <TrendingUp className="w-3 h-3 mr-1" />
                            +12%
                          </Badge>
                        </div>
                        <p className="text-latte-600 text-sm font-medium mb-1">{stat.label}</p>
                        <p className="text-3xl font-bold text-latte-900">
                          {stat.value}
                          <span className="text-base text-latte-400 ml-2 font-normal">{stat.unit}</span>
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
                알림 배지
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                  { icon: CheckCircle2, title: '성공', desc: '작업이 완료되었습니다', color: 'green', bg: 'green-50', border: 'green-200' },
                  { icon: AlertTriangle, title: '경고', desc: '재고가 부족합니다', color: 'amber', bg: 'amber-50', border: 'amber-200' },
                  { icon: XCircle, title: '오류', desc: '연결에 실패했습니다', color: 'red', bg: 'red-50', border: 'red-200' }
                ].map((alert, idx) => (
                  <motion.div
                    key={idx}
                    whileHover={{ scale: 1.02 }}
                    transition={{ type: "spring", stiffness: 400 }}
                  >
                    <Card className={`border-${alert.border} bg-${alert.bg}/50 hover:shadow-lg transition-all`}>
                      <CardContent className="p-6">
                        <div className="flex items-start gap-4">
                          <div className={`p-3 rounded-2xl bg-${alert.color}-100`}>
                            <alert.icon className={`w-6 h-6 text-${alert.color}-600`} />
                          </div>
                          <div className="flex-1">
                            <h3 className={`text-lg font-bold text-${alert.color}-900 mb-1`}>{alert.title}</h3>
                            <p className={`text-${alert.color}-600 text-sm`}>{alert.desc}</p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.section>

            {/* Buttons Showcase */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6 flex items-center gap-3">
                <Target className="w-8 h-8 text-latte-600" />
                버튼 스타일
              </h2>
              <Card className="border-latte-200">
                <CardContent className="p-8">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="space-y-4">
                      <h3 className="text-lg font-bold text-latte-800 mb-4">Primary Actions</h3>
                      <div className="flex flex-wrap gap-3">
                        <Button size="lg" onClick={() => showNotification('Primary 클릭!')}>
                          <Coffee className="w-4 h-4 mr-2" />
                          Primary Large
                        </Button>
                        <Button onClick={() => showNotification('Medium 클릭!')}>
                          <Star className="w-4 h-4 mr-2" />
                          Medium
                        </Button>
                        <Button size="sm" onClick={() => showNotification('Small 클릭!')}>
                          Small
                        </Button>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <h3 className="text-lg font-bold text-latte-800 mb-4">Secondary Actions</h3>
                      <div className="flex flex-wrap gap-3">
                        <Button variant="outline" size="lg">
                          <Filter className="w-4 h-4 mr-2" />
                          Outline Large
                        </Button>
                        <Button variant="outline">
                          <Search className="w-4 h-4 mr-2" />
                          Outline
                        </Button>
                        <Button variant="ghost">
                          <Settings className="w-4 h-4 mr-2" />
                          Ghost
                        </Button>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <h3 className="text-lg font-bold text-latte-800 mb-4">Destructive</h3>
                      <div className="flex flex-wrap gap-3">
                        <Button variant="destructive" size="lg">
                          <XCircle className="w-4 h-4 mr-2" />
                          Delete
                        </Button>
                        <Button variant="destructive">
                          Remove
                        </Button>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <h3 className="text-lg font-bold text-latte-800 mb-4">With Icons</h3>
                      <div className="flex flex-wrap gap-3">
                        <Button className="bg-gradient-to-r from-latte-700 to-latte-900">
                          <Sparkles className="w-4 h-4 mr-2" />
                          Special
                        </Button>
                        <Button className="bg-green-600 hover:bg-green-700">
                          <CheckCircle2 className="w-4 h-4 mr-2" />
                          Confirm
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.section>

            {/* Form Elements */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6 flex items-center gap-3">
                <Info className="w-8 h-8 text-latte-600" />
                폼 요소
              </h2>
              <Card className="border-latte-200">
                <CardContent className="p-8">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <div>
                        <label className="text-sm font-medium text-latte-700 mb-2 block">
                          원두 이름
                        </label>
                        <Input
                          placeholder="예: Ethiopia Yirgacheffe"
                          className="border-latte-300 focus:border-latte-500"
                        />
                      </div>
                      <div>
                        <label className="text-sm font-medium text-latte-700 mb-2 block">
                          검색
                        </label>
                        <div className="relative">
                          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-latte-400" />
                          <Input
                            placeholder="원두, 블렌드 검색..."
                            className="pl-10 border-latte-300"
                          />
                        </div>
                      </div>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-latte-700 mb-2 block">
                        메모
                      </label>
                      <Textarea
                        placeholder="로스팅 노트를 입력하세요..."
                        className="border-latte-300 focus:border-latte-500 min-h-[120px]"
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.section>
          </motion.div>
        )}

        {/* Layouts Tab */}
        {selectedTab === 'layouts' && (
          <motion.div
            key="layouts"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-12"
          >
            {/* Dashboard Layout */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6">
                대시보드 레이아웃
              </h2>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-6">
                  <Card className="border-latte-200">
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between">
                        <span className="flex items-center gap-2">
                          <BarChart3 className="w-5 h-5 text-latte-600" />
                          판매 추이
                        </span>
                        <Badge variant="secondary">최근 7일</Badge>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="h-64 bg-gradient-to-br from-latte-50 to-latte-100 rounded-xl flex items-center justify-center">
                        <div className="text-center">
                          <PieChart className="w-16 h-16 text-latte-300 mx-auto mb-4" />
                          <p className="text-latte-500">차트 영역</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>

                <div className="space-y-6">
                  <Card className="border-latte-200 bg-gradient-to-br from-latte-900 to-latte-800 text-white">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Moon className="w-5 h-5" />
                        오늘의 목표
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div>
                          <div className="flex justify-between text-sm mb-2">
                            <span>로스팅</span>
                            <span>75%</span>
                          </div>
                          <div className="h-2 bg-white/20 rounded-full overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: '75%' }}
                              transition={{ duration: 1, delay: 0.5 }}
                              className="h-full bg-white rounded-full"
                            />
                          </div>
                        </div>
                        <div>
                          <div className="flex justify-between text-sm mb-2">
                            <span>품질 검사</span>
                            <span>90%</span>
                          </div>
                          <div className="h-2 bg-white/20 rounded-full overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: '90%' }}
                              transition={{ duration: 1, delay: 0.7 }}
                              className="h-full bg-latte-200 rounded-full"
                            />
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="border-latte-200">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Calendar className="w-5 h-5 text-latte-600" />
                        오늘 일정
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        {[
                          { time: '09:00', task: '원두 입고 검수', color: 'blue' },
                          { time: '14:00', task: '블렌딩 작업', color: 'green' },
                          { time: '16:30', task: '재고 점검', color: 'amber' }
                        ].map((item, idx) => (
                          <motion.div
                            key={idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.8 + idx * 0.1 }}
                            className="flex items-center gap-3 p-3 rounded-xl bg-latte-50 hover:bg-latte-100 transition-colors"
                          >
                            <div className={`w-2 h-2 rounded-full bg-${item.color}-500`} />
                            <span className="text-sm font-mono text-latte-600">{item.time}</span>
                            <span className="text-sm text-latte-800 font-medium">{item.task}</span>
                          </motion.div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>
            </motion.section>

            {/* Grid Layouts */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6">
                그리드 레이아웃
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { name: 'Antigua', image: '/images/beans/antigua.png' },
                  { name: 'Brazil', image: '/images/beans/brazil.png' },
                  { name: 'Colombia', image: '/images/beans/colombia.png' },
                  { name: 'Ethiopia', image: '/images/beans/ethiopia.png' },
                  { name: 'El Tanque', image: '/images/beans/el-tanque.png' },
                  { name: 'Fazenda', image: '/images/beans/fazenda-carmo.png' },
                  { name: 'Decaf SDM', image: '/images/beans/decaf-sdm.png' },
                  { name: 'Decaf SM', image: '/images/beans/decaf-sm.png' }
                ].map((bean, idx) => (
                  <motion.div
                    key={idx}
                    whileHover={{ scale: 1.05, y: -8 }}
                    transition={{ type: "spring", stiffness: 300 }}
                    className="group aspect-square bg-white rounded-2xl shadow-md hover:shadow-2xl transition-all overflow-hidden cursor-pointer border border-latte-200 hover:border-latte-400"
                  >
                    <div className="relative h-full flex flex-col">
                      {/* Image Container */}
                      <div className="flex-1 relative overflow-hidden bg-gradient-to-br from-latte-50 to-latte-100 p-4">
                        <motion.img
                          whileHover={{ scale: 1.1, rotate: 5 }}
                          transition={{ duration: 0.3 }}
                          src={bean.image}
                          alt={bean.name}
                          className="w-full h-full object-contain drop-shadow-lg"
                        />
                        {/* Overlay on Hover */}
                        <motion.div
                          initial={{ opacity: 0 }}
                          whileHover={{ opacity: 1 }}
                          className="absolute inset-0 bg-latte-900/10 backdrop-blur-[1px] flex items-center justify-center"
                        >
                          <div className="w-12 h-12 bg-white/90 rounded-full flex items-center justify-center shadow-xl">
                            <Heart className="w-6 h-6 text-latte-600" />
                          </div>
                        </motion.div>
                      </div>

                      {/* Label */}
                      <div className="p-3 bg-white border-t border-latte-100">
                        <p className="text-sm font-semibold text-latte-900 text-center truncate group-hover:text-latte-700 transition-colors">
                          {bean.name}
                        </p>
                        <div className="flex items-center justify-center gap-1 mt-1">
                          <div className="w-1 h-1 rounded-full bg-latte-400" />
                          <div className="w-1 h-1 rounded-full bg-latte-400" />
                          <div className="w-1 h-1 rounded-full bg-latte-400" />
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.section>
          </motion.div>
        )}

        {/* Interactions Tab */}
        {selectedTab === 'interactions' && (
          <motion.div
            key="interactions"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-12"
          >
            {/* Hover Effects */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6">
                호버 효과
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                  { title: 'Scale Up', icon: Zap, color: 'from-purple-500 to-pink-500' },
                  { title: 'Rotate', icon: Star, color: 'from-blue-500 to-cyan-500' },
                  { title: 'Glow', icon: Sparkles, color: 'from-amber-500 to-orange-500' }
                ].map((item, idx) => (
                  <motion.div
                    key={idx}
                    whileHover={{ scale: 1.1, rotate: idx === 1 ? 5 : 0 }}
                    whileTap={{ scale: 0.95 }}
                    className={`aspect-square bg-gradient-to-br ${item.color} rounded-3xl shadow-lg cursor-pointer flex flex-col items-center justify-center text-white hover:shadow-2xl transition-shadow`}
                  >
                    <item.icon className="w-16 h-16 mb-4" />
                    <h3 className="text-xl font-bold">{item.title}</h3>
                  </motion.div>
                ))}
              </div>
            </motion.section>

            {/* Loading States */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6">
                로딩 상태
              </h2>
              <Card className="border-latte-200">
                <CardContent className="p-8">
                  <div className="flex flex-col items-center justify-center space-y-6">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 2, repeat: Infinity }}
                      className="w-16 h-16 border-4 border-latte-200 border-t-latte-800 rounded-full"
                    />
                    <div className="space-y-3 w-full max-w-md">
                      {[100, 80, 60].map((width, idx) => (
                        <motion.div
                          key={idx}
                          initial={{ opacity: 0.3 }}
                          animate={{ opacity: [0.3, 1, 0.3] }}
                          transition={{ duration: 1.5, delay: idx * 0.2, repeat: Infinity }}
                          className="h-4 bg-latte-200 rounded-full"
                          style={{ width: `${width}%` }}
                        />
                      ))}
                    </div>
                    <p className="text-latte-600 font-medium">데이터를 불러오는 중...</p>
                  </div>
                </CardContent>
              </Card>
            </motion.section>

            {/* Animated Cards */}
            <motion.section variants={itemVariants}>
              <h2 className="text-3xl font-serif font-bold text-latte-900 mb-6">
                애니메이션 카드
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {[
                  { title: '스무스 페이드인', desc: '부드러운 등장 애니메이션', icon: Sun },
                  { title: '스케일 효과', desc: '크기 변화와 함께', icon: Moon },
                  { title: '슬라이드 업', desc: '아래에서 위로', icon: Award },
                  { title: '회전 애니메이션', desc: '3D 효과와 함께', icon: Target }
                ].map((card, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 50 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: false, margin: "-100px" }}
                    transition={{ duration: 0.6, delay: idx * 0.1 }}
                  >
                    <Card className="border-latte-200 hover:border-latte-400 group cursor-pointer">
                      <CardContent className="p-6">
                        <div className="flex items-start gap-4">
                          <div className="p-3 bg-latte-100 rounded-2xl group-hover:bg-latte-800 transition-colors">
                            <card.icon className="w-6 h-6 text-latte-600 group-hover:text-white transition-colors" />
                          </div>
                          <div className="flex-1">
                            <h3 className="text-lg font-bold text-latte-900 mb-1">{card.title}</h3>
                            <p className="text-latte-600 text-sm">{card.desc}</p>
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
      </div>
    </div>
  )
}
