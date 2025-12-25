import { writable, derived } from 'svelte/store';
import type { Entry } from '$lib/types/entry';
import { entryService } from '$lib/services/entryService';

interface EntryStore {
  currentEntry: Entry | null;
  isLoading: boolean;
  error: string | null;
}

const createEntryStore = () => {
  const { subscribe, set, update } = writable<EntryStore>({
    currentEntry: null,
    isLoading: false,
    error: null,
  });

  return {
    subscribe,
    async fetchEntry(date: Date) {
      update((state) => ({ ...state, isLoading: true, error: null }));
      try {
        const entry = await entryService.getEntry(date);
        update((state) => ({ ...state, currentEntry: entry, isLoading: false }));
      } catch (error) {
        update((state) => ({
          ...state,
          error: error instanceof Error ? error.message : 'Failed to fetch entry',
          isLoading: false,
        }));
      }
    },
    async saveEntry(data: any) {
      update((state) => ({ ...state, isLoading: true, error: null }));
      try {
        const entry = await entryService.saveEntry(data);
        update((state) => ({ ...state, currentEntry: entry, isLoading: false }));
        return entry;
      } catch (error) {
        update((state) => ({
          ...state,
          error: error instanceof Error ? error.message : 'Failed to save entry',
          isLoading: false,
        }));
        throw error;
      }
    },
    reset() {
      set({
        currentEntry: null,
        isLoading: false,
        error: null,
      });
    },
  };
};

export const entryStore = createEntryStore();
