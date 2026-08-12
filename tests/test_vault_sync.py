from tools.scripts.vault_sync import _vault_note_to_record


def test_vault_import_with_regime_remains_pending_not_zero_coded():
    record = _vault_note_to_record(
        {
            "id": "BR-999",
            "titulo": "Alegoria de teste",
            "url": "https://example.org/object/999",
            "pais": "BR",
            "regime": "normativo",
            "_file": "BR-999 Alegoria de teste.md",
        }
    )

    assert "purificacao" not in record
    claim = record["iconocode"]["interpretation"][0]
    assert claim["claim_text"] == "Regime iconocrático: NORMATIVO"
    assert claim["status"] == "tentative"
    assert "coding-pending" in record["exports"]["audit_flags"]


def test_vault_import_without_regime_remains_pending():
    record = _vault_note_to_record(
        {
            "id": "BR-998",
            "titulo": "Alegoria sem regime",
            "url": "https://example.org/object/998",
            "pais": "BR",
            "_file": "BR-998 Alegoria sem regime.md",
        }
    )

    assert "purificacao" not in record
    assert record["iconocode"]["interpretation"][0]["status"] == "tentative"
    assert "coding-pending" in record["exports"]["audit_flags"]
