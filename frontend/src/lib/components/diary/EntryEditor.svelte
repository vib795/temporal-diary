<script lang="ts">
  import { onDestroy } from 'svelte';
  import { entryStore } from '$lib/stores/entries';
  import type { Entry } from '$lib/types/entry';

  export let date: Date;
  export let entry: Entry | null = null;

  let content = '';
  let title = '';
  let isSaving = false;
  let lastSaved: Date | null = null;
  let autoSaveTimer: ReturnType<typeof setTimeout>;

  $: wordCount = content.trim() ? content.trim().split(/\s+/).length : 0;

  $: if (entry) {
    content = entry.content || '';
    title = entry.title || '';
  }

  function scheduleAutoSave() {
    clearTimeout(autoSaveTimer);
    autoSaveTimer = setTimeout(async () => {
      if (content.trim()) {
        await saveEntry();
      }
    }, 2000);
  }

  async function saveEntry() {
    if (isSaving) return;

    isSaving = true;
    try {
      await entryStore.saveEntry({
        entry_date: date.toISOString().split('T')[0],
        title: title || undefined,
        content,
      });
      lastSaved = new Date();
    } catch (error) {
      console.error('Failed to save:', error);
    } finally {
      isSaving = false;
    }
  }

  function handleInput() {
    scheduleAutoSave();
  }

  onDestroy(() => {
    clearTimeout(autoSaveTimer);
  });
</script>

<div class="space-y-4">
  <input
    type="text"
    bind:value={title}
    on:input={handleInput}
    placeholder="Give this day a title... (optional)"
    class="w-full bg-transparent text-white text-xl font-light placeholder-white/30 border-none outline-none focus:ring-0"
  />

  <div class="relative">
    <textarea
      bind:value={content}
      on:input={handleInput}
      placeholder="What's on your mind today? Your thoughts exist in the same moment as stars being born and civilizations rising..."
      class="w-full min-h-[300px] bg-transparent text-white/90 placeholder-white/30 border-none outline-none focus:ring-0 resize-none leading-relaxed"
    />
  </div>

  <div class="flex items-center justify-between pt-4 border-t border-white/10">
    <div class="flex items-center gap-4">
      <span class="text-white/30 text-sm">
        {wordCount} {wordCount === 1 ? 'word' : 'words'}
      </span>
    </div>

    <div class="flex items-center gap-4">
      {#if isSaving}
        <span class="text-white/40 text-sm">Saving...</span>
      {:else if lastSaved}
        <span class="text-white/30 text-sm">
          Saved {lastSaved.toLocaleTimeString()}
        </span>
      {/if}

      <button
        on:click={saveEntry}
        disabled={isSaving || !content.trim()}
        class="px-4 py-2 rounded-lg bg-white/10 text-white text-sm hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Save Entry
      </button>
    </div>
  </div>
</div>
