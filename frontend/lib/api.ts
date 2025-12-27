/**
 * API 클라이언트
 *
 * FastAPI 백엔드와 통신
 */
import axios from 'axios';

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Render.com 슬립 모드 대응: 첫 요청은 최대 60초까지 대기
  timeout: 60000, // 60초
});

// 요청 인터셉터 (인증 토큰 추가 - 미사용 시에도 구조 유지)
// api.interceptors.request.use(...)

// 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // 에러 처리 로직
    return Promise.reject(error);
  }
);

export default api;

// --- Types ---

export type BeanType = 'GREEN_BEAN' | 'ROASTED_BEAN' | 'BLEND_BEAN';
export type RoastProfile = 'LIGHT' | 'MEDIUM' | 'DARK';

export interface Bean {
  id: number;
  name: string;
  type: BeanType;
  sku?: string;

  // 다국어 정보
  name_ko?: string;
  name_en?: string;

  // 생두 정보
  origin?: string;
  origin_ko?: string;
  origin_en?: string;
  variety?: string;
  grade?: string;
  processing_method?: string;

  // 원두 정보
  roast_profile?: RoastProfile;
  parent_bean_id?: number;

  // 재고 및 가격
  quantity_kg: number;
  avg_price: number;
  purchase_price_per_kg?: number;
  cost_price?: number;

  // 메타
  description?: string;
  // Missing properties added to fix lint errors
  roast_level?: string;
  purchase_date?: string;
  notes?: string;
  expected_loss_rate?: number;
  created_at: string;
  updated_at?: string;
}

