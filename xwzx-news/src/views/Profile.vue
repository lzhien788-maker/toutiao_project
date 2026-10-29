<template>
  <div class="profile-page">
    <van-nav-bar
      title="个人信息"
      left-arrow
      @click-left="$router.back()"
      fixed
    />

    <div class="profile-hero">
      <span class="hero-orb hero-orb-1"></span>
      <span class="hero-orb hero-orb-2"></span>
      <div class="avatar-wrap">
        <van-image
          round
          width="76"
          height="76"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
          class="avatar-img"
        />
      </div>
      <div class="hero-name">{{ userInfo?.username || '未登录用户' }}</div>
      <div class="hero-id">账号 ID: heima-{{ userId || 'N/A' }}</div>
      <div class="hero-bio">{{ userBio || '还没有写下个人简介' }}</div>
    </div>

    <div class="profile-container">
      <div class="settings-block">
        <div class="section-title">基本信息</div>
        <div class="app-card">
          <van-cell title="用户名" icon="contact">
            <template #value>
              <span class="cell-value strong">{{ userInfo?.username || 'admin' }}</span>
            </template>
          </van-cell>
          <van-cell title="账号 ID" icon="idcard">
            <template #value>
              <span class="cell-value">heima-{{ userId || 'N/A' }}</span>
            </template>
          </van-cell>
          <van-cell title="个人简介" icon="edit" is-link @click="showBioDialog">
            <template #value>
              <span class="cell-value">{{ userBio || '暂无简介' }}</span>
            </template>
          </van-cell>
        </div>
      </div>

      <div class="settings-block">
        <div class="section-title">账号安全</div>
        <div class="app-card">
          <van-cell title="修改密码" icon="lock" is-link @click="showPasswordConfirm" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, h, onMounted } from 'vue';
import { useUserStore } from '../store/user';
import { showDialog, showToast, showLoadingToast, showSuccessToast, showFailToast } from 'vant';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { apiConfig } from '../config/api';

const router = useRouter();
const userStore = useUserStore();

// 初始化用户状态
onMounted(async () => {
  // 如果用户未登录，跳转到登录页面
  if (!userStore.getLoginStatus) {
    router.push('/login');
    return;
  }

  // 获取用户信息
  try {
    // 显示加载提示
    const loadingInstance = showLoadingToast({
      message: '加载中...',
      forbidClick: true,
      duration: 0
    });

    // console.log('获取用户信息，当前token:', userStore.token);

    // 使用新的 getUserInfoDetail 方法
    const result = await userStore.getUserInfoDetail();

    // 手动关闭加载提示
    loadingInstance.close();

    if (result.success) {
      console.log('获取用户信息成功:', userStore.userInfo);
      // 显示成功提示
      // showSuccessToast('获取用户信息成功');
    } else {
      console.error('获取用户信息失败:', result.message);
      showFailToast(result.message || '获取用户信息失败');
    }
  } catch (error) {
    console.error('获取用户信息请求失败:', error);
    // 确保关闭加载提示
    showToast.clear();
    showToast.fail('获取用户信息失败');
  }
});

const userInfo = computed(() => userStore.userInfo);
const userId = computed(() => userStore.token ? userStore.token.substring(0, 5) : '');
const userBio = computed(() => userStore.userInfo?.bio || '暂无简介');

const showPasswordConfirm = () => {
  // 使用ref创建响应式变量
  const oldPassword = ref('');
  const newPassword = ref('');
  const confirmPassword = ref('');

  showDialog({
    title: '修改密码',
    showCancelButton: true,
    className: 'password-dialog',
    message: h('div', { style: 'text-align: left; padding: 10px 0;' }, [
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '当前密码：'),
        h('input', {
          type: 'password',
          value: oldPassword.value,
          onInput: (e) => { oldPassword.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 4px; padding: 8px; box-sizing: border-box;'
        })
      ]),
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '新密码：'),
        h('input', {
          type: 'password',
          value: newPassword.value,
          onInput: (e) => { newPassword.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 4px; padding: 8px; box-sizing: border-box;'
        })
      ]),
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '确认密码：'),
        h('input', {
          type: 'password',
          value: confirmPassword.value,
          onInput: (e) => { confirmPassword.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 4px; padding: 8px; box-sizing: border-box;'
        })
      ])
    ]),
  }).then(async () => {
    // 点击确认按钮
    if (!oldPassword.value) {
      showToast('请输入当前密码');
      return;
    }

    if (!newPassword.value) {
      showToast('请输入新密码');
      return;
    }

    if (newPassword.value !== confirmPassword.value) {
      showToast('两次密码输入不一致');
      return;
    }

    try {
      // 显示加载提示
      const loadingInstance = showLoadingToast({
        message: '修改中...',
        forbidClick: true,
        duration: 0
      });

      // 调用API更新密码
      const result = await userStore.updatePassword(oldPassword.value, newPassword.value);

      // 关闭加载提示
      loadingInstance.close();

      if (result && result.success) {
        showSuccessToast('密码修改成功');
      } else {
        showFailToast((result && result.message) || '密码修改失败');
      }
    } catch (error) {
      console.error('修改密码失败:', error);
      showToast.clear();
      showToast.fail('密码修改失败');
    }
  }).catch(() => {
    // 点击取消按钮
  });
};

