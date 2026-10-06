export type Snapshot = {
  tokens: number
  usd: number
  percent: number
  window: number
  startedAt: number
  now: number
  tools: number
  recent: string[]
  working: boolean
}

declare module 'claude-code' {
  interface PluginState {
    consumo: { snap: Snapshot }
  }
}
