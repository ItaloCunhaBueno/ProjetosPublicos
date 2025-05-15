<script>
  import { toggleMode, mode } from "mode-watcher";
  import Button from "./ui/button/button.svelte";
  import LucideMoonStar from "~icons/lucide/moon-star";
  import LucideSun from "~icons/lucide/sun";

  let { class: ClassName, variant = "outline" } = $props();
</script>

<Button {variant} size="icon" onclick={toggleMode} class={ClassName}>
  {#if $mode == "dark"}
    <LucideMoonStar />
  {:else}
    <LucideSun />
  {/if}
</Button>