const showBioDialog = () => {
  // 使用ref创建响应式变量
  const newBioValue = ref(userBio.value);

  showDialog({
    title: '修改个人简介',
    showCancelButton: true,
    confirmButtonText: '确认',
    className: 'bio-dialog',
    message: h('div', { style: 'text-align: left; padding: 10px 0;' }, [
      h('div', { style: 'margin-bottom: 15px;' }, [
        h('div', { style: 'margin-bottom: 5px; text-align: left;' }, '个人简介：'),
        h('textarea', {
          value: newBioValue.value,
          onInput: (e) => { newBioValue.value = e.target.value },
          style: 'width: 100%; border: 1px solid #dcdee0; border-radius: 4px; padding: 8px; box-sizing: border-box; min-height: 100px; resize: vertical;'
        })
      ])
    ])
  }).then(async () => {
    // 点击确认按钮
    try {
      // 显示加载提示
      const loadingInstance = showLoadingToast({
        message: '保存中...',
        forbidClick: true,
        duration: 0
      });

      console.log('更新个人简介:', newBioValue.value);

      // 调用API更新个人简介
      const result = await userStore.updateUserBio(newBioValue.value);

      // 关闭加载提示
      loadingInstance.close();

      if (result && result.success) {
        showSuccessToast('个人简介修改成功');
      } else {
        showFailToast((result && result.message) || '个人简介修改失败');
      }
    } catch (error) {
      console.error('更新个人简介失败:', error);
      showToast.clear();
      showToast.fail('个人简介修改失败');
    }
  }).catch(() => {
    // 点击取消按钮
  });
};
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background-color: var(--app-bg);
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

.profile-hero {
  position: relative;
  padding: 66px 20px 46px;
  text-align: center;
  background: var(--app-header-gradient);
  border-radius: 0 0 28px 28px;
  box-shadow: var(--app-shadow-primary);
  overflow: hidden;
}

.hero-orb {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.14);
}

.hero-orb-1 {
  width: 190px;
  height: 190px;
  top: -90px;
  left: -50px;
}

.hero-orb-2 {
  width: 120px;
  height: 120px;
  bottom: -50px;
  right: -20px;
  background: rgba(255, 255, 255, 0.09);
}

.avatar-wrap {
  width: 88px;
  height: 88px;
  margin: 0 auto 14px;
  padding: 5px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.35);
  box-shadow: 0 10px 26px rgba(11, 91, 215, 0.32);
}

.avatar-img {
  border: 3px solid #fff;
  display: block;
}

.hero-name {
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

.hero-id {
  margin-top: 6px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
}

.hero-bio {
  margin: 14px auto 0;
  max-width: 280px;
  padding: 9px 14px;
  border-radius: 999px;
  font-size: 12px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.92);
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.22);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-container {
  padding: 0 12px 30px;
  margin-top: 18px;
}

.settings-block {
  margin-bottom: 22px;
}

.settings-block .section-title {
  padding: 0 4px 12px;
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
  font-size: 13px;
  color: var(--app-text-3);
  max-width: 190px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cell-value.strong {
  color: var(--app-text-1);
  font-weight: 600;
}

.password-dialog .van-dialog__content {
  padding: 20px;
}

.password-form .form-item {
  margin-bottom: 15px;
  text-align: left;
}

.password-form .form-item span {
  display: block;
  margin-bottom: 5px;
  text-align: left;
}

.password-form .password-input {
  width: 100%;
  border: 1px solid #dcdee0;
  border-radius: 4px;
  padding: 8px;
  outline: none;
  box-sizing: border-box;
}
</style>
