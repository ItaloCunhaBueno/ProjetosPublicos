<script>
	import { Description } from '$lib/components/ui/alert';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import LucideTrendingDown from '~icons/lucide/trending-down';
	import LucideTrendingUp from '~icons/lucide/trending-up';
	import autoAnimate from '@formkit/auto-animate';
	import Progress from '$lib/components/ui/progress/progress.svelte';
	import * as path from '@tauri-apps/api/path';
	import { exists } from '@tauri-apps/plugin-fs';
	import { Command } from '@tauri-apps/plugin-shell';

	let informacoes = $state({
		saldo: 0,
		despesas: [
			{
				descricao: 'Alimentação',
				valor: 100,
				data: new Date()
			},
			{
				descricao: 'Alimentação',
				valor: 100,
				data: new Date()
			},
			{
				descricao: 'Alimentação',
				valor: 100,
				data: new Date()
			},
			{
				descricao: 'Alimentação',
				valor: 100,
				data: new Date()
			}
		],
		receitas: [
			{
				descricao: 'Salário',
				valor: 2000,
				data: new Date()
			},
			{
				descricao: 'Salário',
				valor: 2000,
				data: new Date()
			},
			{
				descricao: 'Salário',
				valor: 2000,
				data: new Date()
			}
		],
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

<Card.Root class="flex flex-col w-full max-w-full overflow-auto">
	<Card.Content class="flex flex-col gap-2">
		<Card.Title>Balanço:</Card.Title>
		{#if informacoes.saldo < 0}
			<p class="flex items-center gap-2 text-2xl font-bold text-destructive"><LucideTrendingDown />R$ {informacoes.saldo.toFixed(2)}</p>
		{:else}
			<p class="flex items-center gap-2 text-2xl font-bold text-green-500"><LucideTrendingUp />R$ {informacoes.saldo.toFixed(2)}</p>
		{/if}
	</Card.Content>

	<Card.Content class="flex flex-1 flex-col justify-center gap-2">
		<div class="flex max-h-[350px] flex-1 gap-2">
			<div class="flex flex-1 flex-col gap-2 border-y p-4">
				<Card.Title>Últimas receitas</Card.Title>
				<ul class="flex flex-col gap-1 overflow-auto" use:autoAnimate>
					{#each informacoes.receitas as receita}
						<li class="flex flex-wrap items-center justify-between gap-2 rounded-lg bg-border px-4 py-2 shadow-sm">
							<div class="flex flex-col gap-0">
								<p class="text-sm font-bold text-muted-foreground">{receita.descricao}</p>
								<p class="text-sm text-muted-foreground">{receita.data.toLocaleDateString('pt-BR')}</p>
							</div>
							<p class="text-nowrap text-sm font-bold text-green-500">+ R$ {receita.valor.toFixed(2)}</p>
						</li>
					{/each}
				</ul>
			</div>
			<div class="flex flex-1 flex-col gap-2 border-y p-4">
				<Card.Title>Últimas despesas</Card.Title>
				<ul class="flex flex-col gap-1 overflow-auto" use:autoAnimate>
					{#each informacoes.despesas as despesa}
						<li class="flex flex-wrap items-center justify-between gap-2 rounded-lg bg-border px-4 py-2 shadow-sm">
							<div class="flex flex-col gap-0">
								<p class="text-sm font-bold text-muted-foreground">{despesa.descricao}</p>
								<p class="text-sm text-muted-foreground">{despesa.data.toLocaleDateString('pt-BR')}</p>
							</div>
							<p class="text-nowrap text-sm font-bold text-red-500">- R$ {despesa.valor.toFixed(2)}</p>
						</li>
					{/each}
				</ul>
			</div>
		</div>
		<div class="flex h-min flex-1 flex-col gap-2">
			<Card.Title>Objetivos</Card.Title>
			<ul class="flex gap-2 overflow-auto" use:autoAnimate>
				{#each informacoes.objetivos as objetivo}
					<li class="relative flex min-w-[250px] max-w-sm flex-col gap-2 rounded-lg bg-border p-4 shadow-sm">
						<div class="flex flex-col gap-0">
							<Card.Title class="text-lg">{objetivo.titulo}</Card.Title>
							<Card.Description>{objetivo.descricao}</Card.Description>
							<p class="text-sm text-muted-foreground">Meta: R$ {objetivo.meta.toFixed(2)}</p>
						</div>

						<p class="mt-4 w-full text-right text-xl font-bold text-green-500">R$ {objetivo.guardado.toFixed(2)}</p>
						<Progress value={(objetivo.guardado / objetivo.meta) * 100} max="100" />
					</li>
				{/each}
			</ul>
		</div>
	</Card.Content>
</Card.Root>
