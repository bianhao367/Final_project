const NaturalQuery = {
    template: `
        <div class="card">
            <div class="card-header">自然语言查询</div>
            <div class="card-body">
                <div class="query-section">
                    <input type="text" class="query-input" v-model="queryInput"
                           placeholder="请输入您的查询，例如：查询所有电子产品的销售总额"
                           @keypress.enter="executeQuery">
                    <button @click="executeQuery" :disabled="loading"
                            style="padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; cursor: pointer;">
                        {{ loading ? '执行中...' : '执行查询' }}
                    </button>
                </div>
                <div class="suggestions">
                    <span v-for="(suggestion, index) in suggestions" :key="index"
                          class="suggestion" @click="useSuggestion(suggestion)">
                        {{ suggestion }}
                    </span>
                </div>
                <div class="query-result">
                    <div v-if="queryResult.sql" class="sql-display">
                        SQL: {{ queryResult.sql }}
                    </div>
                    <table v-if="queryResult.result && queryResult.result.length > 0">
                        <thead>
                            <tr>
                                <th v-for="col in queryResult.columns" :key="col">{{ col }}</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(row, index) in queryResult.result" :key="index">
                                <td v-for="col in queryResult.columns" :key="col">
                                    {{ row[col] || '-' }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <p v-else>输入自然语言查询，系统将自动转换为SQL并执行</p>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            queryInput: '',
            suggestions: [],
            queryResult: {
                sql: '',
                result: [],
                columns: []
            },
            loading: false
        }
    },
    mounted() {
        this.loadSuggestions();
    },
    methods: {
        async loadSuggestions() {
            try {
                const response = await axios.get('/api/query/suggestions');
                if (response.data.suggestions) {
                    this.suggestions = response.data.suggestions;
                }
            } catch (error) {
                console.error('加载查询建议失败:', error);
            }
        },
        async executeQuery() {
            const query = this.queryInput.trim();
            if (!query || this.loading) return;

            this.loading = true;
            this.queryResult = { sql: '', result: [], columns: [] };

            try {
                const response = await axios.post('/api/query', { query });

                if (response.data.error) {
                    console.error(response.data.error);
                } else {
                    this.queryResult = {
                        sql: response.data.sql,
                        result: response.data.result,
                        columns: response.data.columns
                    };
                }
            } catch (error) {
                console.error('查询执行失败:', error);
            } finally {
                this.loading = false;
            }
        },
        useSuggestion(suggestion) {
            this.queryInput = suggestion;
            this.executeQuery();
        }
    }
};