from fossil.config import get_settings


def test_settings_defaults_are_sane() -> None:
    s = get_settings()
    assert s.request_timeout > 0
    assert s.max_retries >= 0
    assert s.reports_per_run >= 1
