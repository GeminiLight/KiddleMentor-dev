"""Interactive onboarding command for GenMentor setup."""

import os
import sys
from pathlib import Path
from typing import Optional

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from omegaconf import OmegaConf

from gen_mentor.config import (
    get_default_config_path,
    ensure_config_dir,
    load_config,
    AppConfig,
)

console = Console()


def print_welcome():
    """Print welcome banner."""
    console.print()
    console.print("[bold cyan]" + "=" * 60)
    console.print("[bold cyan]       🎓 GenMentor - Interactive Setup 🎓")
    console.print("[bold cyan]" + "=" * 60)
    console.print()


def print_security_warning():
    """Print security warning."""
    warning_text = """
## Security Warning

**Please read carefully before proceeding:**

GenMentor uses Large Language Models (LLMs) and may:
- Send data to external API providers
- Access your local filesystem (if RAG is enabled)
- Store learning data in local databases

**Recommended practices:**
- Keep API keys secure and never commit them to git
- Review the configuration before running
- Use environment variables for sensitive data
- Understand your LLM provider's data policies

**For more information:**
https://github.com/yourusername/gen-mentor/wiki#security
"""
    console.print(Panel(Markdown(warning_text), title="⚠️  Security", border_style="yellow"))


def check_existing_config() -> Optional[AppConfig]:
    """Check if configuration already exists."""
    config_path = get_default_config_path()
    if config_path.exists():
        try:
            config = load_config(auto_create=False)
            return config
        except Exception:
            return None
    return None


def show_existing_config(config: AppConfig):
    """Display existing configuration."""
    console.print()
    console.print("[bold green]Existing configuration found:[/bold green]")
    console.print(f"  Location: {get_default_config_path()}")
    console.print(f"  Model: {config.agent_defaults.model}")
    console.print(f"  Temperature: {config.agent_defaults.temperature}")
    console.print(f"  Search Provider: {config.search_defaults.provider}")
    console.print()


def select_onboarding_mode() -> str:
    """Select onboarding mode."""
    return questionary.select(
        "Choose setup mode:",
        choices=[
            "Quick Start (Recommended)",
            "Advanced Setup",
            "Exit"
        ],
        style=questionary.Style([
            ("selected", "fg:cyan bold"),
            ("pointer", "fg:cyan bold"),
        ])
    ).ask()


def select_llm_provider() -> str:
    """Select LLM provider."""
    return questionary.select(
        "Select your primary LLM provider:",
        choices=[
            "OpenAI (GPT-4, GPT-3.5)",
            "Anthropic (Claude)",
            "DeepSeek (Recommended for cost)",
            "Together AI",
            "Groq (Fast inference)",
            "OpenRouter (Multi-provider)",
            "Ollama (Local models)",
            "Custom OpenAI-compatible API",
        ],
        style=questionary.Style([
            ("selected", "fg:cyan bold"),
            ("pointer", "fg:cyan bold"),
        ])
    ).ask()


def get_provider_info(provider_choice: str) -> tuple[str, str, Optional[str]]:
    """Get provider ID and default model."""
    provider_map = {
        "OpenAI (GPT-4, GPT-3.5)": ("openai", "gpt-4o-mini", None),
        "Anthropic (Claude)": ("anthropic", "claude-3-5-sonnet-20241022", None),
        "DeepSeek (Recommended for cost)": ("deepseek", "deepseek-chat", "https://api.deepseek.com"),
        "Together AI": ("together", "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "https://api.together.xyz"),
        "Groq (Fast inference)": ("groq", "llama-3.3-70b-versatile", "https://api.groq.com/openai/v1"),
        "OpenRouter (Multi-provider)": ("openrouter", "anthropic/claude-3.5-sonnet", "https://openrouter.ai/api/v1"),
        "Ollama (Local models)": ("ollama", "llama2", "http://localhost:11434"),
        "Custom OpenAI-compatible API": ("custom", "gpt-3.5-turbo", None),
    }
    return provider_map.get(provider_choice, ("openai", "gpt-4o-mini", None))


def get_api_key(provider: str) -> Optional[str]:
    """Get API key for provider."""
    if provider == "ollama":
        console.print("[yellow]Ollama doesn't require an API key (local models)[/yellow]")
        return None

    env_var_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "together": "TOGETHER_API_KEY",
        "groq": "GROQ_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "custom": "CUSTOM_API_KEY",
    }

    env_var = env_var_map.get(provider, f"{provider.upper()}_API_KEY")

    # Check if already in environment
    existing_key = os.getenv(env_var)
    if existing_key:
        use_existing = questionary.confirm(
            f"Found {env_var} in environment. Use it?",
            default=True
        ).ask()
        if use_existing:
            return None  # Use env var

    # Ask user to provide key
    console.print()
    console.print(f"[bold]API Key Setup for {provider}[/bold]")

    choice = questionary.select(
        "How would you like to provide the API key?",
        choices=[
            "Enter API key now (will be saved to config)",
            f"Set as environment variable ({env_var})",
            "Skip for now",
        ]
    ).ask()

    if choice.startswith("Enter API key"):
        api_key = questionary.password(
            f"Enter your {provider} API key:"
        ).ask()
        return api_key
    elif choice.startswith("Set as environment"):
        console.print(f"\n[yellow]Please set the environment variable:[/yellow]")
        console.print(f"  export {env_var}='your-api-key-here'")
        questionary.press_any_key_to_continue("Press any key after setting...").ask()
        return None
    else:
        console.print("[yellow]Skipping API key setup. You'll need to configure it later.[/yellow]")
        return None


