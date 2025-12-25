import { apiClient } from './api';
import type { Entry, CreateEntryInput } from '$lib/types/entry';
import { format } from 'date-fns';

export class EntryService {
  async getEntry(date: Date): Promise<Entry | null> {
    const dateStr = format(date, 'yyyy-MM-dd');
    try {
      return await apiClient.get<Entry>(`/api/v1/entries/${dateStr}`);
    } catch {
      return null;
    }
  }

  async getTodayEntry(): Promise<Entry | null> {
    try {
      return await apiClient.get<Entry>('/api/v1/entries/today');
    } catch {
      return null;
    }
  }

  async createEntry(data: CreateEntryInput): Promise<Entry> {
    return await apiClient.post<Entry>('/api/v1/entries', data);
  }

  async updateEntry(date: Date, data: Partial<CreateEntryInput>): Promise<Entry> {
    const dateStr = format(date, 'yyyy-MM-dd');
    return await apiClient.put<Entry>(`/api/v1/entries/${dateStr}`, data);
  }

  async deleteEntry(date: Date): Promise<void> {
    const dateStr = format(date, 'yyyy-MM-dd');
    await apiClient.delete(`/api/v1/entries/${dateStr}`);
  }

  async saveEntry(data: CreateEntryInput): Promise<Entry> {
    // Try to update first, if fails, create
    try {
      const dateObj = new Date(data.entry_date);
      return await this.updateEntry(dateObj, data);
    } catch {
      return await this.createEntry(data);
    }
  }
}

export const entryService = new EntryService();
