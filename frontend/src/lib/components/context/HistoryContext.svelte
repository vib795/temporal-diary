<script lang="ts">
  import { fade, slide } from 'svelte/transition';
  import type { HistoricalEvent, HistoricalFigure } from '$lib/types/context';

  export let events: HistoricalEvent[] = [];
  export let births: HistoricalFigure[] = [];
  export let deaths: HistoricalFigure[] = [];
  export let yearFact: string | null = null;

  let activeSection: 'events' | 'births' | 'deaths' = 'events';
</script>

<div class="space-y-6">
  {#if yearFact}
    <div
      class="p-4 rounded-xl bg-gradient-to-r from-amber-900/30 to-orange-900/30 border border-amber-500/20"
      in:fade
    >
      <p class="text-amber-200/80 text-sm">{yearFact}</p>
    </div>
  {/if}

  <div class="flex gap-2">
    <button
      class="px-3 py-1.5 text-xs rounded-full transition-colors"
      class:bg-white/20={activeSection === 'events'}
      class:text-white={activeSection === 'events'}
      class:text-white/50={activeSection !== 'events'}
      on:click={() => (activeSection = 'events')}
    >
      Events ({events.length})
    </button>
    <button
      class="px-3 py-1.5 text-xs rounded-full transition-colors"
      class:bg-white/20={activeSection === 'births'}
      class:text-white={activeSection === 'births'}
      class:text-white/50={activeSection !== 'births'}
      on:click={() => (activeSection = 'births')}
    >
      Births ({births.length})
    </button>
    <button
      class="px-3 py-1.5 text-xs rounded-full transition-colors"
      class:bg-white/20={activeSection === 'deaths'}
      class:text-white={activeSection === 'deaths'}
      class:text-white/50={activeSection !== 'deaths'}
      on:click={() => (activeSection = 'deaths')}
    >
      Deaths ({deaths.length})
    </button>
  </div>

  {#if activeSection === 'events'}
    <div class="space-y-3" in:fade={{ duration: 200 }}>
      {#each events as event, i}
        <div
          class="relative pl-4 border-l-2 border-white/20 hover:border-amber-500/50 transition-colors"
          in:slide={{ duration: 200, delay: i * 50 }}
        >
          <span
            class="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-amber-500/20 border-2 border-amber-500/50"
          />
          <div class="pb-4">
            <span class="text-amber-400 text-xs font-medium">{event.year}</span>
            <p class="text-white/80 text-sm mt-1 leading-relaxed">
              {event.title}
            </p>
            {#if event.wikipedia_url}
              <a
                href={event.wikipedia_url}
                target="_blank"
                rel="noopener"
                class="text-xs text-white/40 hover:text-white/60 mt-1 inline-block"
              >
                Learn more →
              </a>
            {/if}
          </div>
        </div>
      {/each}

      {#if events.length === 0}
        <p class="text-white/40 text-center py-8">No events found for this day</p>
      {/if}
    </div>
  {/if}

  {#if activeSection === 'births'}
    <div class="space-y-3" in:fade={{ duration: 200 }}>
      {#each births as person, i}
        <div
          class="p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          in:slide={{ duration: 200, delay: i * 50 }}
        >
          <div class="flex items-center gap-2">
            <span class="text-green-400">🎂</span>
            <span class="text-white font-medium text-sm">{person.name}</span>
            <span class="text-white/40 text-xs">({person.year})</span>
          </div>
          <p class="text-white/50 text-xs mt-1 line-clamp-2">
            {person.description}
          </p>
        </div>
      {/each}

      {#if births.length === 0}
        <p class="text-white/40 text-center py-8">No notable births found</p>
      {/if}
    </div>
  {/if}

  {#if activeSection === 'deaths'}
    <div class="space-y-3" in:fade={{ duration: 200 }}>
      {#each deaths as person, i}
        <div
          class="p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
          in:slide={{ duration: 200, delay: i * 50 }}
        >
          <div class="flex items-center gap-2">
            <span class="text-gray-400">🕯️</span>
            <span class="text-white font-medium text-sm">{person.name}</span>
            <span class="text-white/40 text-xs">({person.year})</span>
          </div>
          <p class="text-white/50 text-xs mt-1 line-clamp-2">
            {person.description}
          </p>
        </div>
      {/each}

      {#if deaths.length === 0}
        <p class="text-white/40 text-center py-8">No notable deaths found</p>
      {/if}
    </div>
  {/if}
</div>
