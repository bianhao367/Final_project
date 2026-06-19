const DataSummary = {
    template: `
        <div class="card">
            <div class="card-header">数据概览</div>
            <div class="card-body">
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value">{{ formatCurrency(statistics.总销售额) }}</div>
                        <div class="stat-label">总销售额</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ formatNumber(statistics.订单数量) }}</div>
                        <div class="stat-label">订单数量</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ formatCurrency(statistics.总利润) }}</div>
                        <div class="stat-label">总利润</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ formatCurrency(statistics.平均订单金额) }}</div>
                        <div class="stat-label">平均订单金额</div>
                    </div>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            statistics: {
                总销售额: 0,
                订单数量: 0,
                总利润: 0,
                平均订单金额: 0
            }
        }
    },
    mounted() {
        this.loadDataSummary();
    },
    methods: {
        async loadDataSummary() {
            try {
                const response = await axios.get('/api/data/summary');
                if (response.data.error) {
                    console.error(response.data.error);
                    return;
                }
                this.statistics = response.data.statistics;
            } catch (error) {
                console.error('加载数据摘要失败:', error);
            }
        },
        formatCurrency(value) {
            if (!value) return '¥0.00';
            return '¥' + Number(value).toLocaleString('zh-CN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        },
        formatNumber(value) {
            if (!value) return '0';
            return Number(value).toLocaleString('zh-CN');
        }
    }
};