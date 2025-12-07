'use client'

import React from 'react'
import Link from 'next/link'
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ArrowLeft, Download, Filter, MoreHorizontal } from 'lucide-react'

const orders = [
    {
        id: "#ORD-7829",
        date: "Today, 10:23 AM",
        items: "Ethiopia Yirgacheffe (200g)",
        customer: "Alice M.",
        status: "Processing",
        total: "₩ 24,000",
        method: "Credit Card"
    },
    {
        id: "#ORD-7830",
        date: "Yesterday",
        items: "Kenya AA (1kg)",
        customer: "Coffee Lab Ltd.",
        status: "Shipped",
        total: "₩ 110,000",
        method: "Invoice"
    },
    {
        id: "#ORD-7831",
        date: "Oct 24, 2024",
        items: "House Blend (500g)",
        customer: "John Doe",
        status: "Delivered",
        total: "₩ 35,000",
        method: "Paypal"
    },
    {
        id: "#ORD-7832",
        date: "Oct 22, 2024",
        items: "Brazil Santos (200g) x3",
        customer: "Sarah K.",
        status: "Delivered",
        total: "₩ 54,000",
        method: "Credit Card"
    },
    {
        id: "#ORD-7833",
        date: "Oct 20, 2024",
        items: "Decaf Pack",
        customer: "Mike R.",
        status: "Cancelled",
        total: "₩ 22,000",
        method: "Credit Card"
    }
]

export default function OrdersPage() {
    return (
        <div className="min-h-screen bg-latte-50 p-8 md:p-12 font-sans relative">
            {/* Back Nav */}
            <div className="absolute top-4 left-4 z-50">
                <Button asChild variant="ghost" className="text-latte-600 hover:text-latte-900 hover:bg-latte-100/50 transition-colors">
                    <Link href="/design-sample">
                        <ArrowLeft className="mr-2 h-4 w-4" /> Back to Gallery
                    </Link>
                </Button>
            </div>

            <div className="max-w-6xl mx-auto pt-8 space-y-6">
                <div className="flex flex-col md:flex-row justify-between items-end md:items-center gap-4">
                    <div>
                        <h1 className="font-serif text-3xl font-bold text-latte-900">Order History</h1>
                        <p className="text-latte-500 mt-1">Manage recent orders and billing invoices.</p>
                    </div>
                    <div className="flex gap-2">
                        <Select defaultValue="all">
                            <SelectTrigger className="w-[140px] bg-white border-latte-200">
                                <SelectValue placeholder="Status" />
                            </SelectTrigger>
                            <SelectContent className="bg-white">
                                <SelectItem value="all">All Status</SelectItem>
                                <SelectItem value="pending">Pending</SelectItem>
                                <SelectItem value="completed">Completed</SelectItem>
                            </SelectContent>
                        </Select>
                        <Button variant="outline" className="bg-white border-latte-200 text-latte-700">
                            <Filter className="mr-2 h-4 w-4" /> Filter
                        </Button>
                        <Button className="bg-latte-900 text-white hover:bg-latte-800">
                            <Download className="mr-2 h-4 w-4" /> Export CSV
                        </Button>
                    </div>
                </div>

                <Card className="bg-white border-latte-100 shadow-sm overflow-hidden rounded-xl">
                    <CardContent className="p-0">
                        <Table>
                            <TableCaption className="pb-4 text-latte-400">A list of your recent transactions.</TableCaption>
                            <TableHeader className="bg-latte-50/50">
                                <TableRow className="hover:bg-transparent border-latte-100">
                                    <TableHead className="w-[100px] text-latte-800 font-bold">Order ID</TableHead>
                                    <TableHead className="text-latte-600">Date</TableHead>
                                    <TableHead className="text-latte-600">Items</TableHead>
                                    <TableHead className="text-latte-600">Customer</TableHead>
                                    <TableHead className="text-latte-600">Status</TableHead>
                                    <TableHead className="text-right text-latte-800 font-bold">Total</TableHead>
                                    <TableHead></TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {orders.map((order) => (
                                    <TableRow key={order.id} className="border-latte-50 hover:bg-latte-50/30">
                                        <TableCell className="font-medium text-latte-900">{order.id}</TableCell>
                                        <TableCell className="text-latte-500">{order.date}</TableCell>
                                        <TableCell className="text-latte-700 max-w-[200px] truncate" title={order.items}>{order.items}</TableCell>
                                        <TableCell className="text-latte-600">
                                            <div className="flex items-center gap-2">
                                                <div className="w-6 h-6 rounded-full bg-latte-200 text-xs flex items-center justify-center font-bold text-latte-700">
                                                    {order.customer.charAt(0)}
                                                </div>
                                                {order.customer}
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline" className={`border-0 font-medium ${order.status === 'Processing' ? 'bg-blue-50 text-blue-700' :
                                                    order.status === 'Shipped' ? 'bg-orange-50 text-orange-700' :
                                                        order.status === 'Delivered' ? 'bg-green-50 text-green-700' :
                                                            'bg-gray-100 text-gray-500'
                                                }`}>
                                                {order.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right font-mono text-latte-800">{order.total}</TableCell>
                                        <TableCell>
                                            <Button variant="ghost" size="icon" className="h-8 w-8 text-latte-400 hover:text-latte-900">
                                                <MoreHorizontal size={16} />
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
