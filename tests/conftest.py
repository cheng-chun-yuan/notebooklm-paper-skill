import sys
from pathlib import Path

import pytest

# Add project root to path so 'scripts.config' is importable
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def tmp_project_dir(tmp_path):
    """Create a temp directory structure mimicking a project.

    Provides a Path to a temporary project directory with a ``drafts/``
    subdirectory already created, ready for tests to populate with
    artifact files.
    """
    project = tmp_path / "test-project"
    project.mkdir()
    (project / "drafts").mkdir()
    return project
