<template>
  <div class="ai-chat-container">
    <div class="chat-nav">
      <span class="nav-orb nav-orb-1"></span>
      <span class="nav-orb nav-orb-2"></span>
      <div class="nav-inner">
        <div class="nav-icon"><van-icon name="chat-o" /></div>
        <div class="nav-text">
          <div class="nav-title">AI问答</div>
          <div class="nav-desc">智能助手，随时为你解答</div>
        </div>
        <span class="nav-status">在线</span>
      </div>
    </div>

    <div class="chat-content">
      <div class="messages-container" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']"
        >
          <div class="avatar" :class="message.role === 'user' ? 'avatar-user' : 'avatar-ai'">
            <van-icon :name="message.role === 'user' ? 'user-o' : 'service-o'" />
          </div>
          <div class="bubble-wrap">
            <div class="bubble-name">{{ message.role === 'user' ? '我' : 'AI 助手' }}</div>
            <div class="message-content">
              <div v-if="message.role === 'assistant' && message.content === ''" class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <div v-else v-html="formatMessage(message.content)"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="input-container">
        <div class="quick-row" v-if="messages.length <= 1">
          <span
            class="quick-chip"
            v-for="tip in quickTips"
            :key="tip"
            @click="useQuickTip(tip)"
          >
            {{ tip }}
          </span>
        </div>
        <div class="input-bar">
          <van-field
            v-model="userInput"
            rows="1"
            autosize
            type="textarea"
            placeholder="请输入问题..."
            class="chat-input"
            @keypress.enter.prevent="sendMessage"
          />
          <button class="send-button" :disabled="isLoading || !userInput.trim()" @click="sendMessage">
            <van-icon name="guide-o" />
            <span>发送</span>
          </button>
        </div>
      </div>
    </div>

    <tab-bar />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import TabBar from '../components/TabBar.vue';
import { showToast } from 'vant';
import * as marked from 'marked';
import DOMPurify from 'dompurify';
import { aiChatConfig } from '../config/api';

// 聊天消息
const messages = ref([
  { role: 'assistant', content: '你好！我是AI助手，有什么可以帮助你的吗？' }
]);
const userInput = ref('');
const messagesContainer = ref(null);
const isLoading = ref(false);

const quickTips = ['今日热点速览', '科技行业趋势', '写一段周末计划'];

// 从配置文件获取API设置
const apiEndpoint = ref(aiChatConfig.apiEndpoint);
const apiKey = ref(aiChatConfig.apiKey);
const model = ref(aiChatConfig.model);

// 格式化消息内容（支持Markdown）
const formatMessage = (content) => {
  if (!content) return '';
  // 使用marked解析Markdown，并用DOMPurify清理HTML
  return DOMPurify.sanitize(marked.parse(content));
};

// 快捷短语填充
const useQuickTip = (tip) => {
  userInput.value = tip;
};

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return;

  // 检查API设置
  if (!apiKey.value || apiKey.value === 'your-api-key-here') {
    showToast('API Key未配置，请联系管理员');
    return;
  }

  // 添加用户消息
  const userMessage = userInput.value.trim();
  messages.value.push({ role: 'user', content: userMessage });
  userInput.value = '';

  // 添加AI消息占位
  messages.value.push({ role: 'assistant', content: '' });

  // 滚动到底部
  await nextTick();
  scrollToBottom();

  // 发送请求
  isLoading.value = true;
  try {
    await fetchAIResponse(userMessage);
  } catch (error) {
    console.error('Error fetching AI response:', error);
    // 更新最后一条消息为错误信息
    messages.value[messages.value.length - 1].content = `发生错误: ${error.message || '请检查网络连接和API设置'}`;
  } finally {
    isLoading.value = false;
    await nextTick();
    scrollToBottom();
  }
};