def get_custom_model(provider: str, default_model: str) -> str:
    """Get custom model name."""
    use_default = questionary.confirm(
        f"Use default model '{default_model}'?",
        default=True
    ).ask()

    if use_default:
        return default_model

    model = questionary.text(
        "Enter model name:",
        default=default_model
    ).ask()
    return model or default_model


def get_custom_base_url(provider: str, default_url: Optional[str]) -> Optional[str]:
    """Get custom API base URL."""
    if provider == "openai":
        # OpenAI doesn't usually need custom URL
        return None

    if default_url:
        use_default = questionary.confirm(
            f"Use default API endpoint '{default_url}'?",
            default=True
        ).ask()
        if use_default:
            return default_url

    use_custom = questionary.confirm(
        "Use a custom API endpoint?",
        default=False
    ).ask()

    if use_custom:
        url = questionary.text(
            "Enter API base URL:",
            default=default_url or ""
        ).ask()
        return url or default_url

    return default_url


def select_search_provider() -> str:
    """Select search provider."""
    return questionary.select(
        "Select search provider (for RAG):",
        choices=[
            "DuckDuckGo (Free, no key required)",
            "Tavily (Requires API key)",
            "Serper (Requires API key)",
            "Bing (Requires API key)",
            "Brave (Requires API key)",
            "You.com (Requires API key)",
            "None (Disable search)",
        ],
        style=questionary.Style([
            ("selected", "fg:cyan bold"),
            ("pointer", "fg:cyan bold"),
        ])
    ).ask()


def get_search_provider_id(choice: str) -> str:
    """Get search provider ID."""
    provider_map = {
        "DuckDuckGo (Free, no key required)": "duckduckgo",
        "Tavily (Requires API key)": "tavily",
        "Serper (Requires API key)": "serper",
        "Bing (Requires API key)": "bing",
        "Brave (Requires API key)": "brave",
        "You.com (Requires API key)": "you",
        "None (Disable search)": "duckduckgo",
    }
    return provider_map.get(choice, "duckduckgo")


def select_embedding_provider() -> str:
    """Select embedding provider."""
    return questionary.select(
        "Select embedding provider:",
        choices=[
            "HuggingFace (Free, local models - Recommended)",
            "OpenAI (Requires API key)",
            "Cohere (Requires API key)",
            "Azure OpenAI (Requires API key)",
            "Ollama (Local models)",
        ],
        style=questionary.Style([
            ("selected", "fg:cyan bold"),
            ("pointer", "fg:cyan bold"),
        ])
    ).ask()


def get_embedding_provider_id(choice: str) -> str:
    """Get embedding provider ID."""
    provider_map = {
        "HuggingFace (Free, local models - Recommended)": "huggingface",
        "OpenAI (Requires API key)": "openai",
        "Cohere (Requires API key)": "cohere",
        "Azure OpenAI (Requires API key)": "azure",
        "Ollama (Local models)": "ollama",
    }
    return provider_map.get(choice, "huggingface")


