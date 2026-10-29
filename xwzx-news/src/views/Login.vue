<template>
  <div class="login-page">
    <span class="page-orb page-orb-1"></span>
    <span class="page-orb page-orb-2"></span>
    <span class="page-orb page-orb-3"></span>

    <van-nav-bar
      title="用户登录"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />

    <div class="login-container">
      <div class="login-brand">
        <div class="brand-logo">
          <van-image
            width="64"
            height="64"
            src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
            round
          />
        </div>
        <h2 class="brand-title">新闻资讯</h2>
        <p class="brand-sub">登录后同步收藏与浏览记录，随时随地读好新闻</p>
      </div>

      <div class="login-card">
        <van-form @submit="onSubmit" class="login-form">
          <van-cell-group>
            <van-field
              v-model="username"
              name="username"
              label="用户名"
              placeholder="请输入用户名"
              :rules="[{ required: true, message: '请填写用户名' }]"
            />
            <van-field
              v-model="password"
              type="password"
              name="password"
              label="密码"
              placeholder="请输入密码"
              :rules="[{ required: true, message: '请填写密码' }]"
            />
          </van-cell-group>

          <div class="submit-btn">
            <van-button round block type="primary" native-type="submit" size="large">
              登录
            </van-button>
          </div>

          <div class="login-tips">
            <van-icon name="info-o" class="tips-icon" />
            <p>测试账号：admin</p>
            <p>测试密码：123456</p>
          </div>
        </van-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { useUserStore } from '../store/user';

const router = useRouter();
const userStore = useUserStore();

const username = ref('');
const password = ref('');

const onSubmit = async (values) => {
  showToast({
    type: 'loading',
    message: '登录中...',
    forbidClick: true,
    duration: 0
  });

  try {
    const result = await userStore.login({
      username: username.value,
      password: password.value
    });

    if (result.success) {
      showToast({
        type: 'success',
        message: result.message
      });

      router.push('/');
    } else {
      showToast({
        type: 'fail',
        message: result.message
      });
    }
  } catch (error) {
    showToast({
      type: 'fail',
      message: '登录失败，请稍后再试'
    });
  }
};

const onClickLeft = () => {
  router.back();
};
</script>

<style scoped>
.login-page {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(165deg, #1677ff 0%, #0d5ad8 48%, #0a3f9e 100%);
  overflow-x: hidden;
}

.page-orb {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
}

.page-orb-1 {
  width: 260px;
  height: 260px;
  top: -90px;
  right: -90px;
}

.page-orb-2 {
  width: 180px;
  height: 180px;
  top: 220px;
  left: -70px;
  background: rgba(255, 255, 255, 0.06);
}

.page-orb-3 {
  width: 220px;
  height: 220px;
  bottom: -80px;
  right: -40px;
  background: rgba(255, 255, 255, 0.05);
}

:deep(.van-nav-bar) {
  background-color: transparent;
}

:deep(.van-nav-bar__title) {
  color: #fff;
  font-weight: 600;
}

:deep(.van-nav-bar__left),
:deep(.van-nav-bar__right) {
  color: #fff;
}

:deep(.van-nav-bar__left .van-icon) {
  color: #fff;
}

.login-container {
  position: relative;
  z-index: 1;
  padding: 76px 18px 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-brand {
  text-align: center;
  margin-bottom: 26px;
}

.brand-logo {
  display: inline-flex;
  padding: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.22);
  box-shadow: 0 12px 30px rgba(4, 26, 70, 0.28);
}

.brand-logo :deep(.van-image) {
  border: 2px solid rgba(255, 255, 255, 0.85);
}

.brand-title {
  margin: 16px 0 0;
  color: #fff;
  font-size: 26px;
  font-weight: 700;
  letter-spacing: 3px;
}

.brand-sub {
  margin: 8px 0 0;
  color: rgba(255, 255, 255, 0.78);
  font-size: 13px;
  line-height: 1.6;
}

.login-card {
  width: 100%;
  max-width: 420px;
  padding: 22px 18px 18px;
  background: rgba(255, 255, 255, 0.97);
  border-radius: var(--app-radius-lg);
  box-shadow: 0 20px 48px rgba(4, 26, 70, 0.3);
}

.login-form {
  width: 100%;
}

.login-form :deep(.van-cell-group) {
  background: transparent;
}

.login-form :deep(.van-field) {
  margin-bottom: 12px;
  padding: 12px 14px;
  border-radius: 12px;
  background-color: #f4f6fa;
  border: 1px solid transparent;
  transition: border-color 0.25s ease, background-color 0.25s ease;
}

.login-form :deep(.van-field:focus-within) {
  background-color: #fff;
  border-color: var(--app-primary);
}

.login-form :deep(.van-field__label) {
  width: 56px;
  color: var(--app-text-2);
  font-weight: 500;
}

.login-form :deep(.van-field__control) {
  font-size: 15px;
}

.submit-btn {
  margin-top: 22px;
}

.submit-btn :deep(.van-button) {
  box-shadow: var(--app-shadow-primary);
  letter-spacing: 4px;
}

.login-tips {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px 6px;
  justify-content: center;
  margin-top: 18px;
  padding: 10px 12px;
  border-radius: 12px;
  background-color: var(--app-gradient-soft);
  color: var(--app-text-2);
  font-size: 12px;
}

.login-tips p {
  margin: 0;
}

.tips-icon {
  color: var(--app-primary);
  font-size: 15px;
}
</style>
