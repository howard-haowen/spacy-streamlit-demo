from dragonmapper import hanzi, transcriptions
import jieba
import pandas as pd
import re
import requests 
import spacy
from spacy_streamlit import visualize_ner, visualize_tokens
#from spacy.language import Language
from spacy.tokens import Doc
import streamlit as st

# Global variables
ZH_TEXT = """（中央社）迎接虎年到來，台北101今天表示，即日起推出「虎年新春燈光秀」，將持續至2月5日，每晚6時至10時，除整點會有報時燈光變化外，每15分鐘還會有3分鐘的燈光秀。台北101下午透過新聞稿表示，今年特別設計「虎年新春燈光秀」，從今晚開始閃耀台北天際線，一直延續至2月5日，共7天。"""
DESCRIPTION = "AI模型輔助語言學習"
TOK_SEP = " | "
PUNCT_SYM = ["PUNCT", "SYM"]

# External API callers
def moedict_caller(word):
    st.write(f"### {word}")
    req = requests.get(f"https://www.moedict.tw/a/{word}.json")
    if req:
        with st.expander("點擊 + 檢視結果"):
            st.json(req.json())
    else:
        st.write("查無結果")
            
# Custom tokenizer class
class JiebaTokenizer:
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = jieba.cut(text) # returns a generator
        tokens = list(words) # convert the genetator to a list
        spaces = [False] * len(tokens)
        doc = Doc(self.vocab, words=tokens, spaces=spaces)
        return doc
    
# Utility functions
def filter_tokens(doc):
    clean_tokens = [tok for tok in doc if tok.pos_ not in PUNCT_SYM]
    clean_tokens = [tok for tok in clean_tokens if not tok.like_email]
    clean_tokens = [tok for tok in clean_tokens if not tok.like_url]
    # clean_tokens = [tok for tok in clean_tokens if not tok.like_num]
    clean_tokens = [tok for tok in clean_tokens if not tok.is_punct]
    clean_tokens = [tok for tok in clean_tokens if not tok.is_space]
    return clean_tokens

@st.cache
def load_tocfl_table(filename="./tocfl_wordlist.csv"):
    table = pd.read_csv(filename)
    return table
       
# Page setting
st.set_page_config(
    page_icon="🤠",
    layout="wide",
    initial_sidebar_state="auto",
)

# Choose a language and select functions
st.markdown(f"# {DESCRIPTION}") 

# Load the model
nlp = spacy.load('zh_core_web_sm')
          
# Merge entity spans to tokens
# nlp.add_pipe("merge_entities") 

# Select a tokenizer if the Chinese model is chosen
selected_tokenizer = st.radio("請選擇斷詞模型", ["jieba-TW", "spaCy"])
if selected_tokenizer == "jieba-TW":
    nlp.tokenizer = JiebaTokenizer(nlp.vocab)
default_text = ZH_TEXT

st.markdown("## 待分析文本")     
st.info("請在下面的文字框輸入文本並按下Ctrl + Enter以更新分析結果")
text = st.text_area("",  default_text, height=200)
doc = nlp(text)
st.markdown("---")

# Language-specific logic 
# keywords_extraction = st.sidebar.checkbox("關鍵詞分析", False) # YAKE doesn't work for Chinese texts
analyzed_text = st.checkbox("分析後文本", True)
defs_examples = st.checkbox("單詞解釋與例句", True)
# morphology = st.sidebar.checkbox("詞形變化", True)
ner_viz = st.checkbox("命名實體", True)
tok_table = st.checkbox("斷詞特徵", False)

if analyzed_text:
    st.markdown("## 分析後文本") 
    for idx, sent in enumerate(doc.sents):
        tokens_text = [tok.text for tok in sent if tok.pos_ not in PUNCT_SYM]
        pinyins = [hanzi.to_pinyin(word) for word in tokens_text]
        display = []
        for text, pinyin in zip(tokens_text, pinyins):
            res = f"{text} [{pinyin}]"
            display.append(res)
        if display:
            display_text = TOK_SEP.join(display)
            st.write(f"{idx+1} >>> {display_text}")
        else:
            st.write(f"{idx+1} >>> EMPTY LINE")

if defs_examples:
    st.markdown("## 單詞解析")
    clean_tokens = filter_tokens(doc)
    alphanum_pattern = re.compile(r"[a-zA-Z0-9]")
    clean_tokens_text = [tok.text for tok in clean_tokens if not alphanum_pattern.search(tok.text)]
    vocab = list(set(clean_tokens_text))
    if vocab:
        tocfl_table = load_tocfl_table()
        filt = table['詞彙'].isin(vocab)
        tocfl_res = tocfl_table[filt]
from dragonmapper import hanzi, transcriptions
import jieba
import pandas as pd
import re
import requests 
import spacy
from spacy_streamlit import visualize_ner, visualize_tokens
#from spacy.language import Language
from spacy.tokens import Doc
import streamlit as st

