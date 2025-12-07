'use client'

import { motion, HTMLMotionProps, Variants } from 'framer-motion'
import React from 'react'

// ============================================================================
// Animation Variants (미니멀 스타일)
// ============================================================================

export const fadeInVariants: Variants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 }
}

export const fadeInUpVariants: Variants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
}

export const fadeInDownVariants: Variants = {
    hidden: { opacity: 0, y: -20 },
    visible: { opacity: 1, y: 0 }
}

export const scaleInVariants: Variants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { opacity: 1, scale: 1 }
}

export const staggerContainerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1,
            delayChildren: 0.1
        }
    }
}

// ============================================================================
// FadeIn Component - 기본 페이드인 애니메이션
// ============================================================================

interface FadeInProps extends HTMLMotionProps<'div'> {
    children: React.ReactNode
    direction?: 'up' | 'down' | 'none'
    delay?: number
    duration?: number
    className?: string
}

export function FadeIn({
    children,
    direction = 'up',
    delay = 0,
    duration = 0.5,
    className = '',
    ...props
}: FadeInProps) {
    const variants = direction === 'up'
        ? fadeInUpVariants
        : direction === 'down'
            ? fadeInDownVariants
            : fadeInVariants

    return (
        <motion.div
            initial="hidden"
            animate="visible"
            variants={variants}
            transition={{ duration, delay, ease: 'easeOut' }}
            className={className}
            {...props}
        >
            {children}
        </motion.div>
    )
}

// ============================================================================
// FadeInView Component - 뷰포트에 들어올 때 애니메이션
// ============================================================================

interface FadeInViewProps extends HTMLMotionProps<'div'> {
    children: React.ReactNode
    direction?: 'up' | 'down' | 'none'
    delay?: number
    duration?: number
    className?: string
    once?: boolean
}

export function FadeInView({
    children,
    direction = 'up',
    delay = 0,
    duration = 0.5,
    className = '',
    once = true,
    ...props
}: FadeInViewProps) {
    const variants = direction === 'up'
        ? fadeInUpVariants
        : direction === 'down'
            ? fadeInDownVariants
            : fadeInVariants

    return (
        <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once, margin: '-50px' }}
            variants={variants}
            transition={{ duration, delay, ease: 'easeOut' }}
            className={className}
            {...props}
        >
            {children}
        </motion.div>
    )
}

// ============================================================================
// AnimatedCard Component - 카드용 애니메이션 래퍼
// ============================================================================

interface AnimatedCardProps extends HTMLMotionProps<'div'> {
    children: React.ReactNode
    index?: number
    className?: string
}

export function AnimatedCard({
    children,
    index = 0,
    className = '',
    ...props
}: AnimatedCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
                duration: 0.4,
                delay: index * 0.1,
                ease: 'easeOut'
            }}
            className={className}
            {...props}
        >
            {children}
        </motion.div>
    )
}

// ============================================================================
// StaggerContainer Component - 자식 요소 순차적 애니메이션 컨테이너
// ============================================================================

interface StaggerContainerProps extends HTMLMotionProps<'div'> {
    children: React.ReactNode
    className?: string
    staggerDelay?: number
}

export function StaggerContainer({
    children,
    className = '',
    staggerDelay = 0.1,
    ...props
}: StaggerContainerProps) {
    return (
        <motion.div
            initial="hidden"
            animate="visible"
            variants={{
                hidden: { opacity: 0 },
                visible: {
                    opacity: 1,
                    transition: {
                        staggerChildren: staggerDelay,
                        delayChildren: 0.1
                    }
                }
            }}
            className={className}
            {...props}
        >
            {children}
        </motion.div>
    )
}

// ============================================================================
// StaggerItem Component - StaggerContainer 내부 아이템
// ============================================================================

interface StaggerItemProps extends HTMLMotionProps<'div'> {
    children: React.ReactNode
    className?: string
}

export function StaggerItem({
    children,
    className = '',
    ...props
}: StaggerItemProps) {
    return (
        <motion.div
            variants={fadeInUpVariants}
            transition={{ duration: 0.4, ease: 'easeOut' }}
            className={className}
            {...props}
        >
            {children}
        </motion.div>
    )
}

// ============================================================================
// PageTransition Component - 페이지 전체 전환 애니메이션
// ============================================================================

interface PageTransitionProps {
    children: React.ReactNode
    className?: string
}

export function PageTransition({ children, className = '' }: PageTransitionProps) {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4, ease: 'easeOut' }}
            className={className}
        >
            {children}
        </motion.div>
    )
}

// ============================================================================
// MotionDiv Export - 기본 motion.div 재내보내기
// ============================================================================

export const MotionDiv = motion.div
export const MotionSpan = motion.span
export const MotionSection = motion.section
