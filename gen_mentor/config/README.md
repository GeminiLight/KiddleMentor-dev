# GenMentor Configuration

This directory contains the configuration system for GenMentor.

## Files

- **`schemas.py`**: Configuration dataclass definitions
- **`loader.py`**: Configuration loading utilities
- **`config.example.yaml`**: Example configuration file

## Configuration Location

GenMentor automatically stores user configuration in:
```
~/.gen-mentor/config.yaml
```

On first run, if this file doesn't exist, it will be automatically created from the example configuration.

## Quick Start

### 1. Using Default Configuration (Automatic)

```python
from gen_mentor.config import default_config

# Automatically loads from ~/.gen-mentor/config.yaml
# (creates it if it doesn't exist)
llm = default_config.llms.get_default_llm()
print(f"Using {llm.provider}/{llm.model_name}")
```

### 2. Loading from Custom Location

```python
from gen_mentor.config import load_config

# Load custom config
config = load_config("path/to/custom_config.yaml")

# Get default LLM
llm = config.llms.get_default_llm()

# Get specific LLM by name
gpt4 = config.llms.get_llm("gpt4")
```

### 3. Editing Your Configuration

The configuration file is automatically created at `~/.gen-mentor/config.yaml`. You can edit it directly:

```bash
# Open in your editor
vim ~/.gen-mentor/config.yaml
# or
code ~/.gen-mentor/config.yaml
```

Or get the path programmatically:

```python
from gen_mentor.config import get_default_config_path

config_path = get_default_config_path()
print(f"Config location: {config_path}")
# Output: Config location: /home/username/.gen-mentor/config.yaml
```

### 4. Saving Configuration Programmatically

```python
from gen_mentor.config import load_config, save_config

# Load existing config
config = load_config()

# Modify it
config.llms.default = "gpt4"

# Save back to ~/.gen-mentor/config.yaml
save_config(config)

# Or save to custom location
save_config(config, "path/to/custom_config.yaml")
```

## Multiple LLM Configuration

The config system supports multiple LLM providers, allowing you to:

- Define different LLMs for different tasks
- Switch between models easily
- Test different providers
- Use local models (Ollama) alongside cloud APIs

### Accessing LLMs

```python
from gen_mentor.config import load_config

config = load_config("my_config.yaml")

# Get default LLM
default_llm = config.llms.get_default_llm()

# Get specific LLM by name
gpt4_llm = config.llms.get_llm("gpt4")
claude_llm = config.llms.get_llm("claude")
ollama_llm = config.llms.get_llm("ollama")

# List all available LLMs
for name, llm_config in config.llms.llms.items():
    print(f"{name}: {llm_config.provider}/{llm_config.model_name}")
```

## Multiple Search Provider Configuration

The config system also supports multiple search providers:

- Define different search APIs for different use cases
- Switch between free and paid search services
- Test search quality across providers
- Fallback options if one provider is down

### Accessing Search Providers

```python
from gen_mentor.config import load_config

config = load_config("my_config.yaml")

# Get default search provider
default_search = config.searches.get_default_search()

# Get specific search provider by name
tavily_search = config.searches.get_search("tavily")
serper_search = config.searches.get_search("serper")
duckduckgo_search = config.searches.get_search("duckduckgo")

# List all available search providers
for name, search_config in config.searches.searches.items():
    print(f"{name}: {search_config.provider} (max_results={search_config.max_results})")
```

## Environment Variables

API keys should be set via environment variables:

**LLM Providers:**
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `DEEPSEEK_API_KEY` - DeepSeek API key
- `TOGETHER_API_KEY` - Together AI API key
- `GROQ_API_KEY` - Groq API key

**Search Providers:**
- `TAVILY_API_KEY` - Tavily search API key
- `SERPER_API_KEY` - Serper (Google Search) API key
- `BING_SUBSCRIPTION_KEY` - Bing Search API key
- `BRAVE_API_KEY` - Brave Search API key
- `YDC_API_KEY` - You.com Search API key

## First-Time Setup

On first import or when `default_config` is accessed, GenMentor will:

1. Check if `~/.gen-mentor/config.yaml` exists
2. If not, automatically create the directory and copy the example configuration
3. You'll see a message: `Created default configuration at: ~/.gen-mentor/config.yaml`
4. You can then edit this file to customize your settings

