<script>
	import { getTipos, addTipo, deleteTipo, updateTipo, getMetodos, addMetodo, deleteMetodo, updateMetodo } from '$lib/database.js';
	import { onMount } from 'svelte';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import Button from '$lib/components/ui/button/button.svelte';
	import Input from '$lib/components/ui/input/input.svelte';
	import LucideCirclePlus from '~icons/lucide/circle-plus';
	import LucideTrash2 from '~icons/lucide/trash-2';
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js';
	import LucideTriangleAlert from '~icons/lucide/triangle-alert';

	let dialogoAddTipo = $state(false);
	let tipoDialogoTipo = $state('');
	let valorDialogoTipo = $state('');
	let mensagemErroTipo = $state('');

	let dialogoAddMetodo = $state(false);
	let valorDialogoMetodo = $state('');
	let mensagemErroMetodo = $state('');

	let tiposReceita = $state([]);
	let tiposDespesa = $state([]);

	let metodos = $state([]);

	async function recarregarDados() {
		tiposReceita = await getTipos('receita');
		tiposDespesa = await getTipos('despesa');
		metodos = await getMetodos();
	}

	onMount(async () => {
		await recarregarDados();
	});
</script>

<Dialog.Root bind:open={dialogoAddTipo}>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>
				<span>Adicionar </span>
				<span class="capitalize">{tipoDialogoTipo}</span>
			</Dialog.Title>
		</Dialog.Header>
		<div class="flex flex-col gap-2">
			<Input bind:value={valorDialogoTipo} />
			{#if mensagemErroTipo}
				<p class="text-amber-500 text-sm flex items-center gap-1"><LucideTriangleAlert />{mensagemErroTipo}</p>
			{/if}
		</div>
		<Dialog.Footer>
			<Button variant="ghost" onclick={() => (dialogoAddTipo = false)}>Cancelar</Button>
			<Button
				onclick={async () => {
					mensagemErroTipo = '';
					const listaTiposReceita = tiposReceita.map((t) => t.tipo);
					const listaTiposDespesa = tiposDespesa.map((t) => t.tipo);

					if (valorDialogoTipo) {
						if (tipoDialogoTipo === 'receita') {
							if (listaTiposReceita.includes(valorDialogoTipo)) {
								mensagemErroTipo = 'Tipo de receita já existe.';
							} else {
								await addTipo(tipoDialogoTipo, valorDialogoTipo);
								await recarregarDados();
								dialogoAddTipo = false;
							}
						} else if (tipoDialogoTipo === 'despesa') {
							if (listaTiposDespesa.includes(valorDialogoTipo)) {
								mensagemErroTipo = 'Tipo de despesa já existe.';
							} else {
								await addTipo(tipoDialogoTipo, valorDialogoTipo);
								await recarregarDados();
								dialogoAddTipo = false;
							}
						}
					} else {
						mensagemErroTipo = 'O campo não pode estar vazio.';
					}
				}}>Adicionar</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>

<Dialog.Root bind:open={dialogoAddMetodo}>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>
				<span>Adicionar Método de Pagamento</span>
			</Dialog.Title>
		</Dialog.Header>
		<div class="flex flex-col gap-2">
			<Input bind:value={valorDialogoMetodo} />
			{#if mensagemErroMetodo}
				<p class="text-amber-500 text-sm flex items-center gap-1"><LucideTriangleAlert />{mensagemErroMetodo}</p>
			{/if}
		</div>
		<Dialog.Footer>
			<Button variant="ghost" onclick={() => (dialogoAddMetodo = false)}>Cancelar</Button>
			<Button
				onclick={async () => {
					mensagemErroMetodo = '';
					const listaMetodos = metodos.map((m) => m.metodo);
					if (valorDialogoMetodo) {
						if (listaMetodos.includes(valorDialogoMetodo)) {
							mensagemErroMetodo = 'Método de pagamento já existe.';
						} else {
							await addMetodo(valorDialogoMetodo);
							await recarregarDados();
							dialogoAddMetodo = false;
						}
					} else {
						mensagemErroMetodo = 'O campo não pode estar vazio.';
					}
				}}>Adicionar</Button>
		</Dialog.Footer>
	</Dialog.Content>
</Dialog.Root>

<Card.Root class="flex flex-col w-full max-w-full overflow-auto">
	<Card.Header>
		<Card.Title>Configurações:</Card.Title>
	</Card.Header>
	<Card.Content class="flex-shrink flex flex-col gap-4 w-full">
		<Card.Title class="w-full">Tipos:</Card.Title>
		<div class="w-full flex flex-wrap gap-4">
			<div class="flex-1 flex flex-col gap-2 !min-w-96">
				<p class="text-sm text-muted-foreground">Tipo de Receita:</p>
				<div class="flex flex-col max-h-56 rounded-lg border overflow-hidden bg-accent">
					<div class="sticky top-0 flex items-center justify-between w-full p-2">
						<span class="text-sm text-muted-foreground font-bold">Nome</span>
						<Button
							title="Adicionar"
							variant="ghost"
							class="text-green-500 text-sm"
							onclick={() => {
								tipoDialogoTipo = 'receita';
								dialogoAddTipo = true;
							}}>
							<LucideCirclePlus />
							Adicionar
						</Button>
					</div>
					<ul class="flex-1 flex flex-col overflow-auto">
						{#if tiposReceita.length > 0}
							{#each tiposReceita as tipo (tipo.id)}
								<li class="flex w-full min-w-fit items-center gap-2 pl-2 hover:bg-input transition-all">
									<Input
										value={tipo.tipo}
										onchange={async (e) => {
											await updateTipo(tipo.id, e.target.value);
											await recarregarDados();
										}}
										class="flex-1 border-none m-0 p-0 focus-visible:ring-0" />
									<AlertDialog.Root>
										<AlertDialog.Trigger>
											<Button size="icon" title="Deletar" variant="ghost" class="text-red-500">
												<LucideTrash2 />
											</Button>
										</AlertDialog.Trigger>
										<AlertDialog.Content>
											<AlertDialog.Header>
												<AlertDialog.Title>Tem certeza?</AlertDialog.Title>
												<AlertDialog.Description>Tem certeza que deseja deletar o tipo '{tipo.tipo}'?.</AlertDialog.Description>
											</AlertDialog.Header>
											<AlertDialog.Footer>
												<AlertDialog.Cancel>Cancelar</AlertDialog.Cancel>
												<Button
													variant="destructive"
													onclick={async () => {
														await deleteTipo(tipo.id);
														await recarregarDados();
													}}><LucideTrash2 /> Deletar</Button>
											</AlertDialog.Footer>
										</AlertDialog.Content>
									</AlertDialog.Root>
								</li>
							{/each}
						{:else}
							<p class="m-2 text-muted-foreground text-center">Nenhum tipo de receita adicionado.</p>
						{/if}
					</ul>
				</div>
			</div>
			<div class="flex-1 flex flex-col gap-2 !min-w-96">
				<p class="text-sm text-muted-foreground">Tipo de Despesa:</p>
				<div class="flex flex-col max-h-56 rounded-lg border overflow-hidden bg-accent">
					<div class="sticky top-0 flex items-center justify-between w-full p-2">
						<span class="text-sm text-muted-foreground font-bold">Nome</span>
						<Button
							title="Adicionar"
							variant="ghost"
							class="text-green-500 text-sm"
							onclick={() => {
								tipoDialogoTipo = 'despesa';
								dialogoAddTipo = true;
							}}>
							<LucideCirclePlus />
							Adicionar
						</Button>
					</div>
					<ul class="flex-1 flex flex-col overflow-auto">
						{#if tiposDespesa.length > 0}
							{#each tiposDespesa as tipo (tipo.id)}
								<li class="flex w-full min-w-fit pl-2 hover:bg-input transition-all">
									<Input
										value={tipo.tipo}
										onchange={async (e) => {
											await updateTipo(tipo.id, e.target.value);
											await recarregarDados();
										}}
										class="flex-1 border-none m-0 p-0 focus-visible:ring-0" />
									<AlertDialog.Root>
										<AlertDialog.Trigger>
											<Button size="icon" title="Deletar" variant="ghost" class="text-red-500">
												<LucideTrash2 />
											</Button>
										</AlertDialog.Trigger>
										<AlertDialog.Content>
											<AlertDialog.Header>
												<AlertDialog.Title>Tem certeza?</AlertDialog.Title>
												<AlertDialog.Description>Tem certeza que deseja deletar o tipo '{tipo.tipo}'?.</AlertDialog.Description>
											</AlertDialog.Header>
											<AlertDialog.Footer>
												<AlertDialog.Cancel>Cancelar</AlertDialog.Cancel>
												<Button
													variant="destructive"
													onclick={async () => {
														await deleteTipo(tipo.id);
														await recarregarDados();
													}}><LucideTrash2 /> Deletar</Button>
											</AlertDialog.Footer>
										</AlertDialog.Content>
									</AlertDialog.Root>
								</li>
							{/each}
						{:else}
							<p class="m-2 text-muted-foreground text-center">Nenhum tipo de despesa adicionado.</p>
						{/if}
					</ul>
				</div>
			</div>
		</div>
	</Card.Content>
	<Card.Content class="flex-shrink flex flex-col gap-4 w-full">
		<Card.Title class="w-full">Métodos:</Card.Title>
		<div class="w-full flex flex-wrap gap-4">
			<div class="flex-1 flex flex-col gap-2 !min-w-96">
				<p class="text-sm text-muted-foreground">Métodos de Pagamento:</p>
				<div class="flex flex-col max-h-56 rounded-lg border overflow-hidden bg-accent">
					<div class="sticky top-0 flex items-center justify-between w-full p-2">
						<span class="text-sm text-muted-foreground font-bold">Nome</span>
						<Button
							title="Adicionar"
							variant="ghost"
							class="text-green-500 text-sm"
							onclick={() => {
								dialogoAddMetodo = true;
							}}>
							<LucideCirclePlus />
							Adicionar
						</Button>
					</div>
					<ul class="flex-1 flex flex-col overflow-auto">
						{#if metodos.length > 0}
							{#each metodos as metodo (metodo.id)}
								<li class="flex w-full min-w-fit items-center gap-2 pl-2 hover:bg-input transition-all">
									<Input
										value={metodo.metodo}
										onchange={async (e) => {
											await updateMetodo(metodo.id, e.target.value);
											await recarregarDados();
										}}
										class="flex-1 border-none m-0 p-0 focus-visible:ring-0" />
									<AlertDialog.Root>
										<AlertDialog.Trigger>
											<Button size="icon" title="Deletar" variant="ghost" class="text-red-500">
												<LucideTrash2 />
											</Button>
										</AlertDialog.Trigger>
										<AlertDialog.Content>
											<AlertDialog.Header>
												<AlertDialog.Title>Tem certeza?</AlertDialog.Title>
												<AlertDialog.Description>Tem certeza que deseja deletar o método de pagamento '{metodo.metodo}'?.</AlertDialog.Description>
											</AlertDialog.Header>
											<AlertDialog.Footer>
												<AlertDialog.Cancel>Cancelar</AlertDialog.Cancel>
												<Button
													variant="destructive"
													onclick={async () => {
														await deleteMetodo(metodo.id);
														await recarregarDados();
													}}><LucideTrash2 /> Deletar</Button>
											</AlertDialog.Footer>
										</AlertDialog.Content>
									</AlertDialog.Root>
								</li>
							{/each}
						{:else}
							<p class="m-2 text-muted-foreground text-center">Nenhum método de pagamento adicionado.</p>
						{/if}
					</ul>
				</div>
			</div>
		</div>
	</Card.Content>
</Card.Root>
