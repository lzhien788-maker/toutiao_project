/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // DeepSeek API地址
  // 注意：必须是完整的 chat/completions 路径，
  // 直接 POST 到域名根路径 (https://api.deepseek.com) 会返回 404
  apiEndpoint: 'https://api.deepseek.com/chat/completions',
  
  // API Key (由开发人员指定)
  apiKey: 'sk-a23f73e29bd244228aaea39a71aa9e23',

  // 使用的模型 (deepseek-flash 对应 DeepSeek-V4.1-Flash)
  model: 'deepseek-flash'
}