# Global variables
ZH_TEXT = """（中央社）迎接虎年到來，台北101今天表示，即日起推出「虎年新春燈光秀」，將持續至2月5日，每晚6時至10時，除整點會有報時燈光變化外，每15分鐘還會有3分鐘的燈光秀。台北101下午透過新聞稿表示，今年特別設計「虎年新春燈光秀」，從今晚開始閃耀台北天際線，一直延續至2月5日，共7天。"""
DESCRIPTION = "AI模型輔助語言學習"
TOK_SEP = " | "
PUNCT_SYM = ["PUNCT", "SYM"]

# External API callers
def moedict_caller(word):
    st.write(f"### {word}")
    req = requests.get(f"https://www.moedict.tw/a/{word}.json")
    if req:
        with st.expander("點擊 + 檢視結果"):
            st.json(req.json())
    else:
        st.write("查無結果")
            
# Custom tokenizer class
class JiebaTokenizer:
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = jieba.cut(text) # returns a generator
        tokens = list(words) # convert the genetator to a list
        spaces = [False] * len(tokens)
        doc = Doc(self.vocab, words=tokens, spaces=spaces)
        return doc
    
# Utility functions
def filter_tokens(doc):
    clean_tokens = [tok for tok in doc if tok.pos_ not in PUNCT_SYM]
    clean_tokens = [tok for tok in clean_tokens if not tok.like_email]
    clean_tokens = [tok for tok in clean_tokens if not tok.like_url]
    # clean_tokens = [tok for tok in clean_tokens if not tok.like_num]
    clean_tokens = [tok for tok in clean_tokens if not tok.is_punct]
    clean_tokens = [tok for tok in clean_tokens if not tok.is_space]
    return clean_tokens

@st.cache
def load_tocfl_table(filename="./tocfl_wordlist.csv"):
    table = pd.read_csv(filename)
    return table
       
# Page setting
st.set_page_config(
    page_icon="🤠",
    layout="wide",
    initial_sidebar_state="auto",
)

# Choose a language and select functions
st.markdown(f"# {DESCRIPTION}") 

# Load the model
nlp = spacy.load('zh_core_web_sm')
          
# Merge entity spans to tokens
# nlp.add_pipe("merge_entities") 

# Select a tokenizer if the Chinese model is chosen
selected_tokenizer = st.radio("請選擇斷詞模型", ["jieba-TW", "spaCy"])
if selected_tokenizer == "jieba-TW":
    nlp.tokenizer = JiebaTokenizer(nlp.vocab)
default_text = ZH_TEXT

st.markdown("## 待分析文本")     
st.info("請在下面的文字框輸入文本並按下Ctrl + Enter以更新分析結果")
text = st.text_area("",  default_text, height=200)
doc = nlp(text)
st.markdown("---")

# Language-specific logic 
# keywords_extraction = st.sidebar.checkbox("關鍵詞分析", False) # YAKE doesn't work for Chinese texts
analyzed_text = st.checkbox("分析後文本", True)
defs_examples = st.checkbox("單詞解釋與例句", True)
# morphology = st.sidebar.checkbox("詞形變化", True)
ner_viz = st.checkbox("命名實體", True)
tok_table = st.checkbox("斷詞特徵", False)

if analyzed_text:
    st.markdown("## 分析後文本") 
    for idx, sent in enumerate(doc.sents):
        tokens_text = [tok.text for tok in sent if tok.pos_ not in PUNCT_SYM]
        pinyins = [hanzi.to_pinyin(word) for word in tokens_text]
        display = []
        for text, pinyin in zip(tokens_text, pinyins):
            res = f"{text} [{pinyin}]"
            display.append(res)
        if display:
            display_text = TOK_SEP.join(display)
            st.write(f"{idx+1} >>> {display_text}")
        else:
            st.write(f"{idx+1} >>> EMPTY LINE")

if defs_examples:
    st.markdown("## 單詞解析")
    clean_tokens = filter_tokens(doc)
    alphanum_pattern = re.compile(r"[a-zA-Z0-9]")
    clean_tokens_text = [tok.text for tok in clean_tokens if not alphanum_pattern.search(tok.text)]
    vocab = list(set(clean_tokens_text))
    if vocab:
        tocfl_table = load_tocfl_table()
        filt = table['詞彙'].isin(vocab)
        tocfl_res = tocfl_table[filt]
from dragonmapper import hanzi, transcriptions
import jieba
import pandas as pd
import re
import requests 
import spacy
from spacy_streamlit import visualize_ner, visualize_tokens
#from spacy.language import Language
from spacy.tokens import Doc
import streamlit as st

