<template>
  <div class="settings-container">
    <van-nav-bar
      :title="$t('settings.title')"
      left-arrow
      fixed
      @click-left="onClickLeft"
    />

    <div class="settings-hero">
      <span class="hero-orb hero-orb-1"></span>
      <span class="hero-orb hero-orb-2"></span>
      <div class="hero-icon"><van-icon name="setting-o" /></div>
      <div class="hero-title">个性化你的阅读体验</div>
      <div class="hero-desc">主题、语言与账号偏好都可以在这里调整</div>
    </div>

    <div class="settings-list">
      <div class="settings-block">
        <div class="section-title">{{ $t('settings.personalization') }}</div>
        <div class="app-card">
          <van-cell
            :title="$t('settings.themeCustomization')"
            icon="paint-o"
            is-link
            @click="showThemePopup = true"
          >
            <template #value>
              <span class="cell-value">
                <span class="value-dot" :style="{ backgroundColor: currentThemeColor }"></span>
                {{ currentThemeName }}
              </span>
            </template>
          </van-cell>
          <van-cell
            :title="$t('settings.languageSettings')"
            icon="exchange"
            is-link
            @click="showLanguagePopup = true"
          >
            <template #value>
              <span class="cell-value">{{ currentLanguageLabel }}</span>
            </template>
          </van-cell>
        </div>
      </div>

      <div class="settings-block">
        <div class="section-title">{{ $t('settings.account') }}</div>
        <div class="app-card">
          <van-cell
            :title="$t('settings.privacySettings')"
            icon="shield-o"
            is-link
          />
          <van-cell
            :title="$t('settings.notificationSettings')"
            icon="bell"
            is-link
          />
          <van-cell
            :title="$t('settings.aboutUs')"
            icon="info-o"
            is-link
          >
            <template #value>
              <span class="cell-value">v1.0.0</span>
            </template>
          </van-cell>
        </div>
      </div>
    </div>

    <van-popup
      v-model:show="showThemePopup"
      position="bottom"
      round
      :style="{ height: '46%', paddingBottom: '20px' }"
    >
      <div class="popup-handle"></div>
      <div class="popup-title">{{ $t('settings.selectTheme') }}</div>
      <div class="popup-subtitle">挑选一款符合你审美的配色方案</div>
      <div class="theme-list">
        <div
          v-for="theme in themeList"
          :key="theme.id"
          class="theme-item"
          :class="{ active: currentTheme === theme.id }"
          @click="changeTheme(theme.id)"
        >
          <div class="theme-preview" :style="{ background: theme.primaryColor }">
            <span class="theme-check" v-if="currentTheme === theme.id">
              <van-icon name="success" />
            </span>
          </div>
          <div class="theme-name">{{ theme.name }}</div>
        </div>
      </div>
    </van-popup>

    <van-popup
      v-model:show="showLanguagePopup"
      position="bottom"
      round
      :style="{ height: '46%', paddingBottom: '20px' }"
    >
      <div class="popup-handle"></div>
      <div class="popup-title">{{ $t('settings.selectLanguage') }}</div>
      <div class="popup-subtitle">切换后界面文案会同步更新</div>
      <div class="language-list">
        <div
          v-for="lang in languageOptions"
          :key="lang.value"
          class="language-item"
          :class="{ active: currentLanguage === lang.value }"
          @click="currentLanguage = lang.value"
        >
          <span class="language-flag">{{ lang.value === 'zh-CN' ? '中' : 'EN' }}</span>
          <span class="language-label">{{ lang.label }}</span>
          <van-icon v-if="currentLanguage === lang.value" name="success" class="language-check" />
        </div>
      </div>
      <div class="popup-footer">
        <van-button type="primary" block @click="changeLanguage">{{ $t('common.confirm') }}</van-button>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { useThemeStore } from '../store/theme';
import { useI18n } from 'vue-i18n';
import { useLanguageStore } from '../store/language';

const router = useRouter();
const themeStore = useThemeStore();
const languageStore = useLanguageStore();
const { t, locale } = useI18n();

// 返回上一页
const onClickLeft = () => {
  router.back();
};

// 主题相关
const showThemePopup = ref(false);
const themeList = computed(() => themeStore.getAllThemes);
const currentTheme = computed(() => themeStore.getCurrentTheme);
const currentThemeName = computed(() => {
  const found = themeList.value.find(item => item.id === currentTheme.value);
  return found ? found.name : '';
});
const currentThemeColor = computed(() => {
  const found = themeList.value.find(item => item.id === currentTheme.value);
  return found ? found.primaryColor : '#1677ff';
});

// 切换主题
const changeTheme = (themeId) => {
  themeStore.setTheme(themeId);
  showToast(t('settings.themeChanged'));
  showThemePopup.value = false;
};

