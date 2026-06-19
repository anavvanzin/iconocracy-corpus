from iconocracy_corpus_sdk import IconocracyCorpusSdk, Environment

sdk = IconocracyCorpusSdk(base_url=Environment.DEFAULT.value, timeout=10000)

result = sdk.get.get_data()

print(result)
