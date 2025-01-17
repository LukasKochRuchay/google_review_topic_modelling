from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
import unidecode
import string
from openai import OpenAI
from langchain.prompts import PromptTemplate

def extract_sentences(sentence: str, client) -> str:
    try:
        # Format the prompt dynamically with the input sentence
        prompt = PromptTemplate.format(sentence=sentence)
        clien = client
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"


def translate_by_division(row, source_lang='de', target_lang='en', num_parts=10):

    if not isinstance(row, str):
        return row
    num_parts = max(num_parts, 1)
    num_parts = min(num_parts, len(row)) if len(row) > 0 else 1
    part_length = max(len(row) // num_parts, 1)

    chunks = [row[i:i+part_length] for i in range(0, len(row), part_length)]
    
    translated_chunks = []
    for chunk in chunks:
        try:
            translated_chunk = GoogleTranslator(source=source_lang, target=target_lang).translate(chunk)
            if translated_chunk is not None:  #
                translated_chunks.append(translated_chunk)
        except Exception as e:
            continue  
    
    return ' '.join(translated_chunks)

