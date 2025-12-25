<script lang="ts">
  import { fade } from 'svelte/transition';
  import SpaceContext from './SpaceContext.svelte';
  import HistoryContext from './HistoryContext.svelte';
  import type { TemporalContext } from '$lib/types/context';

  export let context: TemporalContext | null = null;
  export let isLoading: boolean = false;

  let activeTab: 'space' | 'history' | 'weather' = 'space';

  const tabs = [
    { id: 'space', label: 'Space', icon: '🌌' },
    { id: 'history', label: 'History', icon: '📜' },
    { id: 'weather', label: 'Weather', icon: '🌤️' },
  ] as const;
</script>

<div class="bg-white/5 backdrop-blur-xl rounded-3xl border border-white/10 overflow-hidden">
  <!-- Tabs -->
  <div class="flex border-b border-white/10">
    {#each tabs as tab}
      <button
        class="flex-1 px-4 py-3 text-sm font-medium transition-colors"
        class:text-white={activeTab === tab.id}
        class:bg-white/10={activeTab === tab.id}
        class:text-white/50={activeTab !== tab.id}
        on:click={() => (activeTab = tab.id)}
      >
        <span class="mr-1">{tab.icon}</span>
        {tab.label}
      </button>
    {/each}
  </div>

  <!-- Content -->
  <div class="p-4 min-h-[400px]">
    {#if isLoading}
      <div class="flex items-center justify-center h-64">
        <div class="animate-pulse text-white/40">Loading cosmic context...</div>
      </div>
    {:else if context}
      {#if activeTab === 'space'}
        <div in:fade={{ duration: 200 }}>
          <SpaceContext
            apod={context.apod || null}
            marsPhotos={context.mars_photos || []}
            neos={context.near_earth_objects || []}
          />
        </div>
      {:else if activeTab === 'history'}
        <div in:fade={{ duration: 200 }}>
          <HistoryContext
            events={context.historical_events || []}
            births={context.notable_births || []}
            deaths={context.notable_deaths || []}
            yearFact={context.year_fact || null}
          />
        </div>
      {:else if activeTab === 'weather' && context.weather}
        <div in:fade={{ duration: 200 }}>
          <div class="space-y-4">
            <div class="p-4 rounded-xl bg-white/5">
              <h3 class="text-xs uppercase tracking-wider text-white/40 mb-3">
                Weather on this day
              </h3>
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-white/60 text-sm">Condition</span>
                  <span class="text-white font-medium">{context.weather.weather_description}</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-white/60 text-sm">Temperature</span>
                  <span class="text-white font-medium">
                    {context.weather.temperature_mean_c.toFixed(1)}°C
                  </span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-white/60 text-sm">Range</span>
                  <span class="text-white/60 text-sm">
                    {context.weather.temperature_min_c.toFixed(1)}°C - {context.weather.temperature_max_c.toFixed(
                      1
                    )}°C
                  </span>
                </div>
                {#if context.weather.precipitation_mm > 0}
                  <div class="flex items-center justify-between">
                    <span class="text-white/60 text-sm">Precipitation</span>
                    <span class="text-white/60 text-sm">
                      {context.weather.precipitation_mm.toFixed(1)}mm
                    </span>
                  </div>
                {/if}
              </div>
            </div>
          </div>
        </div>
      {:else}
        <div class="text-center text-white/40 py-12">
          No weather data available for this date
        </div>
      {/if}
    {:else}
      <div class="text-center text-white/40 py-12">
        No context available for this date
      </div>
    {/if}
  </div>
</div>
