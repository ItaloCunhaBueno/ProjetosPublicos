<script>
	import '../app.css';
	import { ModeWatcher } from 'mode-watcher';
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import AppSidebar from '$lib/components/app-sidebar.svelte';

	let { children } = $props();
</script>

<ModeWatcher />
<Toaster />
<div class="flex gap-0 w-full h-full max-w-full max-h-full">
	<Sidebar.Provider class="flex w-full h-full max-w-full max-h-full overflow-hidden">
		<AppSidebar />
		<main class="flex-1 flex p-2 max-w-[100vw] max-h-[100vh]">
			{@render children?.()}
		</main>
	</Sidebar.Provider>
</div>
