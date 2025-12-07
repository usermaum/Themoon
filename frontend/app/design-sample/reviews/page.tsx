'use client'

import React from 'react'
import Link from 'next/link'
import { Card, CardContent, CardHeader } from "@/components/ui/Card"
import { Button } from "@/components/ui/Button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/Badge"
import { ArrowLeft, Quote, Star, ThumbsUp } from 'lucide-react'

export default function ReviewsPage() {
    return (
        <div className="min-h-screen bg-[#FDFBF7] p-8 md:p-12 font-sans relative">
            {/* Back Nav */}
            <div className="absolute top-4 left-4 z-50">
                <Button asChild variant="ghost" className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <div className="max-w-7xl mx-auto pt-12">
                <div className="text-center mb-16 px-4">
                    <h1 className="font-serif text-5xl font-bold text-latte-900 mb-6">Guest Book</h1>
                    <p className="text-latte-600 max-w-2xl mx-auto text-lg">
                        Stories from our community. <br />Share your coffee moments with us.
                    </p>
                    <div className="mt-8 flex justify-center gap-2">
                        <Badge className="bg-latte-900 text-white text-lg py-1 px-4">4.9/5.0</Badge>
                        <span className="self-center text-sm text-latte-500 font-bold uppercase tracking-wider">Based on 1,240 Reviews</span>
                    </div>
                </div>

                <div className="columns-1 md:columns-2 lg:columns-3 gap-8 space-y-8">

                    <ReviewCard
                        name="Elena Gilbert"
                        role="Coffee Enthusiast"
                        rating={5}
                        text="The Ethiopia Yirgacheffe is absolutely divine. The floral notes are not overwhelming but present enough to make every sip a delight. Highly recommended for pour-over lovers!"
                        date="2 days ago"
                        image="/images/avatar-1.png"
                    />

                    <ReviewCard
                        name="Damon S."
                        role="Verified Buyer"
                        rating={5}
                        text="Fast shipping and the packaging is beautiful. It felt like opening a gift. The beans were roasted just 3 days before arrival."
                        date="1 week ago"
                        image="/images/avatar-2.png"
                    />

                    <ReviewCard
                        name="Stefan W."
                        role="Barista"
                        rating={4}
                        text="Great body on the Espresso blend. Crema is thick and hazelnutty. Would love a slightly darker roast option as well."
                        date="3 weeks ago"
                        image="/images/avatar-3.png"
                    />

                    <ReviewCard
                        name="Bonnie B."
                        role="Local Guide"
                        rating={5}
                        text="Best roastery in town. The atmosphere is cozy and the staff actually knows their stuff. I learned so much about origin processing today."
                        date="1 month ago"
                        image="/images/avatar-placeholder.png"
                    />

                    <ReviewCard
                        name="Caroline F."
                        role="Regular"
                        rating={5}
                        text="I subscribe to the weekly box and I'm never disappointed. It's the highlight of my Monday mornings."
                        date="2 months ago"
                        image="/images/avatar-placeholder.png"
                    />

                    <ReviewCard
                        name="Alaric S."
                        role="Teacher"
                        rating={4}
                        text="Solid consistency. Good price point for the quality provided."
                        date="2 months ago"
                        image="/images/avatar-placeholder.png"
                    />
                </div>
            </div>
        </div>
    )
}

function ReviewCard({ name, role, rating, text, date, image }: any) {
    return (
        <Card className="bg-white border-none shadow-md hover:shadow-xl transition-shadow break-inside-avoid mb-8 relative">
            <div className="absolute top-4 right-4 text-latte-100">
                <Quote size={40} />
            </div>
            <CardContent className="p-8">
                <div className="flex items-center gap-1 mb-4">
                    {[...Array(5)].map((_, i) => (
                        <Star key={i} size={14} className={i < rating ? "fill-yellow-400 text-yellow-400" : "text-gray-200"} />
                    ))}
                </div>
                <p className="text-latte-700 leading-relaxed mb-6 font-serif text-lg">
                    "{text}"
                </p>
                <div className="flex items-center gap-3">
                    <Avatar className="h-10 w-10 border border-latte-100">
                        <AvatarImage src={image} />
                        <AvatarFallback className="bg-latte-100 text-latte-600">{name.charAt(0)}</AvatarFallback>
                    </Avatar>
                    <div>
                        <div className="font-bold text-sm text-latte-900">{name}</div>
                        <div className="text-xs text-latte-400">{role}</div>
                    </div>
                </div>
                <div className="mt-6 flex justify-between items-center border-t border-latte-50 pt-4">
                    <span className="text-xs text-latte-300">{date}</span>
                    <button className="flex items-center gap-1 text-xs font-bold text-latte-400 hover:text-latte-600 transition-colors">
                        <ThumbsUp size={12} /> Helpful
                    </button>
                </div>
            </CardContent>
        </Card>
    )
}
