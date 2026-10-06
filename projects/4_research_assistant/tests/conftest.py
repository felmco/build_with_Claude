import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from research.budget import Budget  # noqa: E402
from research.fake import FakeClient  # noqa: E402


@pytest.fixture
def budget():
    return Budget(max_tokens=1_000_000, max_cost_usd=10.0, max_tool_uses=100)


@pytest.fixture
def fake_client():
    return FakeClient()
