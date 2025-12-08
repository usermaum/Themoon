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
  // Render.com 슬립 모드 대응: 첫 요청은 최대 60초까지 대기
  timeout: 60000, // 60초
})

// 요청 인터셉터 (인증 토큰 추가 - 미사용 시에도 구조 유지)
// api.interceptors.request.use(...)

// 응답 인터셉터
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // 에러 처리 로직
    return Promise.reject(error)
  }
)

export default api

// --- Types ---

export type BeanType = 'GREEN_BEAN' | 'ROASTED_BEAN' | 'BLEND_BEAN'
export type RoastProfile = 'LIGHT' | 'MEDIUM' | 'DARK'

export interface Bean {
  id: number
  name: string
  type: BeanType
  sku?: string

  // 생두 정보
  origin?: string
  variety?: string
  grade?: string
  processing_method?: string

  // 원두 정보
  roast_profile?: RoastProfile
  parent_bean_id?: number

  // 재고 및 가격
  quantity_kg: number
  avg_price: number
  purchase_price_per_kg?: number
  cost_price?: number

  // 메타
  description?: string
  // Missing properties added to fix lint errors
  roast_level?: string
  purchase_date?: string
  notes?: string
  expected_loss_rate?: number
  created_at: string
  updated_at?: string
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
  type: BeanType
  origin?: string
  variety?: string
  grade?: string
  processing_method?: string
  roast_profile?: RoastProfile
  // Missing properties added to fix lint errors
  roast_level?: string
  purchase_date?: string
  purchase_price_per_kg?: number
  quantity_kg: number
  notes?: string
  avg_price?: number
}

// --- Blend Types ---

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

// --- Roasting Types ---

export interface SingleOriginRoastingRequest {
  green_bean_id: number
  input_weight: number
  output_weight: number
  roast_profile: RoastProfile
  notes?: string
}

export interface BlendRoastingRequest {
  blend_id: number
  output_weight: number
  input_weight?: number
  notes?: string
}

export interface RoastingResponse {
  success: boolean
  message: string
  roasted_bean: Bean
  loss_rate_percent: number
  production_cost: number
}

// --- Bean API ---

export const BeanAPI = {
  getAll: async (params?: {
    skip?: number
    limit?: number
    search?: string
    type?: string[]
  }) => {
    // Backend expects: page, size, search, type
    // Convert skip/limit to page/size
    const limitVal = params?.limit || 10
    const skipVal = params?.skip || 0
    const page = Math.floor(skipVal / limitVal) + 1

    // Construct query params manually to handle array correctly if needed, or axios handles it?
    // Axios handles array as type[]=A&type[]=B by default or comma?
    // FastAPI expects type=A&type=B (repeat). Axios default is 'brackets' (type[]=A).
    // We need 'repeat' (type=A&type=B).
    // Use paramsSerializer.

    const queryParams: any = {
      page,
      size: limitVal,
    }

    if (params?.search) queryParams.search = params.search
    if (params?.type) queryParams.type = params.type

    const response = await api.get<BeanListResponse>('/api/v1/beans/', {
      params: queryParams,
      paramsSerializer: (params) => {
        const searchParams = new URLSearchParams()
        if (params.page) searchParams.append('page', params.page.toString())
        if (params.size) searchParams.append('size', params.size.toString())
        if (params.search) searchParams.append('search', params.search)
        if (params.type && Array.isArray(params.type)) {
          params.type.forEach((t: string) => searchParams.append('type', t))
        }
        return searchParams.toString()
      }
    })
    return response.data
  },

  getOne: async (id: number) => {
    const response = await api.get<Bean>(`/api/v1/beans/${id}`)
    return response.data
  },

  create: async (data: BeanCreateData) => {
    const response = await api.post<Bean>('/api/v1/beans/', data)
    return response.data
  },

  delete: async (id: number) => {
    const response = await api.delete(`/api/v1/beans/${id}`)
    return response.data
  },

  update: async (id: number, data: Partial<BeanCreateData>) => {
    const response = await api.put<Bean>(`/api/v1/beans/${id}`, data)
    return response.data
  },
}

// --- Roasting API ---

export const RoastingAPI = {
  roastSingleOrigin: async (data: SingleOriginRoastingRequest) => {
    const response = await api.post<RoastingResponse>('/api/v1/roasting/single-origin', data)
    return response.data
  },

  roastBlend: async (data: BlendRoastingRequest) => {
    const response = await api.post<RoastingResponse>('/api/v1/roasting/blend', data)
    return response.data
  }
}

// --- Blend API ---

export const BlendAPI = {
  getAll: async (params?: {
    skip?: number
    limit?: number
    search?: string
  }) => {
    const response = await api.get<Blend[]>('/api/v1/blends/', { params })
    return response.data
  },

  getOne: async (id: number) => {
    const response = await api.get<Blend>(`/api/v1/blends/${id}`)
    return response.data
  },

  create: async (data: BlendCreateData) => {
    const response = await api.post<Blend>('/api/v1/blends/', data)
    return response.data
  },

  update: async (id: number, data: Partial<BlendCreateData>) => {
    const response = await api.put<Blend>(`/api/v1/blends/${id}`, data)
    return response.data
  },

  delete: async (id: number) => {
    const response = await api.delete(`/api/v1/blends/${id}`)
    return response.data
  },
}

// --- Inventory Types ---

export interface InventoryLog {
  id: number
  bean_id: number
  change_type: string  // "PURCHASE", "ROASTING_INPUT", "ROASTING_OUTPUT", "SALES", "LOSS", "ADJUSTMENT", "BLENDING_INPUT"
  change_amount: number  // +: 증가, -: 감소
  current_quantity: number
  notes?: string
  created_at: string
}

export interface InventoryLogCreateData {
  bean_id: number
  change_type: string
  change_amount: number
  notes?: string
}

// --- Inventory API ---

export const InventoryLogAPI = {
  getAll: async (params?: { bean_id?: number; skip?: number; limit?: number }) => {
    const response = await api.get<InventoryLog[]>('/api/v1/inventory-logs/', { params })
    return response.data
  },

  create: async (data: InventoryLogCreateData) => {
    const response = await api.post<InventoryLog>('/api/v1/inventory-logs/', data)
    return response.data
  },

  update: async (id: number, change_amount: number, notes?: string) => {
    const response = await api.put<InventoryLog>(`/api/v1/inventory-logs/${id}`, null, {
      params: { change_amount, notes }
    })
    return response.data
  },

  delete: async (id: number) => {
    await api.delete(`/api/v1/inventory-logs/${id}`)
  },

  getByBeanId: async (beanId: number) => {
    const response = await api.get<InventoryLog[]>('/api/v1/inventory-logs/', { params: { bean_id: beanId } })
    return response.data
  }
}
