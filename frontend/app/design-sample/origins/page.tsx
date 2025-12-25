'use client';

import React from 'react';
import Link from 'next/link';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { ArrowLeft, MapPin, Calendar, Award } from 'lucide-react';

export default function OriginsPage() {
  return (
    <div className="min-h-screen bg-white font-sans relative">
      {/* Back Nav */}
      <div className="absolute top-4 left-4 z-50">
        <Button
          asChild
          variant="ghost"
          className="text-white hover:text-white hover:bg-white/20 transition-colors"
        >
          <Link href="/design-sample">
            <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
          </Link>
        </Button>
      </div>

      <div className="flex flex-col lg:flex-row min-h-screen">
        {/* Left: Imagery */}
        <div className="w-full lg:w-1/2 bg-latte-900 relative min-h-[400px] lg:min-h-screen">
          <img
            src="/images/beans/ethiopia.png"
            alt="Coffee Farm"
            className="absolute inset-0 w-full h-full object-cover opacity-60 mix-blend-overlay grayscale contrast-125"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-latte-900 via-transparent to-transparent lg:bg-gradient-to-r"></div>

          <div className="absolute bottom-12 left-12 right-12 text-white">
            <div className="inline-flex items-center gap-2 border border-white/30 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest mb-4 backdrop-blur-sm">
              <MapPin size={12} /> Yirgacheffe, Ethiopia
            </div>
            <h1 className="font-serif text-5xl lg:text-7xl font-bold leading-tight mb-4">
              The Birth of
              <br />
              Floral Notes
            </h1>
            <p className="text-latte-100 max-w-md text-lg leading-relaxed opacity-90">
              Discover the ancient traditions and high-altitude drying processes that give our
              signature bean its distinctive character.
            </p>
          </div>
        </div>

        {/* Right: Content Accordion */}
        <div className="w-full lg:w-1/2 p-8 lg:p-24 bg-latte-50 flex flex-col justify-center">
          <div className="max-w-lg mx-auto w-full">
            <h2 className="font-serif text-3xl text-latte-900 mb-8 border-b border-latte-200 pb-4">
              Bean Chronicles
            </h2>

            <Accordion
              type="single"
              collapsible
              defaultValue="item-1"
              className="bg-white rounded-2xl shadow-sm border border-latte-100 overflow-hidden"
            >
              <AccordionItem value="item-1" className="border-b-latte-100 px-6">
                <AccordionTrigger className="hover:no-underline py-6">
                  <div className="flex items-center text-left">
                    <div className="w-10 h-10 rounded-full bg-latte-100 text-latte-600 flex items-center justify-center mr-4">
                      <span className="font-serif font-bold text-lg">01</span>
                    </div>
                    <span className="font-bold text-lg text-latte-800">History & Heritage</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="text-latte-600 leading-relaxed pl-14 pb-6">
                  Coffee Arabica originated in Ethiopia. The Yirgacheffe region is widely considered
                  the birthplace of coffee, where it grows naturally in the forest. Our partner farm
                  has been cultivating these heirloom varieties for over 3 generations.
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-2" className="border-b-latte-100 px-6">
                <AccordionTrigger className="hover:no-underline py-6">
                  <div className="flex items-center text-left">
                    <div className="w-10 h-10 rounded-full bg-latte-100 text-latte-600 flex items-center justify-center mr-4">
                      <span className="font-serif font-bold text-lg">02</span>
                    </div>
                    <span className="font-bold text-lg text-latte-800">Process Method</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="text-latte-600 leading-relaxed pl-14 pb-6">
                  <div className="space-y-4">
                    <p>
                      Washed processing mimics the clarity of tea. The cherries are pulped,
                      fermented for 12-24 hours, and then washed in clean mountain water.
                    </p>
                    <div className="bg-latte-50 p-4 rounded-lg flex gap-4 text-xs font-bold text-latte-500 uppercase">
                      <span className="flex items-center gap-1">
                        <Calendar size={12} /> Harvest: Oct-Dec
                      </span>
                      <span className="flex items-center gap-1">
                        <Award size={12} /> Grade: G1
                      </span>
                    </div>
                  </div>
                </AccordionContent>
              </AccordionItem>

              <AccordionItem value="item-3" className="border-none px-6">
                <AccordionTrigger className="hover:no-underline py-6">
                  <div className="flex items-center text-left">
                    <div className="w-10 h-10 rounded-full bg-latte-100 text-latte-600 flex items-center justify-center mr-4">
                      <span className="font-serif font-bold text-lg">03</span>
                    </div>
                    <span className="font-bold text-lg text-latte-800">Roast Profile</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="text-latte-600 leading-relaxed pl-14 pb-6">
                  We roast this bean lightly to preserve its delicate jasmine and lemon zest notes.
                  A deeper roast would obscure the very characteristics that make Yirgacheffe
                  famous.
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
        </div>
      </div>
    </div>
  );
}
