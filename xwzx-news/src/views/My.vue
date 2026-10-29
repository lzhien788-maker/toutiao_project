<template>
  <div class="my-container">
    <van-nav-bar :title="$t('my.title')" />

    <div class="my-hero">
      <span class="hero-orb hero-orb-1"></span>
      <span class="hero-orb hero-orb-2"></span>
      <div class="user-info" @click="goToProfile" v-if="isLogin">
        <div class="avatar">
          <van-image
            round
            width="72"
            height="72"
            src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
          />
        </div>
        <div class="info">
          <div class="username">{{ isLogin && userInfo ? userInfo.username : $t('my.notLoggedIn') }}</div>
          <div class="desc" v-if="isLogin">{{ userBio || $t('profile.bio') }}</div>
        </div>
        <van-icon name="arrow" class="arrow-icon" />
      </div>
      <div class="user-info" v-else>
        <div class="avatar">
          <van-image
            round
            width="72"
            height="72"
            src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
          />
        </div>
        <div class="info">
          <div class="username">{{ $t('my.notLoggedIn') }}</div>
          <div class="desc desc-actions">
            <van-button type="primary" size="small" @click="goToLogin">{{ $t('my.goToLogin') }}</van-button>
            <van-button type="default" size="small" @click="goToRegister">{{ $t('my.goToRegister') }}</van-button>
          </div>
        </div>
      </div>
    </div>

    <div class="stats-card">
      <div class="stat-item">
        <span class="stat-num">{{ favoriteCount }}</span>
        <span class="stat-label">我的收藏</span>
      </div>
      <span class="stat-divider"></span>
      <div class="stat-item">
        <span class="stat-num">{{ historyCount }}</span>
        <span class="stat-label">浏览历史</span>
      </div>
      <span class="stat-divider"></span>
      <div class="stat-item">
        <span class="stat-num">{{ categoryCount }}</span>
        <span class="stat-label">新闻栏目</span>
      </div>
    </div>

    <div class="menu-list">
      <div class="section-title">{{ $t('my.title') }}</div>
      <div class="menu-card">
        <van-cell :title="$t('my.myFavorite')" is-link @click="goToFavorite">
          <template #icon>
            <span class="menu-icon menu-icon-blue"><van-icon name="star-o" /></span>
          </template>
        </van-cell>
        <van-cell :title="$t('my.browsingHistory')" is-link @click="goToHistory">
          <template #icon>
            <span class="menu-icon menu-icon-cyan"><van-icon name="clock-o" /></span>
          </template>
        </van-cell>
        <van-cell :title="$t('my.notifications')" is-link>
          <template #icon>
            <span class="menu-icon menu-icon-orange"><van-icon name="bell" /></span>
          </template>
        </van-cell>
        <van-cell :title="$t('my.settings')" is-link @click="goToSettings">
          <template #icon>
            <span class="menu-icon menu-icon-violet"><van-icon name="setting-o" /></span>
          </template>
        </van-cell>
        <van-cell v-if="isLogin" :title="$t('my.logout')" @click="handleLogout" class="logout-cell">
          <template #icon>
            <span class="menu-icon menu-icon-red"><van-icon name="cross" /></span>
          </template>
        </van-cell>
      </div>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useUserStore } from '../store/user';
import { useNewsStore } from '../store/modules/news';
import { useFavoriteStore } from '../store/modules/favorite';
import { useHistoryStore } from '../store/modules/history';
import { useRouter } from 'vue-router';
import { showDialog, showToast } from 'vant';
import TabBar from '../components/TabBar.vue';
import { useI18n } from 'vue-i18n';

const userStore = useUserStore();
const newsStore = useNewsStore();
const favoriteStore = useFavoriteStore();
const historyStore = useHistoryStore();
const router = useRouter();
const { t } = useI18n();

const userInfo = computed(() => userStore.userInfo);
const isLogin = computed(() => userStore.getLoginStatus);
const userBio = computed(() => userStore.getUserBio || t('profile.bio'));
const favoriteCount = computed(() => (favoriteStore.getFavorites || []).length);
const historyCount = computed(() => (historyStore.getHistory || []).length);
const categoryCount = computed(() => newsStore.categories.length);

const goToLogin = () => {
  router.push('/login');
};

const goToRegister = () => {
  router.push('/register');
};

const goToProfile = () => {
  if (isLogin.value) {
    router.push('/profile');
  }
};

