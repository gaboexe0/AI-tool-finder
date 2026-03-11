import argparse
import sys
import io
from src.tool_finder import ToolFinder

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║            🤖 AI Tool Finder - Developer Search            ║
║                                                           ║
║   Search npm, GitHub, StackOverflow and more...          ║
║   Type natural language queries like:                    ║
║   • "paquetes npm para autenticación"                    ║
║   • "github repos de machine learning"                    ║
║   • "como usar async await en javascript"                ║
║                                                           ║
║   Commands:                                               ║
║   • Just type to search                                   ║
║   • --exit to quit                                        ║
║   • --help to see options                                 ║
╚═══════════════════════════════════════════════════════════╝
"""


def show_banner():
    print(BANNER)


def show_quota(finder: ToolFinder):
    quota = finder.get_quota_status()
    print(
        f"\n📊 Quota: {quota['count']}/100 used | {quota['remaining']} remaining today\n"
    )


def interactive_search(finder: ToolFinder):
    show_banner()
    show_quota(finder)
    print("[+] Ready to search! Type your query in natural language.\n")

    while True:
        try:
            query = input("🔍 > ").strip()

            if not query:
                continue

            if query.lower() in ["--exit", "exit", "quit", "q", "salir"]:
                print("\n👋 Thanks for using AI Tool Finder!")
                break

            if query.lower() == "--help":
                print_help()
                continue

            if query.lower() == "--quota":
                show_quota(finder)
                continue

            search_natural(finder, query)
            show_quota(finder)

        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using AI Tool Finder!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def truncate_snippet(text: str, max_length: int = 80) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."


def search_natural(finder: ToolFinder, query: str, show_quota_flag: bool = True):
    print(f'\nSearching for: "{query}"...\n')

    npm_results = finder.search_npm(query, 3)
    github_results = finder.search_github(query, 3)
    stackoverflow_results = finder.search_stackoverflow(query, 3)

    if isinstance(npm_results, dict) and "error" in npm_results:
        print(f"❌ NPM Error: {npm_results['error']}")
    elif npm_results:
        print("─" * 60)
        print("📦 NPM PACKAGES")
        print("─" * 60)
        for i, item in enumerate(npm_results, 1):
            print(f"\n  {i}. {item['title']}")
            print(f"     🔗 {item['link']}")
            snippet = truncate_snippet(item.get("snippet", ""))
            print(f"     📝 {snippet}")

    if isinstance(github_results, dict) and "error" in github_results:
        print(f"❌ GitHub Error: {github_results['error']}")
    elif github_results:
        print("\n" + "─" * 60)
        print("🐙 GITHUB REPOSITORIES")
        print("─" * 60)
        for i, item in enumerate(github_results, 1):
            print(f"\n  {i}. {item['title']}")
            print(f"     🔗 {item['link']}")
            snippet = truncate_snippet(item.get("snippet", ""))
            print(f"     📝 {snippet}")

    if isinstance(stackoverflow_results, dict) and "error" in stackoverflow_results:
        print(f"❌ StackOverflow Error: {stackoverflow_results['error']}")
    elif stackoverflow_results:
        print("\n" + "─" * 60)
        print("💬 STACKOVERFLOW QUESTIONS")
        print("─" * 60)
        for i, item in enumerate(stackoverflow_results, 1):
            print(f"\n  {i}. {item['title']}")
            print(f"     🔗 {item['link']}")
            snippet = truncate_snippet(item.get("snippet", ""))
            print(f"     📝 {snippet}")

    if not npm_results and not github_results and not stackoverflow_results:
        print("❌ No results found.\n")

    if show_quota_flag:
        quota = finder.get_quota_status()
        print(
            f"\n📊 Quota: {quota['count']}/100 used | {quota['remaining']} remaining today"
        )

    print()


def print_help():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                      COMMANDS                              ║
╠═══════════════════════════════════════════════════════════╣
║   Just type your search query in natural language!        ║
║                                                           ║
║   Examples:                                               ║
║   • "react hooks library"                                 ║
║   • "python async http client"                            ║
║   • "nodejs oauth authentication"                         ║
║   • "javascript pdf generator"                            ║
║                                                           ║
║   Special commands:                                        ║
║   • exit, quit, q    - Exit the program                   ║
║   • --help          - Show this help                      ║
╚═══════════════════════════════════════════════════════════╝
""")


def main():
    parser = argparse.ArgumentParser(
        description="AI Tool Finder - Developer Search CLI", add_help=False
    )
    parser.add_argument("--init", action="store_true", help="Start interactive mode")
    parser.add_argument("--search", type=str, help="Single search query")
    parser.add_argument("--help", action="store_true", help="Show help")

    args = parser.parse_args()

    if args.help:
        print_help()
        return

    try:
        finder = ToolFinder()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nGet your free API key at: https://serpapi.com/")
        print("Then set it in .env.example file.")
        sys.exit(1)

    if args.search:
        search_natural(finder, args.search)
    else:
        interactive_search(finder)


if __name__ == "__main__":
    main()
