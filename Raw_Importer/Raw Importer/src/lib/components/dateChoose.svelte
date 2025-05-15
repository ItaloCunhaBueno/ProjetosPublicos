<script>
  import * as CommandUI from "$lib/components/ui/command/index.js";
  import * as Select from "$lib/components/ui/select/index.js";
  import { Checkbox } from "$lib/components/ui/checkbox/index.js";
  import { Label } from "$lib/components/ui/label/index.js";

  let { values = $bindable([]), selected = $bindable([]) } = $props();
</script>

<Select.Root type="single" disabled={values.length < 1}>
  <Select.Trigger class="w-full">Selecione uma ou mais datas</Select.Trigger>
  <Select.Content>
    <CommandUI.Root>
      <CommandUI.Input placeholder="Procurar" />
      <CommandUI.List>
        <CommandUI.Empty>Nenhuma data encontrada.</CommandUI.Empty>
        {#if values.length > 1}
          <CommandUI.Item>
            <Checkbox
              id="todas"
              checked={selected == values}
              onCheckedChange={(e) => {
                if (e) {
                  selected = values;
                } else {
                  selected = [];
                }
              }}
            />
            <Label for="todas">Todas as datas</Label>
          </CommandUI.Item>
        {/if}

        {#each values as data}
          <CommandUI.Item>
            <Checkbox
              id={data}
              checked={selected.includes(data)}
              onCheckedChange={(e) => {
                if (e) {
                  selected.push(data);
                } else {
                  selected = selected.filter((item) => item !== data);
                }
              }}
            />
            <Label for={data}>{data}</Label>
          </CommandUI.Item>
        {/each}
      </CommandUI.List>
    </CommandUI.Root>
  </Select.Content>
</Select.Root>
