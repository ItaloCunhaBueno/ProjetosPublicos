<script>
	import * as Card from '$lib/components/ui/card/index.js';
	import Progress from '$lib/components/ui/progress/progress.svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import LucideCirclePlus from '~icons/lucide/circle-plus';
	import * as Dialog from '$lib/components/ui/dialog/index.js';

	let openNovoObjetivo = $state(false);
	let informacoes = $state({
		objetivos: [
			{
				titulo: 'Objetivo 1',
				descricao: 'Descrição do objetivo 1',
				guardado: 250,
				meta: 2000
			},
			{
				titulo: 'Objetivo 2',
				descricao: 'Descrição do objetivo 2',
				guardado: 150,
				meta: 15000
			},
			{
				titulo: 'Objetivo 3',
				descricao: 'Descrição do objetivo 3',
				guardado: 1000,
				meta: 10000
			}
		]
	});
</script>

<Dialog.Root bind:open={openNovoObjetivo}>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>Are you sure absolutely sure?</Dialog.Title>
			<Dialog.Description>This action cannot be undone. This will permanently delete your account and remove your data from our servers.</Dialog.Description>
		</Dialog.Header>

		<Dialog.Footer>
			<Button variant="ghost">Salvar</Button>
			<Button variant="destructive" onclick={() => (openNovoObjetivo = false)}>Cancelar</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>

<Card.Root class="m-0 flex h-full max-h-full w-full max-w-full flex-col overflow-auto">
	<Card.Content class="flex justify-between gap-2">
		<Card.Title>Objetivos:</Card.Title>
		<Button onclick={() => (openNovoObjetivo = true)}><LucideCirclePlus /> Novo Objetivo</Button>
	</Card.Content>
	<Card.Content class="flex flex-1 flex-wrap gap-4 overflow-auto">
		{#each informacoes.objetivos as objetivo}
			<Card.Root title="Editar" class="flex max-h-72 w-auto min-w-72 flex-1 flex-col bg-border transition-all hover:scale-105 hover:cursor-pointer">
				<Card.Content class="flex flex-1 flex-col justify-between gap-2">
					<div class="flex w-full flex-col gap-0">
						<Card.Title>{objetivo.titulo}</Card.Title>
						<Card.Description>{objetivo.descricao}</Card.Description>
					</div>
					<p class="w-full text-right text-2xl font-bold text-green-500">R$ {objetivo.guardado.toFixed(2)}</p>
					<div>
						<p class="w-full text-right text-sm text-muted-foreground">Meta: R$ {objetivo.meta.toFixed(2)}</p>
						<Progress value={(objetivo.guardado / objetivo.meta) * 100} />
					</div>
				</Card.Content>
			</Card.Root>
		{/each}
	</Card.Content>
</Card.Root>
