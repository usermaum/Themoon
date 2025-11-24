/**
 * API 클라이언트
 *
 * FastAPI 백엔드와 통신
 */
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 요청 인터셉터 (인증 토큰 추가)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 응답 인터셉터 (에러 처리)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 인증 실패 처리
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// --- Types ---

export interface Bean {
  id: number
  name: string
  origin: string
  variety: string
  processing_method: string
  roast_level: string
  purchase_date: string
  purchase_price_per_kg: number
  quantity_kg: number
  notes?: string
  created_at: string
  updated_at: string
}

export interface BeanListResponse {
  items: Bean[]
  total: number
  page: number
  size: number
  pages: number
}

export interface BeanCreateData {
  name: string
  origin: string
  variety: string
  processing_method: string
  roast_level: string
  purchase_date: string
  purchase_price_per_kg: number
  quantity_kg: number
  notes?: string
}

export interface BeanUpdateData extends Partial<BeanCreateData> { }

// --- Bean API ---

export const BeanAPI = {
  getAll: async (params?: {
    page?: number
    size?: number
    search?: string
    roast_level?: string
  }) => {
    const response = await api.get<BeanListResponse>('/api/v1/beans', { params })
    return response.data
  },

  getOne: async (id: number) => {
    const response = await api.get<Bean>(`/api/v1/beans/${id}`)
    return response.data
  },

  create: async (data: BeanCreateData) => {
    const response = await api.post<Bean>('/api/v1/beans', data)
    return response.data
  },

  update: async (id: number, data: BeanUpdateData) => {
    const response = await api.put<Bean>(`/api/v1/beans/${id}`, data)
    return response.data
  },

  delete: async (id: number) => {
    await api.delete(`/api/v1/beans/${id}`)
  },

  updateQuantity: async (id: number, quantity_change: number) => {
    const response = await api.patch<Bean>(`/api/v1/beans/${id}/quantity`, {
      quantity_change,
    })
    return response.data
  },
}

// --- Types (Blend) ---

export interface BlendRecipeItem {
  bean_id: number
  ratio: number
}

export interface Blend {
  id: number
  name: string
  description?: string
  recipe: BlendRecipeItem[]
  target_roast_level?: string
  notes?: string
  created_at: string
  updated_at?: string
}

export interface BlendCreateData {
  name: string
  description?: string
  recipe: BlendRecipeItem[]
  target_roast_level?: string
  notes?: string
}

export interface BlendUpdateData extends Partial<BlendCreateData> { }

// --- Blend API ---

export const BlendAPI = {
  getAll: async (params?: { skip?: number; limit?: number }) => {
    const response = await api.get<Blend[]>('/api/v1/blends', { params })
    return response.data
  },

  getOne: async (id: number) => {
    const response = await api.get<Blend>(`/api/v1/blends/${id}`)
    return response.data
  },

  create: async (data: BlendCreateData) => {
    const response = await api.post<Blend>('/api/v1/blends', data)
    return response.data
  },

  update: async (id: number, data: BlendUpdateData) => {
    const response = await api.put<Blend>(`/api/v1/blends/${id}`, data)
    return response.data
  },

  delete: async (id: number) => {
    await api.delete(`/api/v1/blends/${id}`)
  },
}

// --- Types (InventoryLog) ---

export interface InventoryLog {
  id: number
  bean_id: number
  transaction_type: 'IN' | 'OUT' | 'ADJUST'
  quantity_change: number
  current_quantity: number
  reason?: string
  created_at: string
}

export interface InventoryLogCreateData {
  bean_id: number
  transaction_type: 'IN' | 'OUT' | 'ADJUST'
  quantity_change: number
  reason?: string
}

// --- InventoryLog API ---

export const InventoryLogAPI = {
  getAll: async (params?: { bean_id?: number; skip?: number; limit?: number }) => {
    const response = await api.get<InventoryLog[]>('/api/v1/inventory-logs', { params })
    return response.data
  },

  create: async (data: InventoryLogCreateData) => {
    const response = await api.post<InventoryLog>('/api/v1/inventory-logs', data)
    return response.data
  },

  update: async (id: number, quantity_change: number, reason?: string) => {
    const response = await api.put<InventoryLog>(`/api/v1/inventory-logs/${id}`, null, {
      params: { quantity_change, reason }
    })
    return response.data
  },

  delete: async (id: number) => {
    await api.delete(`/api/v1/inventory-logs/${id}`)
  },
}
