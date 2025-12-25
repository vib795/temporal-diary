import { apiClient } from './api';
import type { TemporalContext } from '$lib/types/context';
import { format } from 'date-fns';

export class ContextService {
  async getContext(date: Date): Promise<TemporalContext> {
    const dateStr = format(date, 'yyyy-MM-dd');
    return await apiClient.get<TemporalContext>(`/api/v1/context/${dateStr}`);
  }

  async getSpaceContext(date: Date): Promise<any> {
    const dateStr = format(date, 'yyyy-MM-dd');
    return await apiClient.get(`/api/v1/context/${dateStr}/space`);
  }

  async getHistoryContext(date: Date): Promise<any> {
    const dateStr = format(date, 'yyyy-MM-dd');
    return await apiClient.get(`/api/v1/context/${dateStr}/history`);
  }

  async getWeatherContext(date: Date): Promise<any> {
    const dateStr = format(date, 'yyyy-MM-dd');
    return await apiClient.get(`/api/v1/context/${dateStr}/weather`);
  }
}

export const contextService = new ContextService();