```python
# First time - creates ~/.gen-mentor/config.yaml
from gen_mentor.config import default_config

# Now edit the file and reload
from gen_mentor.config import load_config
config = load_config()  # Reloads from ~/.gen-mentor/config.yaml
```

## Configuration CLI Tool

GenMentor provides config management commands in the main CLI:

```bash
# Show current configuration
gen-mentor config show

# Show configuration file path
gen-mentor config path

# Initialize configuration (create ~/.gen-mentor/config.yaml)
gen-mentor config init

# Force overwrite existing config
gen-mentor config init --force

# Edit configuration in your editor
gen-mentor config edit

# Edit with specific editor
gen-mentor config edit --editor code

# Validate configuration
gen-mentor config validate
```

### Example Output

```bash
$ gen-mentor config show

Configuration file: /home/user/.gen-mentor/config.yaml
File exists: True

┏━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Name      ┃ Provider  ┃ Model                        ┃ Default┃
┡━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ deepseek  │ deepseek  │ deepseek-chat                │        │
│ gpt-5.1   │ openai    │ gpt-5.1                      │   ✓    │
│ claude    │ anthropic │ claude-3-5-sonnet-20241022   │        │
└───────────┴───────────┴──────────────────────────────┴────────┘
```

## Helper Functions

```python
from gen_mentor.config import (
    get_default_config_path,
    ensure_config_dir,
    create_default_config_file,
    save_config,
)

# Get the default config file path
path = get_default_config_path()
# Returns: Path('~/.gen-mentor/config.yaml')

# Ensure the config directory exists
config_dir = ensure_config_dir()
# Creates ~/.gen-mentor if it doesn't exist

# Manually trigger config file creation
config_file = create_default_config_file()
# Creates ~/.gen-mentor/config.yaml from example

# Save modified config
save_config(my_config)  # Saves to default location
save_config(my_config, "custom.yaml")  # Saves to custom location
```

## Configuration Schema

### LLMConfig

Single LLM configuration:

```python
@dataclass
class LLMConfig:
    provider: str          # LLM provider (openai, anthropic, etc.)
    model_name: str        # Model name
    base_url: Optional[str]  # Custom endpoint URL
    temperature: float     # Sampling temperature
    api_key: Optional[str]   # API key (prefer env vars)
```

### LLMsConfig

Multiple LLM configuration manager:

```python
@dataclass
class LLMsConfig:
    llms: Dict[str, LLMConfig]  # Named LLM configurations
    default: str                 # Key of default LLM

    def get_default_llm() -> LLMConfig
    def get_llm(name: str) -> LLMConfig
```

### SearchConfig

Single search provider configuration:

```python
@dataclass
class SearchConfig:
    provider: str              # Search provider name
    max_results: int           # Maximum search results
    loader_type: str           # Document loader type
    api_key: Optional[str]     # API key (prefer env vars)
```

### SearchesConfig

Multiple search provider configuration manager:

```python
@dataclass
class SearchesConfig:
    searches: Dict[str, SearchConfig]  # Named search configurations
    default: str                        # Key of default search provider

    def get_default_search() -> SearchConfig
    def get_search(name: str) -> SearchConfig
```

## Programmatic Configuration

You can also create configuration programmatically:

```python
from gen_mentor.config import (
    LLMConfig, LLMsConfig,
    SearchConfig, SearchesConfig,
    AppConfig
)

# Create custom LLM configs
llms_config = LLMsConfig(
    llms={
        "gpt4": LLMConfig(
            provider="openai",
            model_name="gpt-4-turbo-preview",
            temperature=0.0,
        ),
        "claude": LLMConfig(
            provider="anthropic",
            model_name="claude-3-5-sonnet-20241022",
            temperature=0.0,
        ),
    },
    default="gpt4"
)

# Create custom search configs
searches_config = SearchesConfig(
    searches={
        "duckduckgo": SearchConfig(
            provider="duckduckgo",
            max_results=5,
        ),
        "tavily": SearchConfig(
            provider="tavily",
            max_results=10,
        ),
    },
    default="duckduckgo"
)

# Create full app config
config = AppConfig(
    llms=llms_config,
    searches=searches_config,
    debug=True,
    log_level="INFO",
)
```
