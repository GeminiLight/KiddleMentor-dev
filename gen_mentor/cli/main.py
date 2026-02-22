from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

# Suppress Pydantic V1 warnings for Python 3.13+
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*Pydantic V1 functionality.*")

from rich.console import Console
from rich.json import JSON as RichJSON
from rich.panel import Panel
from rich.table import Table
from rich_argparse import RichHelpFormatter


console = Console()


def _read_text_or_file(value: str | None) -> str:
    if not value:
        return ""
    if value.startswith("@"):
        return Path(value[1:]).read_text(encoding="utf-8")
    return value


def _read_json(value: str | None, default: Any = None) -> Any:
    if value is None:
        return default
    text = _read_text_or_file(value)
    if not text.strip():
        return default
    return json.loads(text)


def _create_llm(args: argparse.Namespace):
    from gen_mentor.core.llm import LLMFactory
    from gen_mentor.config import load_config

    config = load_config()

    # Use provided values or fall back to config
    model = args.model or config.agent_defaults.model
    provider = args.provider or config.get_provider_name(model)
    temperature = args.temperature if hasattr(args, 'temperature') and args.temperature is not None else config.agent_defaults.temperature
    base_url = args.base_url or config.get_api_base(model)

    # Extract model name (remove provider prefix if present)
    model_name = model.split('/')[-1] if '/' in model else model

    return LLMFactory.create(
        model=model_name,
        model_provider=provider,
        temperature=temperature,
        base_url=base_url,
    )


def _print_json(data: Any) -> None:
    console.print(RichJSON.from_data(data, indent=2, ensure_ascii=False))


def _print_banner() -> None:
    console.print(
        Panel.fit(
            "[bold cyan]GenMentor CLI[/bold cyan]\n[dim]Run core capabilities without backend/frontend services[/dim]",
            border_style="cyan",
        )
    )


def _print_command_summary(args: argparse.Namespace) -> None:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="white")
    table.add_row("Command", args.command)
    table.add_row("Provider", str(getattr(args, "provider", "-")))
    table.add_row("Model", str(getattr(args, "model", "-")))
    table.add_row("Temperature", str(getattr(args, "temperature", "-")))
    console.print(table)


def cmd_refine_goal(args: argparse.Namespace) -> int:
    from gen_mentor.agents.learning.skill_gap_identification import refine_learning_goal_with_llm

    with console.status("[bold green]Refining learning goal...[/bold green]"):
        llm = _create_llm(args)
        result = refine_learning_goal_with_llm(
            llm,
            learning_goal=_read_text_or_file(args.goal),
            learner_information=_read_text_or_file(args.learner_info),
        )
    _print_json(result)
    return 0


def cmd_identify_skill_gap(args: argparse.Namespace) -> int:
    from gen_mentor.agents.learning.skill_gap_identification import identify_skill_gap_with_llm

    with console.status("[bold green]Identifying skill gaps...[/bold green]"):
        llm = _create_llm(args)
        skill_requirements = _read_json(args.skill_requirements, default=None)
        skill_gaps, used_requirements = identify_skill_gap_with_llm(
            llm,
            learning_goal=_read_text_or_file(args.goal),
            learner_information=_read_text_or_file(args.learner_info),
            skill_requirements=skill_requirements,
        )
    _print_json(
        {
            "skill_gaps": skill_gaps,
            "skill_requirements": used_requirements,
        }
    )
    return 0


def cmd_schedule_path(args: argparse.Namespace) -> int:
    from gen_mentor.agents.content.personalized_resource_delivery.agents.learning_path_scheduler import (
        schedule_learning_path_with_llm,
    )

    with console.status("[bold green]Scheduling learning path...[/bold green]"):
        llm = _create_llm(args)
        learner_profile = _read_json(args.learner_profile, default={})
        result = schedule_learning_path_with_llm(
            llm,
            learner_profile=learner_profile,
            session_count=args.session_count,
        )
    _print_json(result)
    return 0


# ============================================================================
# Agent Commands
# ============================================================================

