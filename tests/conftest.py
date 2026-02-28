import pytest


@pytest.fixture(autouse=True)
def isolate_media_root(tmp_path, settings):
    """Ensure MEDIA_ROOT is isolated for tests so uploads don't pollute the repo."""
    settings.MEDIA_ROOT = tmp_path / "media"
