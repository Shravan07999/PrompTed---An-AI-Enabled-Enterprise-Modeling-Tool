import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const PromptService = {
    getAll: async () => {
        const response = await api.get('/prompts/');
        return response.data;
    },
    getById: async (id: number) => {
        const response = await api.get(`/prompts/${id}`);
        return response.data;
    },
    create: async (data: any) => {
        const response = await api.post('/prompts/', data);
        return response.data;
    },
    delete: async (id: number) => {
        const response = await api.delete(`/prompts/${id}`);
        return response.data;
    },
};

export const ChainService = {
    getAll: async () => {
        const response = await api.get('/chains/');
        return response.data;
    },
    create: async (data: any) => {
        const response = await api.post('/chains/', data);
        return response.data;
    },
    addStep: async (chainId: number, stepData: any) => {
        const response = await api.post(`/chains/${chainId}/steps`, stepData);
        return response.data;
    },
    update: async (id: number, data: any) => {
        const response = await api.patch(`/chains/${id}`, data);
        return response.data;
    },
    delete: async (id: number) => {
        const response = await api.delete(`/chains/${id}`);
        return response.data;
    },
};

export const AnalyticsService = {
    getUsage: async () => {
        const response = await api.get('/analytics/usage');
        return response.data;
    },
    getAuditLogs: async () => {
        const response = await api.get('/analytics/history');
        return response.data;
    },
};

export const ExecutionService = {
    execute: async (promptId: number, inputs: Record<string, any>) => {
        const response = await api.post('/execute/', {
            prompt_id: promptId,
            inputs: inputs,
        });
        return response.data;
    },
    executeChain: async (chainId: number, inputs: Record<string, any>) => {
        const response = await api.post('/execute/chain', {
            chain_id: chainId,
            inputs: inputs,
        });
        return response.data;
    },
    getHistory: async () => {
        const response = await api.get('/execute/history');
        return response.data;
    },
};

export default api;