def cmd_agent(args: argparse.Namespace) -> int:
    """Run a simple agent query."""
    from gen_mentor.config import load_config
    from gen_mentor.core.llm import LLMFactory
    from gen_mentor.agents.base_agent import BaseAgent

    try:
        # Load configuration
        config = load_config()

        # Use provided model or default from config
        model_str = args.model or config.agent_defaults.model
        provider = args.provider or config.get_provider_name(model_str)
        base_url = args.base_url or config.get_api_base(model_str)
        api_key = args.api_key or config.get_api_key(model_str)
        temperature = args.temperature if args.temperature is not None else config.agent_defaults.temperature

        # Extract model name (remove provider prefix if present)
        model_name = model_str.split('/')[-1] if '/' in model_str else model_str

        console.print(f"\n[bold cyan]Initializing agent...[/bold cyan]")
        console.print(f"[dim]Model: {model_name} ({provider})[/dim]")
        console.print(f"[dim]Temperature: {temperature}[/dim]")

        # Create LLM
        llm = LLMFactory.create(
            model=model_name,
            model_provider=provider,
            temperature=temperature,
            base_url=base_url,
            api_key=api_key,
        )

        # Create agent
        system_prompt = args.system_prompt or "You are a helpful AI assistant."
        agent = BaseAgent(
            model=llm,
            system_prompt=system_prompt,
            tools=[],
            exclude_think=not args.show_thinking,
            jsonalize_output=False,
        )

        # Run query
        console.print(f"\n[bold green]Query:[/bold green] {args.message}\n")

        with console.status("[bold yellow]Thinking...[/bold yellow]"):
            result = agent.invoke(
                input_dict={},
                task_prompt=args.message
            )

        console.print(f"[bold cyan]Response:[/bold cyan]")
        console.print(result)
        console.print()

        return 0

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        import traceback
        if args.debug:
            traceback.print_exc()
        return 1


# ============================================================================
# Config Management Commands
# ============================================================================

def cmd_config_show(args: argparse.Namespace) -> int:
    """Show current configuration."""
    from gen_mentor.config import load_config, get_default_config_path

    try:
        config = load_config()
        config_path = get_default_config_path()

        console.print(f"\n[bold cyan]Configuration file:[/bold cyan] {config_path}")
        console.print(f"[dim]File exists: {config_path.exists()}[/dim]\n")

        # Agent Default Settings
        table = Table(title="Agent Default Settings", show_header=True, header_style="bold magenta")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Default Model", config.agent_defaults.model)
        table.add_row("Temperature", str(config.agent_defaults.temperature))
        table.add_row("Max Tokens", str(config.agent_defaults.max_tokens))
        table.add_row("Workspace", config.agent_defaults.workspace)
        console.print(table)

        # LLM Providers
        table = Table(title="\nLLM Providers", show_header=True, header_style="bold magenta")
        table.add_column("Provider", style="cyan", no_wrap=True)
        table.add_column("API Key", style="green")
        table.add_column("API Base", style="white")

        for provider_name in ["openai", "anthropic", "deepseek", "together", "groq", "openrouter", "ollama", "custom"]:
            provider = getattr(config.providers, provider_name)
            api_key_status = "✓ Set" if provider.api_key else "✗ Not set"
            api_base = provider.api_base or "-"
            table.add_row(provider_name, api_key_status, api_base)

        console.print(table)

        # Search Default Settings
        table = Table(title="\nSearch Default Settings", show_header=True, header_style="bold magenta")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Default Provider", config.search_defaults.provider)
        table.add_row("Max Results", str(config.search_defaults.max_results))
        table.add_row("Loader Type", config.search_defaults.loader_type)
        table.add_row("Search Enabled", "✓ Yes" if config.search_defaults.enable_search else "✗ No")
        console.print(table)

        # Search Providers
        table = Table(title="\nSearch Providers", show_header=True, header_style="bold magenta")
        table.add_column("Provider", style="cyan", no_wrap=True)
        table.add_column("API Key", style="green")
        table.add_column("Max Results", style="white")

        for provider_name in ["duckduckgo", "tavily", "serper", "bing", "brave", "you"]:
            provider = getattr(config.search_providers, provider_name)
            api_key_status = "✓ Set" if provider.api_key else ("N/A" if provider_name == "duckduckgo" else "✗ Not set")
            table.add_row(provider_name, api_key_status, str(provider.max_results))

        console.print(table)

        # Embedding Default Settings
        table = Table(title="\nEmbedding Default Settings", show_header=True, header_style="bold magenta")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Default Provider", config.embedding_defaults.provider)
        table.add_row("Model Name", config.embedding_defaults.model_name)
        table.add_row("Dimension", str(config.embedding_defaults.dimension))
        table.add_row("Vector DB Enabled", "✓ Yes" if config.embedding_defaults.enable_vectordb else "✗ No")
        console.print(table)

        # Embedding Providers
        table = Table(title="\nEmbedding Providers", show_header=True, header_style="bold magenta")
        table.add_column("Provider", style="cyan", no_wrap=True)
        table.add_column("API Key", style="green")
        table.add_column("Model", style="white")

        for provider_name in ["huggingface", "openai", "cohere", "azure", "ollama"]:
            provider = getattr(config.embedding_providers, provider_name)
            if provider_name in ["huggingface", "ollama"]:
                api_key_status = "N/A"
            else:
                api_key_status = "✓ Set" if provider.api_key else "✗ Not set"
            table.add_row(provider_name, api_key_status, provider.model_name)

        console.print(table)

        # Other settings
        table = Table(title="\nOther Settings", show_header=True, header_style="bold magenta")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Environment", config.environment)
        table.add_row("Debug", str(config.debug))
        table.add_row("Log Level", config.log_level)

        console.print(table)

        return 0
    except Exception as e:
        console.print(f"[bold red]Error loading configuration:[/bold red] {e}")
        return 1


