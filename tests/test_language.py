from backend.services.language import language_label, normalize_language


def test_normalize_language() -> None:
    assert normalize_language("Hindi") == "hi"
    assert normalize_language("unknown") == "en"
    assert language_label("ta") == "Tamil"
