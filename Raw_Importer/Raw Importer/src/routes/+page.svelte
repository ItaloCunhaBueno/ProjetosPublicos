<script>
  import { Button } from "$lib/components/ui/button/index.js";
  import { Command } from "@tauri-apps/plugin-shell";
  import { convertFileSrc } from "@tauri-apps/api/core";
  import { exists, copyFile, mkdir } from "@tauri-apps/plugin-fs";
  import { image } from "@tauri-apps/api";
  import { Input } from "$lib/components/ui/input/index.js";
  import { Switch } from "$lib/components/ui/switch/index.js";
  import { toast } from "svelte-sonner";
  import { open } from "@tauri-apps/plugin-dialog";
  import {
    readDate,
    generatePreview,
    readOrientation,
    pathVerify,
    readFiles,
    processaHora,
    deletePreviews,
  } from "$lib/funcoes.svelte.js";
  import * as Alert from "$lib/components/ui/alert/index.js";
  import * as AlertDialog from "$lib/components/ui/alert-dialog/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import * as path from "@tauri-apps/api/path";
  import ColorToggle from "$lib/components/colorToggle.svelte";
  import LucideLoader from "~icons/lucide/loader";
  import LucideSearch from "~icons/lucide/search";
  import LucideTrash2 from "~icons/lucide/trash-2";
  import Progress from "$lib/components/ui/progress/progress.svelte";
  import DateChoose from "$lib/components/dateChoose.svelte";
  import LucideFolderInput from "~icons/lucide/folder-input";
  import LucideFolderOutput from "~icons/lucide/folder-output";
  import LucideCalendarSearch from "~icons/lucide/calendar-search";

  let pasta_entrada = $state("");
  let pasta_saida = $state("");
  let cria_ano = $state(true);
  let logs = $state([]);
  let executando = $state(false);
  let progresso = $state(0);
  let lendoInformacoes = $state(false);
  let datas = $state([]);
  let datas_selecionadas = $state([]);
  let arquivos = $state(undefined);

  let imageData = $state({
    caminho: undefined,
    nome: undefined,
    preview: undefined,
    data: undefined,
    orientacao: undefined,
  });

  let cardStyle = $derived(
    `background-image:url(${convertFileSrc(imageData.preview)}); rotate: z ${imageData.orientacao}deg;`
  );

  const scrollToBottom = (node) => {
    const scroll = () =>
      node.scroll({
        top: node.scrollHeight,
        behavior: "smooth",
      });
    scroll();

    return { update: scroll };
  };

  async function pick_folder(variavel) {
    const caminho = await open({
      multiple: false,
      directory: true,
    });
    if (caminho) {
      if (variavel == "pasta_entrada") {
        pasta_entrada = caminho;
      } else {
        pasta_saida = caminho;
      }
    }
    return;
  }

  $effect(async () => {
    if (pasta_entrada && (await pathVerify(pasta_entrada))) {
      lendoInformacoes = true;
      arquivos = await readFiles(pasta_entrada);
      lendoInformacoes = false;
    }
  });

  $effect(async () => {
    if (arquivos) {
      datas = Object.keys(arquivos);
    }
  });

  async function getInfos(caminho) {
    let obj = {};
    await Promise.all([
      generatePreview(caminho),
      readDate(caminho),
      readOrientation(caminho),
    ]).then((values) => {
      obj = {
        caminho: caminho,
        nome: values[0][0],
        preview: values[0][1],
        data: values[1],
        orientacao: values[2],
      };
    });
    return obj;
  }

  function limpaLogs() {
    logs = [];
  }

  async function executar() {
    if (
      !pasta_entrada ||
      !pasta_saida ||
      !pathVerify(pasta_entrada) ||
      !pathVerify(pasta_saida)
    ) {
      toast.error("Pastas inválidas!");
      return;
    }

    if (datas_selecionadas.length == 0) {
      toast.error("Nenhuma data selecionada!");
      return;
    }

    executando = true;
    progresso = 0;
    imageData = {
      caminho: undefined,
      nome: undefined,
      preview: undefined,
      data: undefined,
      orientacao: undefined,
    };
    let hora_inicial = performance.now();
    let qtd_copiadas = 0;

    let arquivos_filtrados = {};
    for (const data of datas_selecionadas) {
      arquivos_filtrados = { ...arquivos_filtrados, ...arquivos[data] };
    }

    try {
      let qtd_arquivos = Object.keys(arquivos_filtrados).length;
      let indice = 1;
      let previews = [];

      logs.push("Iniciando importação...");

      for (const [key, value] of Object.entries(arquivos_filtrados)) {
        let filepath = value.foto;
        let xmppath = value.xmp;
        let caminhoPastaSaida = pasta_saida;

        if (filepath) {
          const imageInfo = await getInfos(filepath);
          imageData = imageInfo;
          previews.push(imageInfo.preview);

          const filename = await path.basename(filepath);
          const filedate = imageInfo.data.split(" ")[0];
          const filedateyear = filedate.slice(0, 4);

          if (cria_ano) {
            caminhoPastaSaida = await path.join(
              caminhoPastaSaida,
              filedateyear
            );
          }
          caminhoPastaSaida = await path.join(caminhoPastaSaida, filedate);

          if (!(await exists(caminhoPastaSaida))) {
            await mkdir(caminhoPastaSaida, { recursive: true });
          }
          const caminho_saida_foto = await path.join(
            caminhoPastaSaida,
            filename
          );
          logs.push(`Copiando ${filename}...`);
          await copyFile(filepath, caminho_saida_foto);
          if (xmppath) {
            const xmpname = await path.basename(xmppath);
            const caminho_saida_xmp = await path.join(
              caminhoPastaSaida,
              xmpname
            );
            await copyFile(xmppath, caminho_saida_xmp);
          }
          qtd_copiadas += 1;
        }
        progresso = (indice / qtd_arquivos) * 100;
        indice += 1;
      }
      await deletePreviews(previews);
      imageData = {
        caminho: undefined,
        nome: undefined,
        preview: undefined,
        data: undefined,
        orientacao: undefined,
      };
    } catch (error) {
      console.log(error);
      toast.error(error);
    }

    let hora_final = performance.now();
    let tempo_execucao = processaHora(hora_final - hora_inicial);
    logs.push(`${qtd_copiadas} fotos copiadas em: ${tempo_execucao}`);
    executando = false;
  }
