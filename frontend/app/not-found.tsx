'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import MascotStatus from '@/components/ui/mascot-status';
import { Home, ArrowLeft } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-latte-50 flex flex-col items-center justify-center p-6">
      <MascotStatus
        variant="not-found"
        title="길을 잃으셨나요? 냥..."
        description="요청하신 페이지가 존재하지 않거나 어딘가로 숨어버린 것 같아요. 관리자 냥이가 열심히 찾고 있답니다!"
        videoClassName="w-80 h-80"
        action={
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <Link href="/">
              <motion.button
                whileTap={{ scale: 0.98 }}
                className="flex items-center justify-center gap-2 px-8 py-3 bg-latte-900 text-white rounded-full font-bold shadow-lg shadow-latte-900/20 hover:bg-black transition-all whitespace-nowrap"
              >
                <Home className="w-4 h-4" />
                홈으로 돌아가기
              </motion.button>
            </Link>

            <button
              onClick={() => window.history.back()}
              className="flex items-center justify-center gap-2 px-8 py-3 bg-white text-latte-600 rounded-full font-bold border border-latte-200 hover:bg-latte-50 transition-all whitespace-nowrap"
            >
              <ArrowLeft className="w-4 h-4" />
              이전 페이지로
            </button>
          </div>
        }
      />

      {/* Decorative Elements */}
      <div className="fixed bottom-0 left-0 w-64 h-64 bg-amber-500/5 rounded-full blur-3xl -ml-32 -mb-32 pointer-events-none" />
      <div className="fixed top-0 right-0 w-96 h-96 bg-latte-200/20 rounded-full blur-3xl -mr-48 -mt-48 pointer-events-none" />
    </div>
  );
}