const goToHistory = () => {
  if (isLogin.value) {
    router.push('/history');
  } else {
    showToast(t('common.login'));
    router.push('/login');
  }
};

const goToFavorite = () => {
  if (isLogin.value) {
    router.push('/favorite');
  } else {
    showToast(t('common.login'));
    router.push('/login');
  }
};

const goToSettings = () => {
  router.push('/settings');
};

const handleLogout = () => {
  showDialog({
    title: t('common.confirm'),
    message: t('my.logout') + '?',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      userStore.logout();
      router.push('/login');
    }
  });
};

onMounted(async () => {
  try {
    await userStore.getUserInfoDetail();
  } catch (error) {
    console.error('获取用户信息失败:', error);
  }
});
</script>

<style scoped>
.my-container {
  padding-bottom: 60px;
  background-color: var(--app-bg);
  color: var(--app-text-1);
  min-height: 100vh;
  box-sizing: border-box;
}

.van-nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
  background-color: transparent;
  box-shadow: none;
}

:deep(.van-nav-bar__title) {
  color: #fff;
  font-weight: 700;
}

:deep(.van-nav-bar__left),
:deep(.van-nav-bar__right) {
  color: #fff;
}

.my-hero {
  position: relative;
  padding: 62px 18px 42px;
  background: var(--app-header-gradient);
  border-radius: 0 0 26px 26px;
  overflow: hidden;
  box-shadow: 0 12px 26px rgba(22, 119, 255, 0.22);
}

.hero-orb {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.14);
}

.hero-orb-1 {
  width: 170px;
  height: 170px;
  top: -80px;
  right: -40px;
}

.hero-orb-2 {
  width: 96px;
  height: 96px;
  bottom: -46px;
  left: 40px;
  background: rgba(255, 255, 255, 0.1);
}

.user-info {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
}

.avatar {
  margin-right: 14px;
  padding: 3px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.35);
  box-shadow: 0 6px 18px rgba(8, 40, 90, 0.22);
}

.avatar :deep(.van-image) {
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.9);
}

.info {
  flex: 1;
  min-width: 0;
}

.username {
  font-size: 19px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

.desc {
  margin-top: 5px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.82);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.desc-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.desc-actions :deep(.van-button) {
  border-radius: 999px;
  padding: 0 16px;
}

.desc-actions :deep(.van-button--default) {
  background: rgba(255, 255, 255, 0.18);
  border-color: rgba(255, 255, 255, 0.5);
  color: #fff;
}

.arrow-icon {
  color: rgba(255, 255, 255, 0.85);
  font-size: 18px;
}

.stats-card {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  margin: -28px 16px 0;
  padding: 16px 8px;
  background-color: var(--app-surface);
  border-radius: var(--app-radius);
  box-shadow: var(--app-shadow-3);
}

.stat-item {
  flex: 1;
  text-align: center;
}

.stat-num {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: var(--app-text-1);
  line-height: 1.3;
}

.stat-label {
  display: block;
  margin-top: 2px;
  font-size: 12px;
  color: var(--app-text-3);
}

.stat-divider {
  width: 1px;
  height: 26px;
  background-color: var(--app-line);
}

.menu-list {
  margin: 22px 16px 0;
}

.section-title {
  margin-bottom: 10px;
}

.menu-card {
  background-color: var(--app-surface);
  border-radius: var(--app-radius);
  box-shadow: var(--app-shadow-2);
  overflow: hidden;
}

.menu-card :deep(.van-cell) {
  padding-top: 14px;
  padding-bottom: 14px;
}

.menu-card :deep(.van-cell::after) {
  left: 56px;
}

.menu-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  margin-right: 10px;
  border-radius: 10px;
  font-size: 17px;
}

.menu-icon-blue {
  color: #1677ff;
  background: rgba(22, 119, 255, 0.1);
}

.menu-icon-cyan {
  color: #00b7c3;
  background: rgba(0, 183, 195, 0.12);
}

.menu-icon-orange {
  color: #ff9500;
  background: rgba(255, 149, 0, 0.12);
}

.menu-icon-violet {
  color: #7c5cff;
  background: rgba(124, 92, 255, 0.12);
}

.menu-icon-red {
  color: #f04b4b;
  background: rgba(240, 75, 75, 0.1);
}

.logout-cell :deep(.van-cell__title) {
  color: #f04b4b;
}
</style>
