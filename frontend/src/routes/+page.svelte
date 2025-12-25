<script lang="ts">
  import { onMount } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import CosmicBackground from '$lib/components/layout/CosmicBackground.svelte';
  import EntryEditor from '$lib/components/diary/EntryEditor.svelte';
  import ContextPanel from '$lib/components/context/ContextPanel.svelte';
  import { contextStore } from '$lib/stores/context';
  import { entryStore } from '$lib/stores/entries';
  import { format } from 'date-fns';

  let selectedDate = new Date();
  let isLoading = true;

  $: formattedDate = format(selectedDate, 'EEEE, MMMM d, yyyy');

  onMount(async () => {
    await loadDateData(selectedDate);
  });

  async function loadDateData(date: Date) {
    isLoading = true;
    await Promise.all([contextStore.fetchContext(date), entryStore.fetchEntry(date)]);
    isLoading = false;
  }

  function goToToday() {
    selectedDate = new Date();
    loadDateData(selectedDate);
  }

  function changeDate(days: number) {
    const newDate = new Date(selectedDate);
    newDate.setDate(newDate.getDate() + days);
    selectedDate = newDate;
    loadDateData(selectedDate);
  }
</script>

<svelte:head>
  <title>Temporal Diary - {formattedDate}</title>
</svelte:head>

<CosmicBackground />

<div class="min-h-screen relative z-10">
  <main class="container mx-auto px-4 py-8 max-w-7xl">
    <!-- Header -->
    <header class="text-center mb-12" in:fade={{ duration: 500 }}>
      <h1 class="text-4xl md:text-5xl font-light text-white mb-2 tracking-wide">
        Temporal Diary
      </h1>
      <p class="text-white/50 text-lg">Your story, in cosmic context</p>
    </header>

    <!-- Date Navigation -->
    <div class="flex justify-center mb-8 gap-2">
      <button
        on:click={() => changeDate(-1)}
        class="px-4 py-2 rounded-lg bg-white/10 text-white hover:bg-white/20 transition-colors"
      >
        ← Previous Day
      </button>
      <button
        on:click={goToToday}
        class="px-6 py-2 rounded-lg bg-white/10 text-white hover:bg-white/20 transition-colors"
      >
        Today
      </button>
      <button
        on:click={() => changeDate(1)}
        class="px-4 py-2 rounded-lg bg-white/10 text-white hover:bg-white/20 transition-colors"
      >
        Next Day →
      </button>
    </div>

    <!-- Main Content Grid -->
    <div class="grid lg:grid-cols-3 gap-8">
      <!-- Entry Editor -->
      <div class="lg:col-span-2 order-2 lg:order-1">
        <div
          class="bg-white/5 backdrop-blur-xl rounded-3xl p-6 md:p-8 border border-white/10"
          in:fly={{ y: 20, duration: 500, delay: 200 }}
        >
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-2xl font-light text-white">
                {formattedDate}
              </h2>
              {#if $contextStore.context?.day_summary}
                <p class="text-white/40 text-sm mt-1 max-w-xl">
                  {$contextStore.context.day_summary}
                </p>
              {/if}
            </div>
          </div>

          <EntryEditor date={selectedDate} entry={$entryStore.currentEntry} />
        </div>

        <!-- Cosmic Perspective -->
        {#if $contextStore.context?.cosmic_perspective}
          <div
            class="mt-6 p-6 bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-2xl border border-purple-500/20"
            in:fade={{ duration: 500, delay: 600 }}
          >
            <p class="text-white/80 italic text-center">
              "{$contextStore.context.cosmic_perspective}"
            </p>
          </div>
        {/if}
      </div>

      <!-- Context Panel -->
      <div class="order-1 lg:order-2">
        <div in:fly={{ x: 20, duration: 500, delay: 300 }}>
          <ContextPanel context={$contextStore.context} {isLoading} />
        </div>
      </div>
    </div>
  </main>
</div>
