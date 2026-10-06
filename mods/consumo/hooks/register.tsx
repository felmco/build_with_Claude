import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Snapshot } from '../types'

const PANE = 'consumo'
const initial: Snapshot = {
  tokens: 0, usd: 0, percent: 0, window: 0,
  startedAt: 0, now: 0, tools: 0, recent: [], working: false,
}
const snap = atom({ plugin: 'consumo', key: 'snap' } as const, initial)

const clock = (ms: number) => {
  const s = Math.max(0, Math.floor(ms / 1000))
  const mm = String(Math.floor(s / 60)).padStart(2, '0')
  const ss = String(s % 60).padStart(2, '0')
  return `${mm}:${ss}`
}
const k = (n: number) => (n >= 1000 ? `${(n / 1000).toFixed(1)}k` : String(n))

let tools = 0
let recent: string[] = []
let working = false

async function refresh($: any) {
  const u = await $.session.usage()
  const now = await $.clock.now()
  await update($, snap, () => ({
    tokens: u.context.tokens ?? 0,
    usd: u.cost?.usd ?? 0,
    percent: u.context.percent ?? 0,
    window: u.context.window,
    startedAt: u.startedAt,
    now,
    tools,
    recent: recent.slice(-4),
    working,
  }))
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'consumo',
      description: 'Show live consumption: tokens, spend, context, tools, session time',
    })
    $.clock.every(1000, () => void refresh($))
    return next(e)
  })

  on('command.run', { command: 'consumo' }, async $ => {
    await refresh($)
    await $.ui.open({ id: PANE, title: 'Consumo' })
    return { text: 'Consumo pane opened.' }
  })

  on('prompt.submit', async ($, e, next) => {
    working = true
    void refresh($)
    return next(e)
  })

  on('tool.call', async ($, e, next) => {
    tools += 1
    recent = [...recent, e.tool]
    void refresh($)
    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    working = false
    await refresh($)
    return next(e)
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const s = await read($, snap)
    const accent = 'orange'
    const width = Math.max(10, (e.props.bodyColumns ?? 30) - 6)
    const filled = Math.round((Math.min(100, s.percent) / 100) * width)

    const Card = ({ label, value, tag }: { label: string; value: string; tag?: string }) => (
      <Box flexDirection="column" borderStyle="round" borderColor="gray" paddingX={1}>
        <Box justifyContent="space-between">
          <Text dimColor>{label.toUpperCase()}</Text>
          {tag && <Text dimColor>{tag.toUpperCase()}</Text>}
        </Box>
        <Text bold>{value}</Text>
      </Box>
    )

    return (
      <Box flexDirection="column" borderStyle="round" borderColor={accent} paddingX={1}>
        <Text bold color={accent}>CONSUMO {s.working ? '· trabajando' : ''}</Text>
        <Card label="Tokens" tag="último pedido" value={k(s.tokens)} />
        <Card label="Gasto" tag="API" value={`$${s.usd.toFixed(2)}`} />
        <Box flexDirection="column" borderStyle="round" borderColor="gray" paddingX={1}>
          <Text dimColor>CONTEXTO</Text>
          <Text bold>{Math.round(s.percent)}%</Text>
          <Text>
            <Text color={accent}>{'█'.repeat(filled)}</Text>
            <Text dimColor>{'░'.repeat(width - filled)}</Text>
          </Text>
        </Box>
        <Card label="Herramientas" value={String(s.tools)} />
        <Card label="Sesión" value={clock(s.now - s.startedAt)} />
        {s.recent.map(t => <Text dimColor>• {t}</Text>)}
      </Box>
    )
  })
}
