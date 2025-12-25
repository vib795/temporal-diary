<script lang="ts">
  import { onMount } from 'svelte';

  let stars: Array<{ x: number; y: number; size: number; opacity: number; delay: number }> = [];

  onMount(() => {
    stars = Array.from({ length: 100 }, () => ({
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 2 + 1,
      opacity: Math.random() * 0.5 + 0.3,
      delay: Math.random() * 3,
    }));
  });
</script>

<div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
  <!-- Gradient background -->
  <div class="absolute inset-0 bg-gradient-to-b from-slate-950 via-purple-950/20 to-slate-950" />

  <!-- Nebula effects -->
  <div
    class="absolute top-0 left-1/4 w-[500px] h-[500px] bg-purple-500/10 rounded-full blur-[100px] animate-pulse-slow"
  />
  <div
    class="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-blue-500/10 rounded-full blur-[100px] animate-pulse-slow"
    style="animation-delay: 2s;"
  />
  <div
    class="absolute top-1/2 left-1/2 w-[300px] h-[300px] bg-pink-500/5 rounded-full blur-[80px] animate-pulse-slow"
    style="animation-delay: 4s;"
  />

  <!-- Stars -->
  <svg class="absolute inset-0 w-full h-full">
    {#each stars as star}
      <circle
        cx="{star.x}%"
        cy="{star.y}%"
        r={star.size}
        fill="white"
        opacity={star.opacity}
        class="animate-twinkle"
        style="animation-delay: {star.delay}s;"
      />
    {/each}
  </svg>
</div>

<style>
  @keyframes twinkle {
    0%,
    100% {
      opacity: var(--tw-opacity);
    }
    50% {
      opacity: calc(var(--tw-opacity) * 0.3);
    }
  }

  .animate-twinkle {
    animation: twinkle 3s ease-in-out infinite;
  }
</style>