// 语言相关
const showLanguagePopup = ref(false);
const currentLanguage = ref(languageStore.getCurrentLanguage);
const languageOptions = [
  { label: '简体中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' }
];
const currentLanguageLabel = computed(() => {
  const found = languageOptions.find(item => item.value === currentLanguage.value);
  return found ? found.label : '';
});

// 切换语言
const changeLanguage = () => {
  languageStore.setLanguage(currentLanguage.value);
  locale.value = currentLanguage.value;
  showLanguagePopup.value = false;
  showToast(t('settings.languageChanged'));
  // 强制刷新页面以应用语言更改
  window.location.reload();
};
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  background-color: var(--app-bg);
  color: var(--app-text-1);
  padding-top: 46px;
  padding-bottom: 30px;
}

:deep(.van-nav-bar) {
  background: var(--app-header-solid);
  box-shadow: none;
}

:deep(.van-nav-bar__title),
:deep(.van-nav-bar__left) {
  color: #fff;
}

:deep(.van-nav-bar__left .van-icon) {
  color: #fff;
}

.settings-hero {
  position: relative;
  padding: 24px 20px 34px;
  background: var(--app-header-gradient);
  border-radius: 0 0 26px 26px;
  box-shadow: var(--app-shadow-primary);
  overflow: hidden;
}

.hero-orb {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
}

.hero-orb-1 {
  width: 170px;
  height: 170px;
  top: -80px;
  right: -40px;
}

.hero-orb-2 {
  width: 100px;
  height: 100px;
  bottom: -40px;
  right: 60px;
  background: rgba(255, 255, 255, 0.09);
}

.hero-icon {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #fff;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  margin-bottom: 14px;
}

.hero-title {
  font-size: 21px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

.hero-desc {
  margin-top: 7px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.82);
}

.settings-list {
  margin-top: 18px;
  padding: 0 12px;
}

.settings-block {
  margin-bottom: 22px;
}

.settings-block .section-title {
  padding: 0 4px 12px;
}

.settings-block .app-card {
  margin-top: 0;
}

.settings-block .app-card :deep(.van-cell) {
  padding: 15px 16px;
}

.settings-block .app-card :deep(.van-cell::after) {
  left: 16px;
  right: 16px;
}

.settings-block .app-card :deep(.van-cell__left-icon) {
  margin-right: 12px;
  font-size: 19px;
  color: var(--app-primary);
}

.cell-value {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--app-text-3);
}

.value-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.popup-handle {
  width: 38px;
  height: 4px;
  border-radius: 2px;
  background-color: #e3e6eb;
  margin: 10px auto 0;
}

.popup-title {
  text-align: center;
  margin-top: 14px;
  font-size: 17px;
  font-weight: 700;
  color: var(--app-text-1);
}

.popup-subtitle {
  text-align: center;
  margin-top: 6px;
  font-size: 12px;
  color: var(--app-text-3);
}

.theme-list {
  display: flex;
  flex-wrap: wrap;
  padding: 22px 16px 0;
}

.theme-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 18px;
  cursor: pointer;
}

.theme-preview {
  position: relative;
  width: 54px;
  height: 54px;
  border-radius: 18px;
  margin-bottom: 10px;
  box-shadow: 0 8px 18px rgba(16, 24, 40, 0.16);
  transition: transform 0.24s cubic-bezier(0.22, 0.61, 0.36, 1), box-shadow 0.24s ease;
}

.theme-item.active .theme-preview {
  transform: scale(1.08);
  box-shadow: 0 10px 22px rgba(16, 24, 40, 0.22);
  outline: 2px solid rgba(22, 119, 255, 0.45);
  outline-offset: 3px;
}

.theme-check {
  position: absolute;
  right: -5px;
  bottom: -5px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #fff;
  background: var(--app-primary);
  border: 2px solid #fff;
}

.theme-name {
  font-size: 12px;
  color: var(--app-text-2);
  text-align: center;
}

.theme-item.active .theme-name {
  color: var(--app-primary);
  font-weight: 600;
}

.language-list {
  padding: 20px 16px 0;
}

.language-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 14px;
  margin-bottom: 10px;
  border-radius: var(--app-radius);
  background-color: #f6f7fa;
  border: 1px solid transparent;
  transition: all 0.24s ease;
}

.language-item.active {
  background-color: var(--app-primary-soft);
  border-color: rgba(22, 119, 255, 0.35);
}

.language-flag {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  background: var(--app-gradient);
}

.language-label {
  flex: 1;
  font-size: 15px;
  color: var(--app-text-1);
}

.language-check {
  font-size: 17px;
  color: var(--app-primary);
}

.popup-footer {
  padding: 18px 16px 0;
}
</style>
