"""
Suppress Pydantic V1 compatibility warnings for Python 3.13+

Add this to the beginning of your scripts to suppress the warning:
    from gen_mentor.utils.suppress_warnings import suppress_pydantic_warnings
    suppress_pydantic_warnings()
"""

import warnings


def suppress_pydantic_warnings():
    """Suppress Pydantic V1 compatibility warnings."""
    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        module="langchain_core._api.deprecation",
        message=".*Pydantic V1 functionality.*"
    )
    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message=".*Pydantic V1.*"
    )


def suppress_all_deprecation_warnings():
    """Suppress all deprecation warnings (use with caution)."""
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning)


# Auto-suppress on import
suppress_pydantic_warnings()