def get_embedding_model_default(provider: str) -> str:
    """Get default embedding model for provider."""
    models = {
        "huggingface": "sentence-transformers/all-mpnet-base-v2",
        "openai": "text-embedding-3-small",
        "cohere": "embed-english-v3.0",
        "azure": "text-embedding-ada-002",
        "ollama": "nomic-embed-text",
    }
    return models.get(provider, "sentence-transformers/all-mpnet-base-v2")



def configure_advanced_settings() -> dict:
    """Configure advanced settings."""
    console.print("\n[bold]Advanced Settings[/bold]")

    temperature = questionary.text(
        "Temperature (0.0-1.0, lower = more deterministic):",
        default="0.0",
        validate=lambda x: 0.0 <= float(x) <= 1.0
    ).ask()

    max_tokens = questionary.text(
        "Max tokens per response:",
        default="8192"
    ).ask()

    chunk_size = questionary.text(
        "RAG chunk size:",
        default="1000"
    ).ask()

    return {
        "temperature": float(temperature),
        "max_tokens": int(max_tokens),
        "chunk_size": int(chunk_size),
    }


def quick_start_setup() -> dict:
    """Quick start setup flow."""
    console.print("\n[bold cyan]Quick Start Setup[/bold cyan]")
    console.print("We'll set up the essentials. You can customize later.\n")

    # Select LLM provider
    provider_choice = select_llm_provider()
    provider, default_model, default_url = get_provider_info(provider_choice)

    # Get API key
    api_key = get_api_key(provider)

    # Model selection
    model = get_custom_model(provider, default_model)

    # API base URL
    api_base = get_custom_base_url(provider, default_url)

    # Search provider
    console.print("\n[bold]Search Configuration[/bold]")
    console.print("Search is used for RAG (Retrieval-Augmented Generation)")
    search_choice = select_search_provider()
    search_provider = get_search_provider_id(search_choice)

    # Ask about enabling search
    enable_search = questionary.confirm(
        "Enable web search for external context retrieval?",
        default=False
    ).ask()

    # Embedding provider
    console.print("\n[bold]Embedding Configuration[/bold]")
    console.print("Embeddings convert text to vectors for semantic search")
    embedding_choice = select_embedding_provider()
    embedding_provider = get_embedding_provider_id(embedding_choice)
    embedding_model = get_embedding_model_default(embedding_provider)

    # Ask about vectordb
    enable_vectordb = questionary.confirm(
        "Enable vector database for document storage and retrieval?",
        default=False
    ).ask()

    if enable_vectordb:
        console.print("[dim]Note: Vector database requires downloading embedding models on first use[/dim]")

    return {
        "provider": provider,
        "model": model,
        "api_key": api_key,
        "api_base": api_base,
        "search_provider": search_provider,
        "enable_search": enable_search,
        "embedding_provider": embedding_provider,
        "embedding_model": embedding_model,
        "enable_vectordb": enable_vectordb,
        "temperature": 0.0,
        "max_tokens": 8192,
        "chunk_size": 1000,
    }


def advanced_setup() -> dict:
    """Advanced setup flow."""
    console.print("\n[bold cyan]Advanced Setup[/bold cyan]")

    # Run quick start first
    config = quick_start_setup()

    # Add advanced settings
    advanced = configure_advanced_settings()
    config.update(advanced)

    return config


def create_config_from_setup(setup_data: dict) -> dict:
    """Create configuration dict from setup data."""
    provider = setup_data["provider"]
    model = setup_data["model"]

    config = {
        "environment": "dev",
        "debug": True,
        "log_level": "INFO",
        "agent_defaults": {
            "model": f"{provider}/{model}",
            "temperature": setup_data["temperature"],
            "max_tokens": setup_data["max_tokens"],
        },
        "providers": {
            provider: {
                "api_key": setup_data.get("api_key"),
                "api_base": setup_data.get("api_base"),
            }
        },
        "search_defaults": {
            "provider": setup_data["search_provider"],
            "max_results": 5,
            "loader_type": "web",
            "enable_search": setup_data.get("enable_search", False),
        },
        "search_providers": {
            setup_data["search_provider"]: {
                "api_key": None,
                "max_results": 5,
            }
        },
        "embedding_defaults": {
            "provider": setup_data["embedding_provider"],
            "model_name": setup_data["embedding_model"],
            "dimension": 768,
            "enable_vectordb": setup_data.get("enable_vectordb", False),
        },
        "embedding_providers": {
            setup_data["embedding_provider"]: {
                "api_key": None,
                "model_name": setup_data["embedding_model"],
                "api_base": None,
            }
        },
        "vectorstore": {
            "persist_directory": "data/vectorstore",
            "collection_name": "genmentor",
        },
        "rag": {
            "chunk_size": setup_data["chunk_size"],
            "num_retrieval_results": 5,
            "allow_parallel": True,
            "max_workers": 3,
        },
    }

    return config


