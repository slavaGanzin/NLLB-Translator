import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline



TASK = 'translation'
CKPT = 'facebook/nllb-200-distilled-600M'
print('loading model')
device = 0 if torch.cuda.is_available() else -1
model = AutoModelForSeq2SeqLM.from_pretrained(CKPT)
tokenizer = AutoTokenizer.from_pretrained(CKPT)
