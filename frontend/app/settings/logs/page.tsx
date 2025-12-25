'use client';

import { useEffect, useRef, useState } from 'react';
import { SettingsAPI } from '@/lib/api/settings';
import { Terminal, Pause, Play, Trash2, Server, Globe } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';

type LogType = 'backend' | 'frontend';

export default function LogViewerPage() {
    const [logType, setLogType] = useState<LogType>('backend');
    const [logs, setLogs] = useState<string[]>([]);
    const [isPlaying, setIsPlaying] = useState(true);
    const wsRef = useRef<WebSocket | null>(null);
    const bottomRef = useRef<HTMLDivElement>(null);

    // Clear logs when switching type
    useEffect(() => {
        setLogs([]);
    }, [logType]);

    // Connection Management
    useEffect(() => {
        if (isPlaying) {
            const url = SettingsAPI.getLogWebSocketUrl(logType);
            console.log(`Connecting to ${logType} WS:`, url);

            const ws = new WebSocket(url);
            wsRef.current = ws;

            ws.onopen = () => addLog('SYSTEM', `Connected to ${logType} log stream...`);
            ws.onmessage = (event) => addLog('LOG', event.data);
            ws.onclose = () => addLog('SYSTEM', 'Disconnected from log stream.');
            ws.onerror = (err) => {
                console.error('WS Error', err);
                addLog('ERROR', 'WebSocket Connection Error');
            };

            return () => {
                ws.close();
            };
        }
    }, [isPlaying, logType]);

    // Auto-scroll
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [logs]);

    const addLog = (type: string, content: string) => {
        setLogs((prev) => {
            const newLogs = [...prev, content];
            if (newLogs.length > 1000) return newLogs.slice(-1000); // Keep last 1000
            return newLogs;
        });
    };

    const clearLogs = () => setLogs([]);

    return (
        <div className="space-y-4 h-[calc(100vh-200px)] flex flex-col w-full">
            <div className="flex items-center justify-between">
                <Tabs value={logType} onValueChange={(v) => setLogType(v as LogType)} className="w-full max-w-sm">
                    <TabsList className="grid w-full grid-cols-2 bg-latte-100 p-1">
                        <TabsTrigger value="backend" className="group data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm">
                            <Server className={`w-4 h-4 mr-2 transition-colors ${isPlaying ? 'group-data-[state=active]:text-green-600 group-data-[state=active]:animate-pulse' : 'group-data-[state=active]:text-yellow-600'}`} />
                            Backend
                        </TabsTrigger>
                        <TabsTrigger value="frontend" className="group data-[state=active]:bg-white data-[state=active]:text-latte-900 data-[state=active]:shadow-sm">
                            <Globe className={`w-4 h-4 mr-2 transition-colors ${isPlaying ? 'group-data-[state=active]:text-green-600 group-data-[state=active]:animate-pulse' : 'group-data-[state=active]:text-yellow-600'}`} />
                            Frontend
                        </TabsTrigger>
                    </TabsList>
                </Tabs>
            </div>

            <div className="flex flex-col flex-1 bg-[#1e1e1e] rounded-xl overflow-hidden border border-latte-900 shadow-2xl">
                {/* Toolbar */}
                <div className="bg-[#2d2d2d] px-4 py-2 flex items-center justify-between border-b border-[#3d3d3d]">
                    <div className="flex items-center gap-2 text-gray-400 text-sm font-mono">
                        <Terminal className="w-4 h-4" />
                        <span>logs/themoon_{logType}.log</span>

                        {isPlaying ? (
                            <div className="flex items-center gap-1.5 bg-green-950/30 px-2 py-0.5 rounded text-xs text-green-400 font-bold border border-green-900/50">
                                <span className="relative flex h-2 w-2">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                                </span>
                                LIVE
                            </div>
                        ) : (
                            <div className="flex items-center gap-1.5 bg-yellow-950/30 px-2 py-0.5 rounded text-xs text-yellow-500 font-bold border border-yellow-900/50">
                                <span className="relative flex h-2 w-2">
                                    <span className="relative inline-flex rounded-full h-2 w-2 bg-yellow-500"></span>
                                </span>
                                PAUSED
                            </div>
                        )}
                    </div>

                    <div className="flex items-center gap-2">
                        <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => setIsPlaying(!isPlaying)}
                            className={isPlaying ? 'text-green-400 hover:text-green-300' : 'text-yellow-400 hover:text-yellow-300'}
                        >
                            {isPlaying ? <Pause className="w-4 h-4 mr-1" /> : <Play className="w-4 h-4 mr-1" />}
                            {isPlaying ? 'Pause' : 'Resume'}
                        </Button>
                        <Button
                            size="sm"
                            variant="ghost"
                            onClick={clearLogs}
                            className="text-gray-400 hover:text-white"
                        >
                            <Trash2 className="w-4 h-4 mr-1" /> Clear
                        </Button>
                    </div>
                </div>

                {/* Log Console */}
                <ScrollArea className="flex-1 p-4 font-mono text-sm">
                    <div className="space-y-1">
                        {logs.map((log, i) => (
                            <LogLine key={i} content={log} />
                        ))}
                        {logs.length === 0 && (
                            <div className="text-gray-500 italic text-center mt-10">Waiting for logs...</div>
                        )}
                        <div ref={bottomRef} />
                    </div>
                </ScrollArea>
            </div>
        </div>
    );
}

function LogLine({ content }: { content: string }) {
    // Simple syntax highlighting attempt
    let color = 'text-gray-300';
    if (content.includes('ERROR')) color = 'text-red-400 font-bold';
    else if (content.includes('WARNING') || content.includes('WARN')) color = 'text-amber-400';
    else if (content.includes('INFO')) color = 'text-blue-300';
    else if (content.includes('DEBUG')) color = 'text-gray-500';
    else if (content.includes('Compiling') || content.includes('Compiled')) color = 'text-green-300';

    return (
        <div className={`whitespace-pre-wrap break-all ${color} hover:bg-white/5 py-0.5 px-2 rounded`}>
            {content}
        </div>
    );
}
