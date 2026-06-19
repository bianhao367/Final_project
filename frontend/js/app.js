const { createApp } = Vue;

const app = createApp({
    data() {
        return {
            // 全局数据
        }
    }
});

// 注册组件
app.component('data-summary', DataSummary);
app.component('chat-assistant', ChatAssistant);
app.component('data-visualization', DataVisualization);
app.component('natural-query', NaturalQuery);

// 挂载应用
app.mount('#app');