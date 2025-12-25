import { api, API_BASE_URL } from '../api';

export interface SystemStatus {
    cpu: {
        usage_percent: number;
        status: 'normal' | 'warning' | 'critical';
    };
    memory: {
        usage_percent: number;
        total_gb: number;
        used_gb: number;
    };
    disk: {
        usage_percent: number;
        free_gb: number;
    };
    storage: {
        images_size_mb: number;
    };
}

export interface ImageProcessingConfig {
    to_grayscale: boolean;
    enhance_contrast: boolean;
    contrast_factor: number;
    remove_noise: boolean;
    median_filter_size: number;
    enhance_sharpness: boolean;
    sharpness_factor: number;
    upscale_image: boolean;
    auto_rotate: boolean;
}

export interface OCRConfig {
    _model_priority_rule?: string;
    model_priority: string[];
    prompt_structure: Record<string, any>;
}

export interface SystemInfo {
    version: string;
    last_updated: string;
}

export interface SystemConfig {
    system: SystemInfo;
    image_processing: {
        _comments_guide?: Record<string, string>;
        preprocess_for_ocr: ImageProcessingConfig;
    };
    ocr: OCRConfig;
}

export interface Memo {
    id: number;
    content: string;
    created_at: string;
    status?: 'pending' | 'read' | 'in_progress' | 'done';
    admin_reply?: string;
}

export const SettingsAPI = {
    getSystemStatus: async (): Promise<SystemStatus> => {
        const response = await api.get<SystemStatus>('/api/v1/settings/status');
        return response.data;
    },

    getSystemConfig: async (): Promise<SystemConfig> => {
        const response = await api.get<SystemConfig>('/api/v1/settings/config');
        return response.data;
    },

    updateSystemConfig: async (config: SystemConfig): Promise<SystemConfig> => {
        const response = await api.put<SystemConfig>('/api/v1/settings/config', config);
        return response.data;
    },

    getMemos: async (): Promise<Memo[]> => {
        const response = await api.get<Memo[]>('/api/v1/settings/memos');
        return response.data;
    },

    addMemo: async (content: string): Promise<Memo> => {
        const response = await api.post<Memo>('/api/v1/settings/memos', { content });
        return response.data;
    },

    updateMemo: async (id: number, updates: { status?: string; admin_reply?: string }): Promise<Memo> => {
        const response = await api.put<Memo>(`/api/v1/settings/memos/${id}`, updates);
        return response.data;
    },

    deleteMemo: async (id: number): Promise<void> => {
        await api.delete(`/api/v1/settings/memos/${id}`);
    },


    restartFrontend: async (cleanCache: boolean = true): Promise<{ status: string; message: string }> => {
        const response = await api.post('/api/v1/settings/restart/frontend', null, {
            params: { clean_cache: cleanCache }
        });
        return response.data;
    },

    restartBackend: async (): Promise<{ status: string; message: string }> => {
        const response = await api.post('/api/v1/settings/restart/backend');
        return response.data;
    },

    getLogWebSocketUrl: (logType: 'backend' | 'frontend' = 'backend'): string => {
        // Replace http/https with ws/wss
        const wsBase = API_BASE_URL.replace('http', 'ws');
        // WebSocket URL needs full path
        return `${wsBase}/api/v1/settings/ws/logs?log_type=${logType}`;
    }
};