</script>

<div class="flex overflow-auto relative flex-col gap-2 p-2 w-full h-dvh">
  <ColorToggle class="absolute top-4 right-4 text-primary" />
  <Card.Root>
    <Card.Header>
      <Card.Title>Entradas</Card.Title>
    </Card.Header>
    <Card.Content class="flex flex-col gap-2">
      <div class="flex gap-2 items-center w-full">
        <LucideFolderInput class="size-6 text-muted-foreground" />
        <Input placeholder="Pasta de entrada" bind:value={pasta_entrada} />
        <Button
          variant="outline"
          class="text-primary"
          disabled={executando}
          onclick={() => pick_folder("pasta_entrada")}
        >
          <LucideSearch /> PROCURAR
        </Button>
      </div>
      <div class="flex gap-2 items-center w-full">
        <LucideFolderOutput class="size-6 text-muted-foreground" />
        <Input placeholder="Pasta de saída" bind:value={pasta_saida} />
        <Button
          variant="outline"
          class="text-primary"
          disabled={executando}
          onclick={() => pick_folder("pasta_saida")}
        >
          <LucideSearch /> PROCURAR
        </Button>
      </div>
      <div class="flex gap-2 items-center w-full">
        <LucideCalendarSearch class="size-6 text-muted-foreground" />
        <DateChoose bind:values={datas} bind:selected={datas_selecionadas} />
        <div
          class="flex gap-2 items-center p-2 w-64 rounded-md border transition-all hover:bg-border"
        >
          <Switch id="gerar_ano" bind:checked={cria_ano} />
          <label for="gerar_ano" class="text-sm hover:cursor-pointer"
            >Criar pasta do ano</label
          >
        </div>
      </div>
    </Card.Content>
  </Card.Root>
  {#if executando}
    <Button disabled={true}>
      <LucideLoader class="animate-spin" />
    </Button>
  {:else}
    <Button
      onclick={async () => {
        await executar();
      }}
      disabled={false}>EXECUTAR</Button
    >
  {/if}
  <Progress value={progresso} max={100} />

  <ul
    class="flex overflow-auto relative flex-col flex-1 gap-1 pb-2 w-full rounded-lg border shadow-md bg-muted"
    use:scrollToBottom={logs}
  >
    <div
      class="flex sticky top-0 justify-between items-center px-2 py-1 w-full bg-muted"
    >
      <p class="text-muted-foreground">Mensagens:</p>
      <Button
        disabled={executando}
        variant="ghost"
        class="m-0 text-primary"
        onclick={limpaLogs}
      >
        <LucideTrash2 /> LIMPAR
      </Button>
    </div>
    {#each logs as log}
      <li class="px-2 w-full text-sm text-muted-foreground">{log}</li>
    {/each}
  </ul>
  {#key imageData}
    {#if imageData?.preview && imageData?.data}
      <Alert.Root
        class="absolute right-4 bottom-4 z-50 p-2 ml-auto rounded-lg transition-all w-fit hover:right-6"
      >
        <Alert.Description class="flex gap-2 items-center rounded-lg w-fit">
          <div
            class="overflow-hidden max-h-28 bg-center bg-no-repeat bg-contain rounded-md transition-all min-w-28 min-h-28 max-w-28 aspect-square bg-border"
            style={cardStyle}
          ></div>
          <div
            class="flex flex-col gap-2 justify-around items-start h-full w-fit"
          >
            <Alert.Title class="rounded-lg">Importando...</Alert.Title>
            <p class="text-muted-foreground">Nome: {imageData.nome}</p>
            <p class="text-muted-foreground">
              Data: {imageData.data}
            </p>
          </div>
        </Alert.Description>
      </Alert.Root>
    {/if}
  {/key}
</div>

<AlertDialog.Root open={lendoInformacoes}>
  <AlertDialog.Content trapFocus={false}>
    <AlertDialog.Header>
      <AlertDialog.Title>Analisando datas...</AlertDialog.Title>
      <AlertDialog.Description>
        <p>Coletando informações de data.</p>
      </AlertDialog.Description>
      <div class="flex gap-2 justify-center items-center w-full">
        <LucideLoader class="animate-spin" />
      </div>
    </AlertDialog.Header>
  </AlertDialog.Content>
</AlertDialog.Root>
