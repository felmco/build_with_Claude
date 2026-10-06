"""Customer support chatbot: command-line REPL.

    python main.py                 # chat with Claude (needs ANTHROPIC_API_KEY)
    python main.py --dry-run       # offline demo, no API calls
Commands inside the chat: /help  /stats  /reset  /quit
"""
from __future__ import annotations

import argparse
import os
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv

from support_bot.analytics import AnalyticsLog, format_stats, summarize
from support_bot.bot import InputRejected, SupportBot, sanitize_input
from support_bot.tools import SupportTools

HERE = Path(__file__).parent


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Customer support chatbot (Claude, streaming, tools, caching).")
    p.add_argument("--model", default="claude-sonnet-5-5", help="model ID (default: %(default)s)")
    p.add_argument("--max-tokens", type=int, default=1024, help="max output tokens per API call")
    p.add_argument("--effort", choices=["low", "medium", "high"], default=None,
                   help="output_config.effort (not for claude-haiku-4-5); 'low' is good for simple chat")
    p.add_argument("--kb", default=str(HERE / "data" / "kb.json"), help="knowledge-base JSON file")
    p.add_argument("--tickets", default=str(HERE / "data" / "tickets.jsonl"), help="where tickets are appended")
    p.add_argument("--log", default=str(HERE / "logs" / "analytics.jsonl"), help="analytics JSONL file")
    p.add_argument("--max-history", type=int, default=40, help="max messages kept in history")
    p.add_argument("--dry-run", action="store_true", help="offline demo: no API key, no network")
    return p


def handle_command(cmd: str, bot: SupportBot, log: AnalyticsLog, session_id: str) -> bool:
    """Return True if the REPL should exit."""
    if cmd in ("/quit", "/exit"):
        return True
    if cmd == "/reset":
        bot.reset()
        print("Conversation reset.")
    elif cmd == "/stats":
        rows = log.rows()
        print(format_stats("All time", summarize(rows)))
        print(format_stats("This session", summarize([r for r in rows if r.get("session") == session_id])))
    else:
        print("Commands: /stats (usage and cost), /reset (new conversation), /quit")
    return False


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    load_dotenv()
    if args.dry_run:
        from support_bot.offline import OfflineClient
        client = OfflineClient()
    else:
        if not os.getenv("ANTHROPIC_API_KEY"):
            print("ANTHROPIC_API_KEY is not set (see .env.example). Use --dry-run to try the bot offline.",
                  file=sys.stderr)
            return 2
        import anthropic
        client = anthropic.Anthropic()  # SDK retries 429/5xx automatically (max_retries=2)

    session_id = uuid.uuid4().hex[:8]
    log = AnalyticsLog(args.log, session=session_id)
    bot = SupportBot(client, SupportTools(args.kb, args.tickets), model=args.model,
                     max_tokens=args.max_tokens, effort=args.effort, analytics=log,
                     max_history_messages=args.max_history)

    print(f"Support bot ready ({'offline demo' if args.dry_run else args.model}). Type /help for commands.")
    while True:
        try:
            line = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.startswith("/"):
            if handle_command(line.lower(), bot, log, session_id):
                break
            continue
        try:
            line = sanitize_input(line)  # validate before printing the "Aria:" prompt
        except InputRejected as e:
            print(e)
            continue
        print("Aria: ", end="", flush=True)
        res = bot.ask(line, on_text=lambda t: print(t, end="", flush=True))
        print()
        if res.notice:
            print(f"[{res.notice}]")
        if bot.tools.escalated:
            print("[A human agent has been notified and will take over.]")
            bot.tools.escalated = False
    u = bot.session_usage
    print(f"Session usage: {u.calls} calls, in={u.input} out={u.output} cache_read={u.cache_read} "
          f"cache_write={u.cache_write}, estimated cost ${u.cost(args.model):.4f} (estimate)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
