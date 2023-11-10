from index.index_fetcher import IndexFetcher
from index.db import table_exists

query = {
    "question": "What are the types of car insurance?",
    "url": "https://insurify.com/car-insurance",
    "loader_name": "AsyncWebPageReader"
}

# query = {
#     "question": "What is SR22?",
#     "url": "https://insurify.com/sitemap-car-insurance.xml",
#     "loader_name": "SitemapReader"
# }

is_data_loaded = table_exists(query['url'])
index = IndexFetcher(url=query['url'], is_data_loaded=is_data_loaded, loader_name=query['loader_name']).index
query_engine = index.as_query_engine()
response = query_engine.query(query['question'])
sources = list({v['Source'] for v in response.metadata.values()})

print(str(response))

for i, s in enumerate(sources):
    print(f'Source {i + 1}: {s}')