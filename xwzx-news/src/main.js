import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './store'
import axios from 'axios'
import { useUserStore } from './store/user'

// 导入Vant组件库
import { 
  Button, 
  NavBar, 
  Tabbar, 
  TabbarItem, 
  Tab, 
  Tabs, 
  List, 
  PullRefresh, 
  Cell, 
  CellGroup,
  Grid,
  GridItem,
  Empty,
  Form,
  Field,
  Image,
  Toast,
  Icon,
  Popup
} from 'vant'

// 导入Vant样式
import 'vant/lib/index.css'

// 导入全局样式
import './style.css'

// 引入国际化
import { setupI18n } from './i18n'

const app = createApp(App)

// 设置i18n
const i18n = setupI18n()
app.use(i18n)

// 注册Vant组件
app.use(Button)
app.use(NavBar)
app.use(Tabbar)
app.use(TabbarItem)
app.use(Tab)
app.use(Tabs)
app.use(List)
app.use(PullRefresh)
app.use(Cell)
app.use(CellGroup)
app.use(Grid)
app.use(GridItem)
app.use(Empty)
app.use(Form)
app.use(Field)
app.use(Image)
app.use(Toast)
app.use(Icon)
app.use(Popup)

// 使用路由和状态管理
app.use(router)
app.use(pinia)

// ==================== axios 全局拦截器 ====================

// pinia-plugin-persistedstate 把 user-store 这个 store 存在 localStorage 里
const USER_STORE_KEY = 'user-store'

// 从 localStorage 里读 token（拦截器里不能直接用 store，所以读持久化数据）
function getToken() {
  try {
    const raw = localStorage.getItem(USER_STORE_KEY)
    if (!raw) return ''
    return JSON.parse(raw)?.token || ''
  } catch (e) {
    return ''
  }
}

// 请求拦截器：每次请求自动带上 token，不用每个页面手动写 Authorization 头
axios.interceptors.request.use(
  config => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器：401 说明 token 失效/过期，清掉登录态并跳回登录页
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // 1. 清掉本地登录信息
      localStorage.removeItem(USER_STORE_KEY)
      const userStore = useUserStore(pinia)
      userStore.logout()
      // 2. 跳转到登录页
      if (router.currentRoute.value.path !== '/login') {
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

app.mount('#app')

// 初始化主题
import { useThemeStore } from './store/theme'
const themeStore = useThemeStore()
themeStore.initTheme()
