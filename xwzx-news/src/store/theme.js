import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
  state: () => ({
    currentTheme: localStorage.getItem('theme') || 'light', // 默认浅色主题
    themes: {
      light: {
        name: '浅色模式',
        backgroundColor: '#f4f6fa',
        textColor: '#16181d',
        primaryColor: '#1677ff',
        secondaryColor: '#eef1f6',
      },
      dark: {
        name: '深色模式',
        backgroundColor: '#101318',
        textColor: '#f2f4f7',
        primaryColor: '#4c8bf5',
        secondaryColor: '#1b1f26',
      },
      blue: {
        name: '蓝色主题',
        backgroundColor: '#eaf2ff',
        textColor: '#16181d',
        primaryColor: '#1677ff',
        secondaryColor: '#dbe9ff',
      },
      green: {
        name: '绿色主题',
        backgroundColor: '#f1f8f3',
        textColor: '#16181d',
        primaryColor: '#22a06b',
        secondaryColor: '#dcf1e5',
      }
    }
  }),
  
  getters: {
    getCurrentTheme: (state) => state.currentTheme,
    getThemeConfig: (state) => state.themes[state.currentTheme],
    getAllThemes: (state) => Object.keys(state.themes).map(key => ({
      id: key,
      name: state.themes[key].name,
      primaryColor: state.themes[key].primaryColor
    }))
  },
  
  actions: {
    setTheme(themeName) {
      if (this.themes[themeName]) {
        this.currentTheme = themeName;
        localStorage.setItem('theme', themeName);
        this.applyTheme();
      }
    },
    
    applyTheme() {
      const theme = this.themes[this.currentTheme];
      document.documentElement.style.setProperty('--background-color', theme.backgroundColor);
      document.documentElement.style.setProperty('--text-color', theme.textColor);
      document.documentElement.style.setProperty('--primary-color', theme.primaryColor);
      document.documentElement.style.setProperty('--secondary-color', theme.secondaryColor);
    },
    
    initTheme() {
      this.applyTheme();
    }
  }
});