export interface BeanListResponse {
  items: Bean[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface BeanCreateData {
  name: string;
  type: BeanType;

  name_ko?: string;
  name_en?: string;

  origin?: string;
  origin_ko?: string;
  origin_en?: string;
  variety?: string;
  grade?: string;
  processing_method?: string;
  roast_profile?: RoastProfile;
  // Missing properties added to fix lint errors
  roast_level?: string;
  purchase_date?: string;
  purchase_price_per_kg?: number;
  quantity_kg: number;
  notes?: string;
  avg_price?: number;
}

// --- Blend Types ---

export interface BlendRecipeItem {
  bean_id: number;
  ratio: number;
}

export interface Blend {
  id: number;
  name: string;
  description?: string;
  recipe: BlendRecipeItem[];
  target_roast_level?: string;
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface BlendCreateData {
  name: string;
  description?: string;
  recipe: BlendRecipeItem[];
  target_roast_level?: string;
  notes?: string;
}

// --- Roasting Types ---

export interface SingleOriginRoastingRequest {
  green_bean_id: number;
  input_weight: number;
  output_weight: number;
  roast_profile: RoastProfile;
  roasting_time?: number;
  ambient_temp?: number;
  humidity?: number;
  notes?: string;
}

export interface BlendRoastingRequest {
  blend_id: number;
  output_weight: number;
  input_weight?: number;
  notes?: string;
}

export interface RoastingHistoryParams {
  skip?: number;
  limit?: number;
  start_date?: string;
  end_date?: string;
  bean_id?: number;
  bean_type?: string;
}

export interface RoastingResponse {
  success: boolean;
  message: string;
  roasted_bean: Bean;
  batch_no?: string;
  loss_rate_percent: number;
  production_cost: number;
}

export interface RoastingLog {
  id: number;
  batch_no: string;
  roast_date: string;
  target_bean_id: number;
  input_weight_total: number;
  output_weight_total: number;
  loss_rate?: number;
  production_cost?: number;

  // Extended Data
  roast_profile?: string; // or RoastProfile
  roasting_time?: number;
  ambient_temp?: number;
  humidity?: number;

  notes?: string;
  created_at: string;
  target_bean?: Bean;
  inventory_logs?: InventoryLog[];
}

export interface RoastingLogDetail extends RoastingLog {
  inventory_logs: InventoryLog[];
}

// --- Bean API ---

export const BeanAPI = {
  getAll: async (params?: {
    skip?: number;
    limit?: number;
    search?: string;
    type?: string[];
    origin?: string;
    exclude_blend?: boolean;
  }) => {
    // Backend expects: page, size, search, type, origin, exclude_blend
    // Convert skip/limit to page/size
    const limitVal = params?.limit || 10;
    const skipVal = params?.skip || 0;
    const page = Math.floor(skipVal / limitVal) + 1;

    const queryParams: any = {
      page,
      size: limitVal,
    };

    if (params?.search) queryParams.search = params.search;
    if (params?.type) queryParams.type = params.type;
    if (params?.origin) queryParams.origin = params.origin;
    if (params?.exclude_blend) queryParams.exclude_blend = params.exclude_blend;

    const response = await api.get<BeanListResponse>('/api/v1/beans/', {
      params: queryParams,
      paramsSerializer: (params) => {
        const searchParams = new URLSearchParams();
        if (params.page) searchParams.append('page', params.page.toString());
        if (params.size) searchParams.append('size', params.size.toString());
        if (params.search) searchParams.append('search', params.search);
        if (params.type && Array.isArray(params.type)) {
          params.type.forEach((t: string) => searchParams.append('type', t));
        }
        if (params.origin) searchParams.append('origin', params.origin);
        if (params.exclude_blend) searchParams.append('exclude_blend', 'true');
        return searchParams.toString();
      },
    });
    return response.data;
  },

  getOne: async (id: number) => {
    const response = await api.get<Bean>(`/api/v1/beans/${id}`);
    return response.data;
  },

  create: async (data: BeanCreateData) => {
    const response = await api.post<Bean>('/api/v1/beans/', data);
    return response.data;
  },

  delete: async (id: number) => {
    const response = await api.delete(`/api/v1/beans/${id}`);
    return response.data;
  },

  update: async (id: number, data: Partial<BeanCreateData>) => {
    const response = await api.put<Bean>(`/api/v1/beans/${id}`, data);
    return response.data;
  },

  checkBatch: async (names: string[]) => {
    const response = await api.post<
      Array<{
        input_name: string;
        status: string;
        bean_id: number | null;
        bean_name: string | null;
      }>
    >('/api/v1/beans/check-batch', names);
    return response.data;
  },
};

// --- Roasting API ---

export const RoastingAPI = {
  roastSingleOrigin: async (data: SingleOriginRoastingRequest) => {
    const response = await api.post<RoastingResponse>('/api/v1/roasting/single-origin', data);
    return response.data;
  },

  roastBlend: async (data: BlendRoastingRequest) => {
    const response = await api.post<RoastingResponse>('/api/v1/roasting/blend', data);
    return response.data;
  },

  getHistory: async (params?: RoastingHistoryParams) => {
    // Manually serialize params to handle bean_id=0 correctly if needed, or rely on standard axios params
    // Adding bean_type to axios params
    const response = await api.get<RoastingLog[]>('/api/v1/roasting/history', {
      params,
      paramsSerializer: (p) => {
        const searchParams = new URLSearchParams();
        if (p.skip !== undefined) searchParams.append('skip', p.skip.toString());
        if (p.limit !== undefined) searchParams.append('limit', p.limit.toString());
        if (p.start_date) searchParams.append('start_date', p.start_date);
        if (p.end_date) searchParams.append('end_date', p.end_date);
        if (p.bean_id !== undefined && p.bean_id !== null) searchParams.append('bean_id', p.bean_id.toString());
        if (p.bean_type) searchParams.append('bean_type', p.bean_type);
        return searchParams.toString();
      }
    });
    return response.data;
  },

  getLog: async (id: number) => {
    const response = await api.get<RoastingLog>(`/api/v1/roasting/${id}`);
    return response.data;
  },
};

// --- Blend API ---

export const BlendAPI = {
  getAll: async (params?: { skip?: number; limit?: number; search?: string }) => {
    const response = await api.get<Blend[]>('/api/v1/blends/', { params });
    return response.data;
  },

  getOne: async (id: number) => {
    const response = await api.get<Blend>(`/api/v1/blends/${id}`);
    return response.data;
  },

  create: async (data: BlendCreateData) => {
    const response = await api.post<Blend>('/api/v1/blends/', data);
    return response.data;
  },

  update: async (id: number, data: Partial<BlendCreateData>) => {
    const response = await api.put<Blend>(`/api/v1/blends/${id}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    const response = await api.delete(`/api/v1/blends/${id}`);
    return response.data;
  },
};

// --- Inventory Types ---

export interface InventoryLog {
  id: number;
  bean_id: number;
  change_type: string; // "PURCHASE", "ROASTING_INPUT", "ROASTING_OUTPUT", "SALES", "LOSS", "ADJUSTMENT", "BLENDING_INPUT"
  change_amount: number; // +: 증가, -: 감소
  current_quantity: number;
  notes?: string;
  created_at: string;
  bean?: {
    name: string;
    id: number;
    name_ko?: string;
    name_en?: string;
    origin_ko?: string;
  };
}

export interface InventoryLogCreateData {
  bean_id: number;
  change_type: string;
  change_amount: number;
  notes?: string;
}

export interface InventoryLogListResponse {
  items: InventoryLog[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// --- Inventory API ---

export const InventoryLogAPI = {
  getAll: async (params?: {
    bean_id?: number;
    skip?: number;
    limit?: number;
    change_type?: string[];
    search?: string;
  }) => {
    // Convert skip/limit to page/size
    const limitVal = params?.limit || 10;
    const skipVal = params?.skip || 0;
    const page = Math.floor(skipVal / limitVal) + 1;

    const queryParams: any = {
      page,
      size: limitVal,
    };

    if (params?.bean_id) queryParams.bean_id = params.bean_id;
    if (params?.change_type) queryParams.change_type = params.change_type;
    if (params?.search) queryParams.search = params.search;

    const response = await api.get<InventoryLogListResponse>('/api/v1/inventory-logs/', {
      params: queryParams,
      paramsSerializer: (params) => {
        const searchParams = new URLSearchParams();
        if (params.page) searchParams.append('page', params.page.toString());
        if (params.size) searchParams.append('size', params.size.toString());
        if (params.bean_id) searchParams.append('bean_id', params.bean_id.toString());
        if (params.change_type && Array.isArray(params.change_type)) {
          params.change_type.forEach((t: string) => searchParams.append('change_type', t));
        }
        if (params.search) searchParams.append('search', params.search);
        return searchParams.toString();
      },
    });
    return response.data;
  },

  create: async (data: InventoryLogCreateData) => {
    const response = await api.post<InventoryLog>('/api/v1/inventory-logs/', data);
    return response.data;
  },

  update: async (id: number, change_amount: number, notes?: string) => {
    const response = await api.put<InventoryLog>(`/api/v1/inventory-logs/${id}`, null, {
      params: { change_amount, notes },
    });
    return response.data;
  },

  delete: async (id: number) => {
    await api.delete(`/api/v1/inventory-logs/${id}`);
  },

  getByBeanId: async (beanId: number) => {
    const response = await api.get<InventoryLog[]>('/api/v1/inventory-logs/', {
      params: { bean_id: beanId },
    });
    return response.data;
  },
};

// --- Dashboard API ---

export interface DashboardStats {
  total_beans: number;
  total_blends: number;
  total_stock_kg: number;
  low_stock_beans: Bean[];
  low_stock_count: number;
}

export const DashboardAPI = {
  getStats: async () => {
    const response = await api.get<DashboardStats>('/api/v1/dashboard/');
    return response.data;
  },
};

export const AnalyticsAPI = {
  getSupplierStats: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/api/v1/analytics/stats/supplier', { params });
    return response.data;
  },

  getInventoryStats: async (params?: { start_date?: string; end_date?: string }) => {
    const response = await api.get('/api/v1/analytics/stats/inventory', { params });
    return response.data;
  },

  getItemTrends: async (params: { bean_name: string; start_date?: string; end_date?: string }) => {
    const response = await api.get('/api/v1/analytics/stats/item/trends', { params });
    return response.data;
  },

  getInventorySummary: async (): Promise<{
    total_weight: number;
    low_stock_count: number;
    active_varieties: number;
  }> => {
    const response = await api.get('/api/v1/analytics/stats/inventory/summary');
    return response.data;
  },
};
