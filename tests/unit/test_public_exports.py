"""Package wildcard exports must refer to callable public helpers."""

import importlib

import pytest


@pytest.mark.parametrize("package", ["gen_mentor.agents.content", "gen_mentor.agents.assessment"])
def test_all_public_helpers_are_available(package):
    module = importlib.import_module(package)
    for name in module.__all__:
        assert callable(getattr(module, name)), f"{package}.{name} is not a public helper"


@pytest.mark.parametrize("identifier", ["", " ", "\n\t"])
def test_blank_session_ids_are_rejected(identifier):
    from pydantic import ValidationError
    from gen_mentor.schemas import SessionItem

    with pytest.raises(ValidationError, match="Session identifier"):
        SessionItem(id=identifier, title="Lesson", abstract="Intro", if_learned=False)
