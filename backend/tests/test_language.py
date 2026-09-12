import pytest
from backend.app.language.language_service import language_service
from backend.app.language.bhashini_adapter import bhashini_adapter

def test_language_service():
    langs = language_service.get_supported_languages()
    assert len(langs) >= 22
    codes = [l["code"] for l in langs]
    assert "hi" in codes
    assert "bn" in codes
    assert "ta" in codes

@pytest.mark.asyncio
async def test_translation_fallback():
    res = await bhashini_adapter.translate("Heavy rain expected", target_lang="hi")
    assert res is not None
    assert len(res) > 0