def cmd_config_path(args: argparse.Namespace) -> int:
    """Show configuration file path."""
    from gen_mentor.config import get_default_config_path

    config_path = get_default_config_path()
    console.print(f"[cyan]{config_path}[/cyan]")
    return 0


def cmd_config_init(args: argparse.Namespace) -> int:
    """Initialize configuration file."""
    from gen_mentor.config import get_default_config_path, create_default_config_file

    config_path = get_default_config_path()

    if config_path.exists() and not args.force:
        console.print(f"[yellow]Configuration already exists at:[/yellow] {config_path}")
        console.print("[dim]Use --force to overwrite[/dim]")
        return 1

    try:
        config_path = create_default_config_file()
        console.print(f"[bold green]✓[/bold green] Configuration initialized at: [cyan]{config_path}[/cyan]")
        console.print("\n[bold]Edit this file to customize your settings:[/bold]")
        console.print(f"  [dim]vim {config_path}[/dim]")
        console.print(f"  [dim]code {config_path}[/dim]")
        return 0
    except Exception as e:
        console.print(f"[bold red]Error initializing configuration:[/bold red] {e}")
        return 1


def cmd_config_edit(args: argparse.Namespace) -> int:
    """Open configuration file in editor."""
    import os
    import subprocess
    from gen_mentor.config import get_default_config_path

    config_path = get_default_config_path()

    if not config_path.exists():
        console.print(f"[yellow]Configuration not found at:[/yellow] {config_path}")
        console.print("[dim]Run 'gen-mentor config init' to create it[/dim]")
        return 1

    # Try to find an editor
    editor = args.editor or os.environ.get("EDITOR") or "vim"

    try:
        subprocess.run([editor, str(config_path)], check=True)
        return 0
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error opening editor:[/bold red] {e}")
        return 1
    except FileNotFoundError:
        console.print(f"[bold red]Editor not found:[/bold red] {editor}")
        console.print("[dim]Set the EDITOR environment variable or use --editor[/dim]")
        return 1


def cmd_config_validate(args: argparse.Namespace) -> int:
    """Validate configuration file."""
    from gen_mentor.config import load_config, get_default_config_path

    try:
        config = load_config()
        config_path = get_default_config_path()

        console.print(f"\n[bold]Validating configuration:[/bold] [cyan]{config_path}[/cyan]\n")

        # Check default model is valid
        if config.agent_defaults.model:
            console.print(f"[green]✓[/green] Default agent model: {config.agent_defaults.model}")
        else:
            console.print(f"[red]✗[/red] Default agent model not set")
            return 1

        # Check if at least one LLM provider has API key
        has_llm_key = False
        for provider_name in ["openai", "anthropic", "deepseek", "together", "groq", "openrouter", "custom"]:
            provider = getattr(config.providers, provider_name)
            if provider.api_key:
                has_llm_key = True
                break

        if has_llm_key:
            console.print(f"[green]✓[/green] At least one LLM provider has API key configured")
        else:
            console.print(f"[yellow]⚠[/yellow] No LLM provider API keys found. Set via environment variables.")

        # Check default search provider is valid
        if config.search_defaults.provider:
            console.print(f"[green]✓[/green] Default search provider: {config.search_defaults.provider}")
        else:
            console.print(f"[red]✗[/red] Default search provider not set")
            return 1

        console.print("\n[bold green]✓ Configuration is valid[/bold green]")
        return 0

    except Exception as e:
        console.print(f"[bold red]✗ Configuration validation failed:[/bold red] {e}")
        return 1


