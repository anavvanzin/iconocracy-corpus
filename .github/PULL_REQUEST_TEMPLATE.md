## Summary

Describe the intent of this change in 2-4 lines.

## Surface

- [ ] Corpus/data
- [ ] Coding/analysis
- [ ] Writing/docs
- [ ] Infra/publishing

## Checks

- [ ] `python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose`
- [ ] `python tools/scripts/code_purification.py --status` if coding-related
- [ ] `python tools/scripts/vault_sync.py status` or `diff` if vault-facing
- [ ] Release/docs updated if GitHub Pages or Hugging Face is affected

## Notes

List any known drift, skipped checks, or external follow-up.
