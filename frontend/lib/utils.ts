import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number | null | undefined): string {
  if (amount === null || amount === undefined) return '0';
  return Math.round(amount).toLocaleString('ko-KR');
}

export function formatWeight(weight: number | string | null | undefined): string {
  if (weight === null || weight === undefined || weight === '') return '0';
  const num = typeof weight === 'string' ? parseFloat(weight) : weight;
  if (isNaN(num)) return '0';

  // 소수점 2자리까지 표시하되, 뒷자리 0은 제거
  // 예: 30.00 -> 30, 30.50 -> 30.5, 30.25 -> 30.25
  return Number(num.toFixed(2)).toString();
}
