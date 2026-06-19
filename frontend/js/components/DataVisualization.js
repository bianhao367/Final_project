const DataVisualization = {
    template: `
        <div class="card">
            <div class="card-header">数据可视化</div>
            <div class="card-body">
                <div class="viz-controls">
                    <button v-for="type in chartTypes" :key="type.value"
                            :class="['viz-btn', { active: currentType === type.value }]"
                            @click="createChart(type.value)">
                        {{ type.label }}
                    </button>
                </div>
                <div class="chart-container">
                    <img v-if="chartPath" :src="'/' + chartPath" alt="图表">
                    <p v-else>请选择图表类型生成可视化</p>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            currentType: 'bar',
            chartPath: '',
            chartTypes: [
                { value: 'bar', label: '柱状图' },
                { value: 'line', label: '折线图' },
                { value: 'pie', label: '饼图' }
            ]
        }
    },
    mounted() {
        this.createChart('bar');
    },
    methods: {
        async createChart(type) {
            this.currentType = type;

            let endpoint = `/api/visualization/${type}`;
            let body = {};

            if (type === 'bar') {
                body = { x: '产品类别', y: '销售总额', title: '各产品类别销售额' };
            } else if (type === 'pie') {
                body = { names: '产品类别', values: '销售总额', title: '销售额占比' };
            }

            try {
                const response = await axios.post(endpoint, body);

                if (response.data.error) {
                    console.error(response.data.error);
                    this.chartPath = '';
                } else {
                    this.chartPath = response.data.filepath;
                }
            } catch (error) {
                console.error('图表生成失败:', error);
                this.chartPath = '';
            }
        }
    }
};