import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface InventoryValueTableProps {
    data: {
        bean_name: string
        quantity_kg: number
        avg_price: number
        total_value: number
    }[]
}

export function InventoryValueTable({ data }: InventoryValueTableProps) {
    const totalValue = data.reduce((sum, item) => sum + item.total_value, 0)

    return (
        <Card>
            <CardHeader>
                <CardTitle>재고 자산 가치</CardTitle>
                <CardDescription>
                    현재 보유 재고의 평가액 (FIFO 기준)
                </CardDescription>
            </CardHeader>
            <CardContent>
                <div className="mb-4 text-2xl font-bold">
                    총 자산: ₩{totalValue.toLocaleString()}
                </div>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>품목명</TableHead>
                            <TableHead className="text-right">보유량 (kg)</TableHead>
                            <TableHead className="text-right">평균단가</TableHead>
                            <TableHead className="text-right">평가액</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {data.map((item) => (
                            <TableRow key={item.bean_name}>
                                <TableCell className="font-medium">{item.bean_name}</TableCell>
                                <TableCell className="text-right">{item.quantity_kg.toLocaleString()} kg</TableCell>
                                <TableCell className="text-right">₩{item.avg_price.toLocaleString()}</TableCell>
                                <TableCell className="text-right">₩{item.total_value.toLocaleString()}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
        </Card>
    )
}