// 获取AI响应（使用SSE）
const fetchAIResponse = async (userMessage) => {
  const allMessages = messages.value
    .slice(0, -1) // 排除最后一个空的assistant消息
    .map(msg => ({ role: msg.role, content: msg.content }));

  try {
    const response = await fetch(apiEndpoint.value, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`
      },
      body: JSON.stringify({
        model: model.value,
        messages: allMessages,
        stream: true
      })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error?.message || `HTTP error! status: ${response.status}`);
    }

    // 处理SSE流
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let aiResponse = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        if (data === '[DONE]') continue;

        try {
          const json = JSON.parse(data);
          // 兼容 OpenAI 格式（DeepSeek 与其一致）以及 DashScope 的返回格式
          const content = json.choices?.[0]?.delta?.content ||
                         json.output?.text ||
                         json.choices?.[0]?.message?.content || '';
          if (content) {
            aiResponse += content;
            // 更新最后一条消息
            messages.value[messages.value.length - 1].content = aiResponse;
            await nextTick();
            scrollToBottom();
          }
        } catch (e) {
          console.error('Error parsing SSE data:', e);
        }
      }
    }
  }

  // 如果没有收到任何内容
  if (!aiResponse) {
    messages.value[messages.value.length - 1].content = '抱歉，我无法生成回复。请检查API设置或稍后再试。';
  }
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
};

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 监听消息变化，自动滚动
watch(messages, () => {
  nextTick(scrollToBottom);
}, { deep: true });

// 组件挂载时滚动到底部
onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding-bottom: 54px;
  box-sizing: border-box;
  background-color: var(--app-bg);
}

.chat-nav {
  position: relative;
  flex-shrink: 0;
  padding: 12px 16px 16px;
  background: var(--app-gradient-deep);
  box-shadow: var(--app-shadow-primary);
  overflow: hidden;
}

.nav-orb {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.14);
}

.nav-orb-1 {
  width: 150px;
  height: 150px;
  top: -80px;
  right: -30px;
}

.nav-orb-2 {
  width: 90px;
  height: 90px;
  bottom: -50px;
  left: 40px;
  background: rgba(255, 255, 255, 0.08);
}

.nav-inner {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-icon {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #fff;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.nav-text {
  flex: 1;
  min-width: 0;
}

.nav-title {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 0.5px;
}

.nav-desc {
  margin-top: 3px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.78);
}

.nav-status {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 11px;
  color: #fff;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.28);
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px 14px 8px;
}

.message {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 18px;
  animation: message-in 0.3s cubic-bezier(0.22, 0.61, 0.36, 1) both;
}

@keyframes message-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-message {
  flex-direction: row-reverse;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 12px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  color: #fff;
  box-shadow: 0 4px 10px rgba(16, 24, 40, 0.14);
}

.avatar-ai {
  background: var(--app-gradient);
}

.avatar-user {
  background: linear-gradient(135deg, #6b7a90 0%, #47536a 100%);
}

.bubble-wrap {
  max-width: 78%;
  min-width: 0;
}

.user-message .bubble-wrap {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.bubble-name {
  font-size: 11px;
  color: var(--app-text-3);
  margin-bottom: 5px;
  padding: 0 4px;
}

.message-content {
  padding: 12px 14px;
  border-radius: 16px;
  font-size: 15px;
  line-height: 1.72;
  word-break: break-word;
}

.ai-message .message-content {
  background-color: var(--app-surface);
  color: var(--app-text-1);
  border-radius: 4px 16px 16px 16px;
  box-shadow: var(--app-shadow-2);
}

.user-message .message-content {
  background: var(--app-gradient);
  color: #fff;
  border-radius: 16px 4px 16px 16px;
  box-shadow: var(--app-shadow-primary);
}

.user-message .message-content :deep(p),
.user-message .message-content :deep(ul),
.user-message .message-content :deep(ol) {
  color: #fff;
}

.input-container {
  flex-shrink: 0;
  padding: 10px 12px 12px;
  border-top: 1px solid var(--app-line);
  background-color: var(--app-surface);
  box-shadow: 0 -6px 18px rgba(16, 24, 40, 0.05);
}

.quick-row {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.quick-row::-webkit-scrollbar {
  display: none;
}

.quick-chip {
  flex-shrink: 0;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  color: var(--app-primary);
  background-color: var(--app-primary-soft);
  border: 1px solid rgba(22, 119, 255, 0.18);
  cursor: pointer;
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.quick-chip:active {
  transform: scale(0.95);
  background-color: rgba(22, 119, 255, 0.2);
}

.input-bar {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}

.chat-input {
  flex: 1;
  min-width: 0;
  padding: 9px 14px;
  border-radius: 18px;
  background-color: #f2f4f8;
  border: 1px solid transparent;
  transition: border-color 0.24s ease, background-color 0.24s ease;
}

.chat-input:focus-within {
  background-color: var(--app-surface);
  border-color: rgba(22, 119, 255, 0.45);
}

.chat-input :deep(.van-field__control) {
  font-size: 15px;
  line-height: 1.5;
}

.send-button {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  height: 40px;
  padding: 0 16px;
  border: none;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  background: var(--app-gradient);
  box-shadow: var(--app-shadow-primary);
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.send-button:active:not(:disabled) {
  transform: scale(0.94);
}

.send-button:disabled {
  opacity: 0.45;
  box-shadow: none;
  cursor: not-allowed;
}

/* Markdown 样式 */
.message-content pre {
  background-color: #f6f7fa;
  padding: 10px;
  border-radius: 10px;
  overflow-x: auto;
  border: 1px solid var(--app-line);
}

.message-content code {
  background-color: rgba(22, 119, 255, 0.1);
  color: #0b5bd7;
  padding: 2px 5px;
  border-radius: 5px;
  font-size: 13px;
}

.message-content img {
  max-width: 100%;
  border-radius: 10px;
}

.message-content :deep(pre) {
  background-color: #f6f7fa;
  border: 1px solid var(--app-line);
  padding: 10px;
  border-radius: 10px;
  overflow-x: auto;
}

.message-content :deep(code) {
  font-family: monospace;
  background-color: rgba(22, 119, 255, 0.1);
  color: #0b5bd7;
  padding: 2px 5px;
  border-radius: 5px;
}

.message-content :deep(p) {
  margin: 0 0 8px;
}

.message-content :deep(p:last-child) {
  margin-bottom: 0;
}

.message-content :deep(ul),
.message-content :deep(ol) {
  margin: 6px 0;
  padding-left: 20px;
}

.message-content :deep(ul li),
.message-content :deep(ol li) {
  margin-bottom: 4px;
}

.message-content :deep(a) {
  color: var(--app-primary);
  text-decoration: none;
}

.message-content :deep(blockquote) {
  margin: 8px 0;
  padding: 6px 12px;
  border-left: 3px solid var(--app-primary);
  background-color: rgba(22, 119, 255, 0.06);
  color: var(--app-text-2);
}

/* 打字指示器 */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 0;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: var(--app-primary);
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.4s infinite ease-in-out;
  opacity: 0.6;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.18s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.36s;
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  30% {
    transform: translateY(-6px);
    opacity: 1;
  }
}
</style>
