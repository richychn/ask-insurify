from transformers import AutoModel, AutoTokenizer
from os import getcwd

dir = getcwd()

model_name = "BAAI/bge-small-en"

model = AutoModel.from_pretrained(model_name, cache_dir=None, trust_remote_code=False)
tokenizer = AutoTokenizer.from_pretrained(model_name)

model.save_pretrained(f'{dir}/app/weights/embed_model/')
tokenizer.save_pretrained(f'{dir}/app/weights/embed_tokenizer/')