<script lang="ts">
  import { fade } from 'svelte/transition';
  import type { APODData, MarsPhoto, NearEarthObject } from '$lib/types/context';

  export let apod: APODData | null = null;
  export let marsPhotos: MarsPhoto[] = [];
  export let neos: NearEarthObject[] = [];

  let showFullExplanation = false;
</script>

<div class="space-y-6">
  {#if apod}
    <section in:fade={{ duration: 300 }}>
      <h3 class="text-xs uppercase tracking-wider text-white/40 mb-3">
        Astronomy Picture of the Day
      </h3>

      <div class="relative rounded-xl overflow-hidden group">
        {#if apod.media_type === 'image'}
          <img
            src={apod.url}
            alt={apod.title}
            class="w-full h-48 object-cover transition-transform duration-500 group-hover:scale-105"
          />
        {:else}
          <div class="w-full h-48 bg-black flex items-center justify-center">
            <a href={apod.url} target="_blank" rel="noopener" class="text-purple-400 hover:text-purple-300">
              ▶ Watch Video
            </a>
          </div>
        {/if}

        <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent" />

        <div class="absolute bottom-0 left-0 right-0 p-4">
          <h4 class="text-white font-medium text-sm">{apod.title}</h4>
          {#if apod.copyright}
            <p class="text-white/40 text-xs mt-1">© {apod.copyright}</p>
          {/if}
        </div>
      </div>

      <div class="mt-3">
        <p class="text-white/60 text-sm leading-relaxed">
          {#if showFullExplanation}
            {apod.explanation}
          {:else}
            {apod.explanation.slice(0, 150)}...
          {/if}
        </p>
        {#if apod.explanation.length > 150}
          <button
            class="text-purple-400 text-xs mt-2 hover:text-purple-300"
            on:click={() => (showFullExplanation = !showFullExplanation)}
          >
            {showFullExplanation ? 'Show less' : 'Read more'}
          </button>
        {/if}
      </div>
    </section>
  {/if}

  {#if neos.length > 0}
    <section in:fade={{ duration: 300, delay: 100 }}>
      <h3 class="text-xs uppercase tracking-wider text-white/40 mb-3">
        Cosmic Visitors ({neos.length} asteroids)
      </h3>

      <div class="space-y-2">
        {#each neos.slice(0, 3) as neo}
          <div
            class="p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
            class:border-l-2={neo.is_potentially_hazardous}
            class:border-red-500={neo.is_potentially_hazardous}
          >
            <div class="flex items-center justify-between">
              <span class="text-white text-sm font-medium">
                {neo.name.replace(/[()]/g, '')}
              </span>
              {#if neo.is_potentially_hazardous}
                <span class="text-xs px-2 py-0.5 bg-red-500/20 text-red-400 rounded">
                  Hazardous
                </span>
              {/if}
            </div>
            <div class="mt-1 text-xs text-white/40 space-y-1">
              <p>Distance: {(neo.miss_distance_km / 1000000).toFixed(2)} million km</p>
              <p>
                Size: {neo.estimated_diameter_min_m.toFixed(0)}-{neo.estimated_diameter_max_m.toFixed(
                  0
                )}m
              </p>
            </div>
          </div>
        {/each}
      </div>
    </section>
  {/if}

  {#if marsPhotos.length > 0}
    <section in:fade={{ duration: 300, delay: 200 }}>
      <h3 class="text-xs uppercase tracking-wider text-white/40 mb-3">
        From Mars ({marsPhotos[0].rover_name})
      </h3>

      <div class="grid grid-cols-2 gap-2">
        {#each marsPhotos.slice(0, 4) as photo}
          <a
            href={photo.img_src}
            target="_blank"
            rel="noopener"
            class="relative rounded-lg overflow-hidden aspect-square group"
          >
            <img
              src={photo.img_src}
              alt="Mars - {photo.camera_name}"
              class="w-full h-full object-cover transition-transform group-hover:scale-110"
            />
            <div
              class="absolute bottom-0 left-0 right-0 p-2 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <span class="text-white text-xs">{photo.camera_name}</span>
            </div>
          </a>
        {/each}
      </div>
    </section>
  {/if}

  {#if !apod && neos.length === 0 && marsPhotos.length === 0}
    <div class="text-center py-12">
      <div class="text-4xl mb-4">🌟</div>
      <p class="text-white/40">No space data available for this date</p>
      <p class="text-white/30 text-sm mt-1">NASA APOD started June 16, 1995</p>
    </div>
  {/if}
</div>
