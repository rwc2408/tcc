import pandas as pd
import re
from cleantext import clean
import nltk
from nltk.tokenize import word_tokenize
import spacy

from unidecode import unidecode


spacy.cli.download("pt_core_news_sm")
nlp = spacy.load('pt_core_news_sm')

df = pd.read_csv('teste1.csv')

stopword_list = nltk.corpus.stopwords.words('portuguese') + ['https']
stopwords_list = [unidecode(w) for w in stopword_list]

# Normalização dos dados (remoção de stopwords, pontuação, etc)
def normalize_text(text: str): 
    return  " ".join([word for word in word_tokenize(text.lower()) if word not in stopwords_list and word.isalpha()])

# Geração de coluna normalizada com base em outra coluna
def generate_normalized_column(data: pd.DataFrame, from_column: str):
    new_column_name = f"{from_column}_Normalized"
    print(f"New column name: {new_column_name}")
    data[new_column_name] = data.apply(lambda linha: normalize_text(str(linha[from_column])), axis = 1)
    return new_column_name

def preprocess(text):
    
    text = re.sub(r'https://t.co/(\w)*', ' ', text)                     # remove links
    text = re.sub(r'@\w+', ' ', text)                                   # remove os arrobas
    text = re.sub(r'#\w+', ' ', text)                                   # remove as hashtags
    text = text.lower()                                                 # minimiza o texto
    text = re.sub(r'\d+\/\d+\s', ' ', text)                             # remove contagem de posts

    text = unidecode(text)                                              # remove acentos 
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)                         # remove caracteres especiais
    text = re.sub(r'\s+', ' ', text)                                    # remove as quebras de linhas desnecessarias
    
    tokens = [word for word in text.split() if word not in stopwords_list]   # remove as stopwords
    
    return ' '.join(tokens)

normalized_summary_column_name = generate_normalized_column(data=df, from_column="text")

df['word_count'] = df['text_Normalized'].apply(lambda x: len(str(x).split()))

df = df[df.word_count >= 5]

df['text_processed'] = df['text'].apply(preprocess)

print(df.info())

df.drop_duplicates(subset='text_processed', inplace=True)

print(df.info())

df.to_csv('tweets_prefeito_vacina_preprocessed2.csv', index=False)