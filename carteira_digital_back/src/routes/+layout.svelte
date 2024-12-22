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

<main class="flex h-dvh max-h-[100dvh] w-dvw max-w-[100dvw]">
	<Sidebar.Provider>
		<AppSidebar />
		<main class="max-h-full max-w-full flex-1 flex-col p-2">
			{@render children?.()}
		</main>
	</Sidebar.Provider>
</main>
