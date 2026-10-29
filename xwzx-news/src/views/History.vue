<template>
  <div class="history-container">
    <van-nav-bar
      title="浏览历史"
      left-text="返回"
      left-arrow
      @click-left="onClickLeft"
      right-text="清空"
      @click-right="onClickClear"
      fixed
    />

    <div class="history-list" v-if="historyStore.getHistory.length">
      <div class="history-item" v-for="item in historyStore.getHistory" :key="item.id">
        <van-cell @click="goToNewsDetail(item.id)" :border="false" class="history-cell">
          <template #title>
            <div class="history-card">
              <div class="history-main">
                <div class="news-title">{{ item.title }}</div>
                <div class="news-meta">
                  <span>{{ item.author }}</span>
                  <span>{{ item.publishTime }}</span>
                </div>
                <div class="news-viewtime">
                  <van-icon name="clock-o" />
                  <span>浏览时间: {{ item.viewTime }}</span>
                </div>
              </div>
              <div class="news-image" v-if="item.image">
                <img :src="item.image" :alt="item.title" loading="lazy">
              </div>
            </div>
          </template>
        </van-cell>
        <van-button
          class="delete-btn"
          type="danger"
          size="mini"
          icon="cross"
          @click="confirmDelete(item.id)"
        ></van-button>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="empty-icon"><van-icon name="clock-o" /></div>
      <div class="empty-title">暂无浏览历史</div>
      <div class="empty-desc">看过的每一篇好文章都会记录在这里</div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useHistoryStore } from '../store/modules/history';
import { showDialog } from 'vant';

const router = useRouter();
const historyStore = useHistoryStore();

const onClickLeft = () => {
  router.back();
};

const goToNewsDetail = (id) => {
  router.push(`/news/detail/${id}`);
};

const removeHistory = async (id) => {
  try {
    const result = await historyStore.removeHistoryApi(id);
    console.log('删除单条历史记录结果:', result);

    if (!result.success && !result.isLocal) {
      showDialog({
        title: '提示',
        message: result.message || '删除失败，请稍后重试',
      });
    }
  } catch (error) {
    console.error('删除历史记录失败:', error);
  }
};

const confirmDelete = (id) => {
  showDialog({
    title: '提示',
    message: '确定要删除这条浏览记录吗？',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      removeHistory(id);
    }
  });
};

const onClickClear = async () => {
  showDialog({
    title: '提示',
    message: '确定要清空所有浏览历史吗？',
    showCancelButton: true,
  }).then(async (action) => {
    if (action === 'confirm') {
      try {
        const result = await historyStore.clearHistoryApi();
        console.log('清空历史记录结果:', result);

        if (!result.success && !result.isLocal) {
          showDialog({
            title: '提示',
            message: result.message || '清空失败，请稍后重试',
          });
        }
      } catch (error) {
        console.error('清空历史记录失败:', error);
      }
    }
  });
};

onMounted(async () => {
  try {
    const result = await historyStore.getHistoryListApi();
    console.log('浏览历史页面：API获取结果', result);

    if (!result || !result.success) {
      historyStore.loadHistory();
    }
  } catch (error) {
    console.error('浏览历史页面：API请求异常', error);
    historyStore.loadHistory();
  }
});
</script>

<style scoped>
.history-container {
  padding-top: 46px;
  padding-bottom: 30px;
  background-color: var(--app-bg);
  min-height: 100vh;
}

:deep(.van-nav-bar) {
  background-color: var(--app-surface);
  box-shadow: 0 1px 0 rgba(16, 24, 40, 0.04), 0 6px 18px rgba(16, 24, 40, 0.05);
}

:deep(.van-nav-bar__right) {
  color: var(--app-primary);
}

.history-list {
  padding: 14px 12px 0;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding: 14px 12px;
  background-color: var(--app-surface);
  border-radius: var(--app-radius);
  box-shadow: var(--app-shadow-2);
  transition: transform 0.28s cubic-bezier(0.22, 0.61, 0.36, 1), box-shadow 0.28s ease;
}

.history-item:active {
  transform: scale(0.99);
}

@media (hover: hover) {
  .history-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--app-shadow-3);
  }
}

.history-cell {
  flex: 1;
  min-width: 0;
  padding: 0;
  background: transparent;
}

.history-cell :deep(.van-cell__title) {
  padding: 0;
}

.history-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.history-main {
  flex: 1;
  min-width: 0;
}

.news-title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.45;
  color: var(--app-text-1);
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.news-meta {
  font-size: 12px;
  color: var(--app-text-3);
  display: flex;
  flex-wrap: wrap;
}

.news-meta span + span::before {
  content: '';
  display: inline-block;
  width: 3px;
  height: 3px;
  margin: 0 8px;
  border-radius: 50%;
  background-color: #d6d9de;
  vertical-align: middle;
}

.news-viewtime {
  margin-top: 8px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 999px;
  background-color: var(--app-primary-soft);
  color: var(--app-primary);
  font-size: 11px;
}

.news-image {
  width: 108px;
  height: 72px;
  flex-shrink: 0;
  border-radius: var(--app-radius-sm);
  overflow: hidden;
  background: linear-gradient(135deg, #f0f2f6 0%, #e8ebf1 100%);
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.delete-btn {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  min-width: 28px;
  padding: 0;
  border-radius: 50%;
  background-color: rgba(240, 75, 75, 0.1);
  border-color: transparent;
  color: #f04b4b;
  font-size: 13px;
  transition: transform 0.2s ease;
}

.delete-btn:active {
  transform: scale(0.88);
}
</style>
