from sentence_transformers import SentenceTransformer, util
import torch
from transformers import pipeline
from transformers import AutoTokenizer, pipeline, logging
from chatgpt import generate_message
import asyncio

simm = SentenceTransformer('Sakil/sentence_similarity_semantic_search')

summarizer = pipeline("summarization", model="knkarthick/MEETING_SUMMARY")



use_triton = False

blocks=[]

async def save(txt):
  chunks=[txt[i:i+1000] for i in range(0, len(txt), 1000)]
  blocks.append("\n".join([summarizer(i, truncation=True)[0]['summary_text'] for i in chunks]))

async def findbest(contx,n):
  if len(blocks)==0: return []
  contx=simm.encode(contx)
  embeddings = simm.encode(blocks)
  cos_sim = util.cos_sim(embeddings, contx)
  sentence_combinations=[]
  for j in range(len(cos_sim)):
      sentence_combinations.append([cos_sim[j], blocks[j]])

  sentence_combinations = sorted(sentence_combinations, key=lambda x: x[0], reverse=True)
  return list(zip(*sentence_combinations[:n]))[1]

async def generate(context,remember=1):
  intro="\n".join(await findbest(context,remember))+"\n"
  text=intro+context
  return await generate_message(text)

async def main(txt):
   await save(txt=txt)
   await generate(context=txt)
   
asyncio.run(main('в траве сидел кузнечик'))