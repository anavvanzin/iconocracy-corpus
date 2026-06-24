import pytest
from pydantic import ValidationError

from tools.scripts.run_irr_pilot import PilotCodingResult, generate_mock_response


def test_json_parsing_adherence():
    raw_response = """
    {
      "item_id": "FR-COIN-001",
      "indicadores": {
        "desincorporacao": {"score": 2, "justification": "Idealized Marianne head but clear human contours."},
        "rigidez_postural": {"score": 1, "justification": "Profile display, minimal motion."},
        "dessexualizacao": {"score": 2, "justification": "Draped head, non-eroticized."},
        "uniformizacao_facial": {"score": 2, "justification": "Generic profile mask."},
        "heraldizacao": {"score": 1, "justification": "Laurel wreath symbol present."},
        "enquadramento_arquitetonico": {"score": 3, "justification": "Imprinted inside circular coin frame."},
        "apagamento_narrativo": {"score": 3, "justification": "No narrative, isolated portrait."},
        "monocromatizacao": {"score": 3, "justification": "Engraved in monochrome bronze/silver metal."},
        "serialidade": {"score": 3, "justification": "Millions of coins minted."},
        "inscricao_estatal": {"score": 3, "justification": "State coin containing 'Republique Francaise'."}
      }
    }
    """
    result = PilotCodingResult.model_validate_json(raw_response)
    assert result.item_id == "FR-COIN-001"
    assert result.indicadores.desincorporacao.score == 2
    assert result.indicadores.desincorporacao.justification == "Idealized Marianne head but clear human contours."

def test_invalid_pydantic_schema():
    # Scenario 1: missing field 'item_id'
    bad_response_1 = """
    {
      "indicadores": {}
    }
    """
    with pytest.raises(ValidationError):
        PilotCodingResult.model_validate_json(bad_response_1)

    # Scenario 2: out of bounds score (score = 4, must be 0 to 3)
    bad_response_2 = """
    {
      "item_id": "FR-COIN-001",
      "indicadores": {
        "desincorporacao": {"score": 4, "justification": "Out of bounds score"}
      }
    }
    """
    with pytest.raises(ValidationError):
        PilotCodingResult.model_validate_json(bad_response_2)

def test_generate_mock_response_validation():
    mock_dict = generate_mock_response("TEST-ITEM-123")
    result = PilotCodingResult.model_validate(mock_dict)
    assert result.item_id == "TEST-ITEM-123"
    assert result.indicadores.desincorporacao.score == 2
    assert isinstance(result.indicadores.desincorporacao.justification, str)
