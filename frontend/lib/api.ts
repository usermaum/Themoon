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
  notes?: string
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
  quantity_kg: number
  avg_price?: number
}

// --- Roasting Types ---

export interface SingleOriginRoastingRequest {
  green_bean_id: number
  input_weight: number
  output_weight: number
  roast_profile: RoastProfile
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
  }) => {
    const response = await api.get<Bean[]>('/api/v1/beans', { params })
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
}

// --- Roasting API ---

export const RoastingAPI = {
  roastSingleOrigin: async (data: SingleOriginRoastingRequest) => {
    const response = await api.post<RoastingResponse>('/api/v1/roasting/single-origin', data)
    return response.data
  }
}
