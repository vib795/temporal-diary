import { writable } from 'svelte/store';
import type { TemporalContext } from '$lib/types/context';
import { contextService } from '$lib/services/contextService';

interface ContextStore {
  context: TemporalContext | null;
  isLoading: boolean;
  error: string | null;
}

const createContextStore = () => {
  const { subscribe, set, update } = writable<ContextStore>({
    context: null,
    isLoading: false,
    error: null,
  });

  return {
    subscribe,
    async fetchContext(date: Date) {
      update((state) => ({ ...state, isLoading: true, error: null }));
      try {
        const context = await contextService.getContext(date);
        update((state) => ({ ...state, context, isLoading: false }));
      } catch (error) {
        update((state) => ({
          ...state,
          error: error instanceof Error ? error.message : 'Failed to fetch context',
          isLoading: false,
        }));
      }
    },
    reset() {
      set({
        context: null,
        isLoading: false,
        error: null,
      });
    },
  };
};

export const contextStore = createContextStore();
