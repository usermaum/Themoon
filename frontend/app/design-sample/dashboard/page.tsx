'use client';

import React from 'react';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Bell, Coffee, Users, TrendingUp, Sun } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-latte-50 p-8 font-sans relative">
      {/* Back Nav */}
      <div className="absolute top-4 left-4 z-50">
        <Button
          asChild
          variant="ghost"
          className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors"
        >
          <Link href="/design-sample">
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
          </Link>
        </Button>
      </div>

      {/* Header */}
      <header className="flex justify-between items-center mb-12 pt-12 max-w-6xl mx-auto">
        <div>
          <h1 className="font-serif text-4xl text-latte-900 font-bold tracking-tight">
            Morning Dashboard
          </h1>
          <p className="text-latte-600 mt-2">Good morning, Master Roaster.</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm border border-latte-100">
            <Sun className="h-4 w-4 text-orange-400" />
            <span className="text-sm font-medium text-latte-700">Open</span>
            <Switch
              id="store-status"
              defaultChecked
              className="data-[state=checked]:bg-green-600"
            />
          </div>
          <Avatar className="h-12 w-12 border-2 border-white shadow-md cursor-pointer hover:scale-105 transition-transform">
            <AvatarImage src="/images/avatar-placeholder.png" alt="Barista" />
            <AvatarFallback className="bg-latte-800 text-latte-50">BR</AvatarFallback>
          </Avatar>
        </div>
      </header>

      {/* Main Stats */}
      <main className="max-w-6xl mx-auto space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-white border-none shadow-lg shadow-latte-900/5 hover:-translate-y-1 transition-transform duration-300">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-latte-500 uppercase tracking-widest">
                Active Orders
              </CardTitle>
              <Coffee className="h-4 w-4 text-latte-400" />
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-serif font-bold text-latte-900">24</div>
              <p className="text-xs text-latte-400 mt-1 flex items-center">
                <span className="text-green-600 font-bold mr-1 flex items-center">
                  <TrendingUp className="h-3 w-3 mr-0.5" /> +12%
                </span>{' '}
                from last hour
              </p>
            </CardContent>
          </Card>
          <Card className="bg-white border-none shadow-lg shadow-latte-900/5 hover:-translate-y-1 transition-transform duration-300">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-latte-500 uppercase tracking-widest">
                Revenue
              </CardTitle>
              <span className="font-mono text-latte-400">₩</span>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-serif font-bold text-latte-900">450k</div>
              <p className="text-xs text-latte-400 mt-1">Today's accumulated sales</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-latte-800 to-latte-900 text-white border-none shadow-xl hover:-translate-y-1 transition-transform duration-300 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-24 h-24 bg-white opacity-5 rounded-bl-full"></div>
            <CardHeader className="flex flex-row items-center justify-between pb-2 relative z-10">
              <CardTitle className="text-sm font-medium text-latte-200 uppercase tracking-widest">
                VIP Visits
              </CardTitle>
              <Users className="h-4 w-4 text-latte-200" />
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-4xl font-serif font-bold text-latte-50">7</div>
              <div className="flex gap-2 mt-2">
                <Avatar className="h-6 w-6 border border-white/20">
                  <AvatarFallback className="bg-latte-700 text-[10px]">A</AvatarFallback>
                </Avatar>
                <Avatar className="h-6 w-6 border border-white/20">
                  <AvatarFallback className="bg-latte-700 text-[10px]">B</AvatarFallback>
                </Avatar>
                <span className="text-xs text-latte-300 self-center">+5 others</span>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Notifications */}
        <Card className="bg-white/80 backdrop-blur-sm border-latte-100">
          <CardHeader>
            <CardTitle className="font-serif text-xl text-latte-900">
              Recent Notifications
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {[
              {
                title: 'New Bean Shipment',
                desc: 'Ethiopia Sidamo set arrived.',
                time: '2m ago',
                type: 'info',
              },
              {
                title: 'Machine Maintenance',
                desc: 'Group head cleaning required.',
                time: '1h ago',
                type: 'warning',
              },
              {
                title: 'Goal Reached',
                desc: 'Monthly sales target achieved!',
                time: '3h ago',
                type: 'success',
              },
            ].map((item, i) => (
              <div
                key={i}
                className="flex items-start gap-4 p-3 rounded-xl hover:bg-latte-50 transition-colors"
              >
                <div
                  className={`mt-1 h-2 w-2 rounded-full shrink-0 ${
                    item.type === 'info'
                      ? 'bg-blue-400'
                      : item.type === 'warning'
                        ? 'bg-orange-400'
                        : 'bg-green-400'
                  }`}
                ></div>
                <div className="flex-1">
                  <h4 className="text-sm font-medium text-latte-900">{item.title}</h4>
                  <p className="text-xs text-latte-500">{item.desc}</p>
                </div>
                <span className="text-xs text-latte-300 font-mono">{item.time}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
