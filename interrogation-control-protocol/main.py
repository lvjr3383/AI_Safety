import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from rich.console import Console
from harness import run_full_evaluation, print_summary_table, save_results

console = Console()


def main():
    console.print("\n[bold cyan]Interrogation Control Protocol — Evaluation Harness[/bold cyan]")
    console.print("[dim]Testing whether interrogation catches adversarial AI agents[/dim]\n")

    console.print("[bold]Conditions:[/bold]")
    console.print("  [cyan]baseline[/cyan]  — no interrogation, direct classify")
    console.print("  [cyan]unaware[/cyan]   — interrogated, agent does not know it will be questioned")
    console.print("  [cyan]aware[/cyan]     — interrogated, agent knows it may be questioned\n")

    console.print("[dim]Running 8 scenarios × 3 conditions = 24 total evaluations...[/dim]\n")

    results = run_full_evaluation()

    print_summary_table(results)

    filepath = save_results(results)

    console.print("\n[bold green]Evaluation complete.[/bold green]")
    console.print(f"[dim]Full results at: {filepath}[/dim]")
    console.print("[dim]Use results/ folder data for the research report.[/dim]\n")


if __name__ == "__main__":
    main()
