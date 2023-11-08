from index.index_fetcher import IndexFetcher

fetcher = IndexFetcher()
index = fetcher.index
query_engine = index.as_query_engine()

response = query_engine.query("Can you tell me about the types of car insurance coverage?")

print(str(response))

sources = []
for v in response.metadata.values():
    sources.append(v['Source'])
for i, s in enumerate(set(sources)):
    print(f'Source {i + 1}: {s}')