# Global variables
ZH_TEXT = """（中央社）迎接虎年到來，台北101今天表示，即日起推出「虎年新春燈光秀」，將持續至2月5日，每晚6時至10時，除整點會有報時燈光變化外，每15分鐘還會有3分鐘的燈光秀。台北101下午透過新聞稿表示，今年特別設計「虎年新春燈光秀」，從今晚開始閃耀台北天際線，一直延續至2月5日，共7天。"""
DESCRIPTION = "AI模型輔助語言學習"
TOK_SEP = " | "
PUNCT_SYM = ["PUNCT", "SYM"]

# External API callers
def moedict_caller(word):
    st.write(f"### {word}")
    req = requests.get(f"https://www.moedict.tw/a/{word}.json")
    if req:
        with st.expander("點擊 + 檢視結果"):
            st.json(req.json())
    else:
        st.write("查無結果")
            
# Custom tokenizer class
class JiebaTokenizer:
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = jieba.cut(text) # returns a generator
        tokens = list(words) # convert the genetator to a list
        spaces = [False] * len(tokens)
        doc = Doc(self.vocab, words=tokens, spaces=spaces)
        return doc
    
# Utility functions
def filter_tokens(doc):
    clean_tokens = [tok for tok in doc if tok.pos_ not in PUNCT_SYM]
    clean_tokens = [tok for tok in clean_tokens if not tok.like_email]
    clean_tokens = [tok for tok in clean_tokens if not tok.like_url]
    # clean_tokens = [tok for tok in clean_tokens if not tok.like_num]
    clean_tokens = [tok for tok in clean_tokens if not tok.is_punct]
    clean_tokens = [tok for tok in clean_tokens if not tok.is_space]
    return clean_tokens

@st.cache
def load_tocfl_table(filename="./tocfl_wordlist.csv"):
    table = pd.read_csv(filename)
    return table
       
# Page setting
st.set_page_config(
    page_icon="🤠",
    layout="wide",
    initial_sidebar_state="auto",
)

# Choose a language and select functions
st.markdown(f"# {DESCRIPTION}") 

# Load the model
nlp = spacy.load('zh_core_web_sm')
          
# Merge entity spans to tokens
# nlp.add_pipe("merge_entities") 

# Select a tokenizer if the Chinese model is chosen
selected_tokenizer = st.radio("請選擇斷詞模型", ["jieba-TW", "spaCy"])
if selected_tokenizer == "jieba-TW":
    nlp.tokenizer = JiebaTokenizer(nlp.vocab)
default_text = ZH_TEXT

st.markdown("## 待分析文本")     
st.info("請在下面的文字框輸入文本並按下Ctrl + Enter以更新分析結果")
text = st.text_area("",  default_text, height=200)
doc = nlp(text)
st.markdown("---")

# Language-specific logic 
# keywords_extraction = st.sidebar.checkbox("關鍵詞分析", False) # YAKE doesn't work for Chinese texts
analyzed_text = st.checkbox("分析後文本", True)
defs_examples = st.checkbox("單詞解釋與例句", True)
# morphology = st.sidebar.checkbox("詞形變化", True)
ner_viz = st.checkbox("命名實體", True)
tok_table = st.checkbox("斷詞特徵", False)

if analyzed_text:
    st.markdown("## 分析後文本") 
    for idx, sent in enumerate(doc.sents):
        tokens_text = [tok.text for tok in sent if tok.pos_ not in PUNCT_SYM]
        pinyins = [hanzi.to_pinyin(word) for word in tokens_text]
        display = []
        for text, pinyin in zip(tokens_text, pinyins):
            res = f"{text} [{pinyin}]"
            display.append(res)
        if display:
            display_text = TOK_SEP.join(display)
            st.write(f"{idx+1} >>> {display_text}")
        else:
            st.write(f"{idx+1} >>> EMPTY LINE")

if defs_examples:
    st.markdown("## 單詞解析")
    clean_tokens = filter_tokens(doc)
    alphanum_pattern = re.compile(r"[a-zA-Z0-9]")
    clean_tokens_text = [tok.text for tok in clean_tokens if not alphanum_pattern.search(tok.text)]
    vocab = list(set(clean_tokens_text))
    if vocab:
        tocfl_table = load_tocfl_table()
        filt = table['詞彙'].isin(vocab)
        tocfl_res = tocfl_table[filt]
        st.markdown("### 華語詞彙分級")
        st.dataframe(tocfl_res)
        st.markdown("---")
        st.markdown("### 單詞解釋與例句")
        selected_words = st.multiselect("請選擇要查詢的單詞: ", vocab, vocab[0:3])
        for w in selected_words:
            moedict_caller(w)                        

if ner_viz:
    ner_labels = nlp.get_pipe("ner").labels
    visualize_ner(doc, labels=ner_labels, show_table=False, title="命名實體")
    
if tok_table:
    visualize_tokens(doc, attrs=["text", "pos_", "tag_", "dep_", "head"], title="斷詞特徵")
