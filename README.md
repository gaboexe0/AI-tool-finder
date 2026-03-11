# 🔍 AI Tool Finder CLI

Find npm packages, GitHub repos, and StackOverflow answers — all from your terminal, ranked by relevance. Powered by [SerpApi](https://serpapi.com).

Stop context-switching to a browser every time you need to discover a library. Stay in your terminal, stay in flow.

---

## Demo

```
╔═══════════════════════════════════════════════════════════╗
║            🤖 AI Tool Finder - Developer Search            ║
║                                                           ║
║   Search npm, GitHub, StackOverflow and more...          ║
║   Type natural language queries like:                    ║
║   • "react authentication library"                       ║
║   • "python async http client"                           ║
║   • "how to use async await in javascript"               ║
╚═══════════════════════════════════════════════════════════╝

🔍 > next.js components

Searching for: "next.js components"...

────────────────────────────────────────────────────────────
📦 NPM PACKAGES
────────────────────────────────────────────────────────────

  1. robust-ui/nextjs-components
     🔗 https://www.npmjs.com/package/@robust-ui/nextjs-components
     📝 The Main component sets the color and font family...

────────────────────────────────────────────────────────────
🐙 GITHUB REPOSITORIES
────────────────────────────────────────────────────────────

  1. vercel/next.js
     🔗 https://github.com/vercel/next.js
     📝 The React Framework for the Web...

────────────────────────────────────────────────────────────
💬 STACKOVERFLOW QUESTIONS
────────────────────────────────────────────────────────────

  1. How to create reusable components in Next.js?
     🔗 https://stackoverflow.com/questions/...
     📝 I want to create a reusable button component...
```

---

## Why I Built This

As a developer, I kept running into the same friction: I'd be deep in a coding session, need to find a library, and lose 10 minutes jumping between npmjs.com, GitHub search, and StackOverflow tabs.

The problem isn't that the information doesn't exist — it's that it's scattered across three different surfaces with three different search UIs. I wanted one interface that queries all three at once and brings back the top results, ranked by relevance.

SerpApi was the right tool for this. Instead of scraping each site manually or dealing with rate limits across multiple APIs, SerpApi handles the heavy lifting — CAPTCHAs, layout changes, result ranking — in a single call per source.

---

## Installation

**1. Clone the repo**
```bash
git clone https://github.com/gaboexe0/ai-tool-finder.git
cd ai-tool-finder
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your SerpApi key**
```bash
cp .env.example .env
# Add your key to .env
```
Get your free API key at [serpapi.com/manage-api-key](https://serpapi.com/manage-api-key)

---

## Usage

**Interactive mode** (default — just run it and start typing):
```bash
python main.py
```

**Single query mode:**
```bash
python main.py --search "vector database python"
```

**Natural language works:**
```bash
🔍 > python packages for sending emails
🔍 > github repos for building CLI tools
🔍 > how to handle JWT authentication in express
```

**Special commands inside interactive mode:**
```
--help    Show available commands
--exit    Quit (or just Ctrl+C)
```

---

## How It Works

Each query runs 3 parallel SerpApi searches with site-specific targeting:

| Source | What it finds |
|--------|--------------|
| 📦 **npm** | Packages ranked by download popularity and relevance |
| 🐙 **GitHub** | Repositories ranked by stars and activity |
| 💬 **StackOverflow** | Questions ranked by votes and answers |

Results are capped at **3 per source** — enough signal, no noise.

---

## Project Structure

```
ai-tool-finder/
├── main.py           # CLI entry point, interactive loop, argument parsing
├── src/
│   └── tool_finder.py  # SerpApi integration, search logic per source
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Extending It

Some directions worth exploring:

- **PyPI search** — add Python package search alongside npm
- **Filter by language** — `--lang python` to filter GitHub results
- **Save searches** — persist a local history of queries
- **Export to JSON** — `--json` flag to pipe results into other scripts
- **Slack bot wrapper** — post results directly to a channel

PRs welcome.

---

## Tech Stack

- Python 3.8+
- [SerpApi](https://serpapi.com) — handles scraping, CAPTCHAs, and result ranking across sources
- `python-dotenv` — environment variable management
- `requests` — HTTP client

---

## Author

**Gabriel** — Co-founder of a Slack-native software agency. Building at the intersection of APIs, developer communities, and go-to-market.

- Newsletter: [Gabriel Queche](https://substack.com/@gabrielqueche)
- GitHub: [@gaboexe0](https://github.com/gaboexe0)

---

## License

MIT