def save_config(config_dict: dict) -> Path:
    """Save configuration to file."""
    config_path = get_default_config_path()
    ensure_config_dir()

    # Convert to OmegaConf and save
    cfg = OmegaConf.create(config_dict)
    OmegaConf.save(cfg, config_path)

    return config_path


def show_next_steps(config_path: Path, provider: str):
    """Show next steps after setup."""
    console.print()
    console.print("[bold green]✓ Configuration saved successfully![/bold green]")
    console.print(f"  Location: {config_path}")
    console.print()
    console.print("[bold]Next Steps:[/bold]")
    console.print()
    console.print("1. [cyan]Verify your configuration:[/cyan]")
    console.print(f"   cat {config_path}")
    console.print()
    console.print("2. [cyan]Test the CLI:[/cyan]")
    console.print("   gen-mentor agent -m 'What is 2+2?'")
    console.print()
    console.print("3. [cyan]Start the backend:[/cyan]")
    console.print("   cd apps/backend")
    console.print("   uvicorn main:app --reload --port 5000")
    console.print()
    console.print("4. [cyan]Start the frontend:[/cyan]")
    console.print("   cd apps/frontend_streamlit")
    console.print("   streamlit run main.py --server.port 8501")
    console.print()
    console.print("[bold]Documentation:[/bold]")
    console.print("  Wiki: wiki.md")
    console.print("  README: README.md")
    console.print()


def onboard():
    """Main onboarding flow."""
    print_welcome()

    # Security warning
    print_security_warning()
    accept_risk = questionary.confirm(
        "I understand and accept the security implications. Continue?",
        default=False
    ).ask()

    if not accept_risk:
        console.print("\n[yellow]Setup cancelled.[/yellow]")
        sys.exit(0)

    # Check existing config
    existing_config = check_existing_config()
    if existing_config:
        show_existing_config(existing_config)

        action = questionary.select(
            "Configuration already exists. What would you like to do?",
            choices=[
                "Keep existing configuration",
                "Reconfigure (overwrites existing)",
                "Exit"
            ]
        ).ask()

        if action == "Keep existing configuration":
            console.print("\n[green]Using existing configuration.[/green]")
            show_next_steps(get_default_config_path(), existing_config.agent_defaults.model.split("/")[0])
            return
        elif action == "Exit":
            sys.exit(0)

    # Select mode
    mode = select_onboarding_mode()

    if mode == "Exit":
        console.print("\n[yellow]Setup cancelled.[/yellow]")
        sys.exit(0)

    # Run setup
    if mode == "Quick Start (Recommended)":
        setup_data = quick_start_setup()
    else:  # Advanced Setup
        setup_data = advanced_setup()

    # Create config
    config_dict = create_config_from_setup(setup_data)

    # Confirm before saving
    console.print("\n[bold]Configuration Summary:[/bold]")
    console.print(f"  Provider: {setup_data['provider']}")
    console.print(f"  Model: {setup_data['model']}")
    console.print(f"  Temperature: {setup_data['temperature']}")
    console.print(f"  Search: {setup_data['search_provider']} ({'Enabled' if setup_data.get('enable_search', False) else 'Disabled'})")
    console.print(f"  Embedding: {setup_data['embedding_provider']} ({setup_data['embedding_model']})")
    console.print(f"  Vector DB: {'Enabled' if setup_data.get('enable_vectordb', False) else 'Disabled'}")
    console.print()

    confirm = questionary.confirm(
        "Save this configuration?",
        default=True
    ).ask()

    if not confirm:
        console.print("\n[yellow]Setup cancelled.[/yellow]")
        sys.exit(0)

    # Save config
    config_path = save_config(config_dict)

    # Show next steps
    show_next_steps(config_path, setup_data['provider'])

    console.print("[bold green]🎓 GenMentor setup complete! Happy learning! 🎓[/bold green]\n")


if __name__ == "__main__":
    try:
        onboard()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Setup cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error during setup: {e}[/red]")
        console.print("[yellow]Please check the error and try again.[/yellow]")
        sys.exit(1)
