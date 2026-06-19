const ChatAssistant = {
    template: `
        <div class="card">
            <div class="card-header">智能问答助手</div>
            <div class="card-body">
                <div class="chat-container">
                    <div class="chat-messages" ref="chatMessages">
                        <div v-for="(msg, index) in messages" :key="index"
                             :class="['message', msg.role]">
                            <div class="message-content">{{ msg.content }}</div>
                        </div>
                    </div>
                    <div class="chat-input">
                        <input type="text" v-model="inputMessage"
                               placeholder="请输入您的问题..."
                               @keypress.enter="sendMessage">
                        <button @click="sendMessage" :disabled="loading">
                            {{ loading ? '发送中...' : '发送' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            inputMessage: '',
            messages: [
                {
                    role: 'assistant',
                    content: '您好！我是智能数据分析助手，可以帮您分析销售数据、回答数据相关问题。请问有什么可以帮您的？'
                }
            ],
            loading: false
        }
    },
    methods: {
        async sendMessage() {
            const message = this.inputMessage.trim();
            if (!message || this.loading) return;

            // 添加用户消息
            this.messages.push({ role: 'user', content: message });
            this.inputMessage = '';
            this.loading = true;

            // 滚动到底部
            this.$nextTick(() => {
                this.scrollToBottom();
            });

            try {
                const response = await axios.post('/api/chat', { message });

                if (response.data.error) {
                    this.messages.push({
                        role: 'assistant',
                        content: '抱歉，处理您的请求时出现错误: ' + response.data.error
                    });
                } else {
                    this.messages.push({
                        role: 'assistant',
                        content: response.data.response
                    });
                }
            } catch (error) {
                this.messages.push({
                    role: 'assistant',
                    content: '网络错误，请稍后重试'
                });
            } finally {
                this.loading = false;
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            }
        },
        scrollToBottom() {
            const container = this.$refs.chatMessages;
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        }
    }
};