def cmd_onboard(args: argparse.Namespace) -> int:
    """Run interactive onboarding wizard."""
    from gen_mentor.cli.onboard import onboard
    try:
        onboard()
        return 0
    except Exception as e:
        console.print(f"[bold red]Onboarding failed:[/bold red] {e}")
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gen-mentor",
        description="GenMentor core CLI (without backend/frontend app services).",
        formatter_class=RichHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_llm_options(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--provider", default=None, help="LLM provider (auto-detected from config)")
        subparser.add_argument("--model", default=None, help="LLM model name (uses config default if not specified)")
        subparser.add_argument("--temperature", type=float, default=None, help="Sampling temperature (uses config default)")
        subparser.add_argument("--base-url", default=None, help="Optional custom LLM base URL")
        subparser.add_argument("--api-key", default=None, help="Optional API key (uses config if not specified)")

    # ========================================================================
    # Onboarding Command
    # ========================================================================

    p_onboard = subparsers.add_parser("onboard", help="Interactive setup wizard (recommended for first-time users)")
    p_onboard.set_defaults(func=cmd_onboard)

    # ========================================================================
    # Agent Commands
    # ========================================================================

    p_agent = subparsers.add_parser("agent", help="Run a simple agent query")
    p_agent.add_argument("-m", "--message", required=True, help="Message/query for the agent")
    p_agent.add_argument("--system-prompt", default=None, help="Custom system prompt")
    p_agent.add_argument("--show-thinking", action="store_true", help="Show agent's thinking process")
    p_agent.add_argument("--debug", action="store_true", help="Show debug information on error")
    add_llm_options(p_agent)
    p_agent.set_defaults(func=cmd_agent)

    # ========================================================================
    # Learning Commands
    # ========================================================================

    p_refine = subparsers.add_parser("refine-goal", help="Refine a learning goal")
    p_refine.add_argument("--goal", required=True, help="Learning goal text or @file")
    p_refine.add_argument("--learner-info", default="", help="Learner info text or @file")
    add_llm_options(p_refine)
    p_refine.set_defaults(func=cmd_refine_goal)

    p_gap = subparsers.add_parser("identify-skill-gap", help="Identify skill gaps")
    p_gap.add_argument("--goal", required=True, help="Learning goal text or @file")
    p_gap.add_argument("--learner-info", required=True, help="Learner information text or @file")
    p_gap.add_argument(
        "--skill-requirements",
        default=None,
        help="Optional JSON text or @json_file for precomputed requirements",
    )
    add_llm_options(p_gap)
    p_gap.set_defaults(func=cmd_identify_skill_gap)

    p_path = subparsers.add_parser("schedule-path", help="Schedule a learning path")
    p_path.add_argument(
        "--learner-profile",
        required=True,
        help="Learner profile JSON text or @json_file",
    )
    p_path.add_argument("--session-count", type=int, default=8, help="Number of sessions")
    add_llm_options(p_path)
    p_path.set_defaults(func=cmd_schedule_path)

    # ========================================================================
    # Config Commands
    # ========================================================================

    p_config = subparsers.add_parser("config", help="Manage configuration")
    config_subparsers = p_config.add_subparsers(dest="config_command", required=True)

    # config show
    p_config_show = config_subparsers.add_parser("show", help="Show current configuration")
    p_config_show.set_defaults(func=cmd_config_show)

    # config path
    p_config_path = config_subparsers.add_parser("path", help="Show configuration file path")
    p_config_path.set_defaults(func=cmd_config_path)

    # config init
    p_config_init = config_subparsers.add_parser("init", help="Initialize configuration file")
    p_config_init.add_argument("--force", action="store_true", help="Overwrite existing configuration")
    p_config_init.set_defaults(func=cmd_config_init)

    # config edit
    p_config_edit = config_subparsers.add_parser("edit", help="Edit configuration file")
    p_config_edit.add_argument("--editor", help="Editor to use (defaults to $EDITOR)")
    p_config_edit.set_defaults(func=cmd_config_edit)

    # config validate
    p_config_validate = config_subparsers.add_parser("validate", help="Validate configuration")
    p_config_validate.set_defaults(func=cmd_config_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _print_banner()
    _print_command_summary(args)
    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        console.print("[yellow]Interrupted[/yellow]")
        return 130
    except Exception as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
