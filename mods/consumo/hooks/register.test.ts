import { test, expect } from 'claude-code/testing'

test('consumo pane renders the five cards', async $ => {
  const ui = await $.ui.mount({
    plugin: 'consumo',
    surface: 'terminal',
    component: 'Pane',
    requestId: 'consumo',
    props: { title: 'Consumo', isFocused: false, bodyColumns: 40 },
  } as any)
  for (const label of ['TOKENS', 'GASTO', 'CONTEXTO', 'HERRAMIENTAS', 'SESIÓN']) {
    expect(await ui.find({ type: 'Text', text: label })).toBeDefined()
  }
  await ui.unmount()
})
