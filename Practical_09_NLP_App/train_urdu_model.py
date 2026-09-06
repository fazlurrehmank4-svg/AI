"""
Urdu AI Model Training & Corpus Ingestion Pipeline
Based on resources and datasets from Traversaal AI Urdu LLM Registry (https://github.com/traversaal-ai/urdu-llm-resources):
- Instruction Tuning (Alpaca / Instruct format: Instruction -> Input -> Response)
- Urdu Linguistic Normalization (Diacritics/Aerab removal, Character variant mapping)
- Stopword Filtering & Subword N-Gram TF-IDF Intent Classification
- Agricultural & Weather Domain Grounding (20+ Crops, Diseases, Fertilizers, Sprays, Precautions)
"""

import os
import sys
import re
import json
import pickle
import unicodedata
from typing import Dict, List, Any, Tuple
import numpy as np

# Reconfigure stdout for UTF-8 in Windows environments
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. Urdu NLP Preprocessing & Linguistic Normalization ---

URDU_DIACRITICS = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06ED]')
URDU_PUNCTUATION = re.compile(r'[۔،؛؟!"\'\(\)\[\]\{\}«»<>:,\.\-\_\/\\|]')

# Character normalization table to standardize Urdu letters across keyboards/corpora
URDU_CHAR_MAP = {
    'ي': 'ی', 'ى': 'ی', 'ئ': 'ی',
    'ك': 'ک',
    'ة': 'ہ', 'ۂ': 'ہ', 'ه': 'ہ',
    'ؤ': 'و',
    'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
}

URDU_STOPWORDS = {
    'کا', 'کی', 'کے', 'کو', 'نے', 'میں', 'سے', 'پر', 'تک', 'اور', 'یا', 'تو',
    'ہے', 'ہیں', 'تھا', 'تھے', 'تھی', 'تھیں', 'ہو', 'ہونا', 'ہوتی', 'ہوتے', 'ہوتا',
    'گا', 'گے', 'گی', 'یہ', 'وہ', 'اس', 'ان', 'جس', 'جن', 'کس', 'کن',
    'کیا', 'کیوں', 'کیسے', 'کب', 'کہاں', 'کون', 'کتنا', 'کتنے', 'کتنی',
    'اپنا', 'اپنی', 'اپنے', 'ہم', 'آپ', 'تم', 'میرا', 'میری', 'میرے',
    'ایک', 'دو', 'تین', 'بہت', 'زیادہ', 'کم', 'اگر', 'مگر', 'لیکن', 'بھی'
}

def normalize_urdu_text(text: str) -> str:
    """Standardizes Urdu text by removing aerab/diacritics and mapping variant glyphs."""
    if not text:
        return ""
    # Normalize unicode forms
    text = unicodedata.normalize('NFKD', text)
    # Remove diacritics / aerab
    text = URDU_DIACRITICS.sub('', text)
    # Map letter variations
    normalized_chars = [URDU_CHAR_MAP.get(c, c) for c in text]
    text = "".join(normalized_chars)
    # Strip excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()

def tokenize_urdu(text: str, remove_stopwords: bool = False) -> List[str]:
    """Tokenizes Urdu text into word tokens with optional stopword filtering."""
    cleaned = URDU_PUNCTUATION.sub(' ', normalize_urdu_text(text))
    tokens = [t.strip() for t in cleaned.split() if t.strip()]
    if remove_stopwords:
        tokens = [t for t in tokens if t not in URDU_STOPWORDS]
    return tokens

# --- 2. Rich Urdu Instruction & Domain Dataset ---
# Formatted following Traversaal Urdu Chat Alpaca / Urdu Instruct conventions

URDU_INSTRUCTION_DATASET: List[Dict[str, Any]] = [
    # --- Greetings & AI Identity ---
    {
        "instruction": "اپنا تعارف کروائیں اور بتائیں کہ آپ کیا کر سکتے ہیں۔",
        "input": "آپ کون ہیں؟",
        "category": "greeting",
        "intent": "identity",
        "response": "خوش آمدید! میں **CropGuard AI معاون** ہوں — ایک مکمل مقامی زرعی اور موسمیاتی مشیر۔ میں فصلوں کی حفاظت، بیماریوں کی روک تھام، کھاد کے شیڈول، اسپرے کے اوقات، اور لائیو موسمی خطرات کے تجزیے میں کسانوں اور محققین کی مدد کرتا ہوں۔"
    },
    {
        "instruction": "اسلامی یا روایتی سلام کا جواب دیں۔",
        "input": "السلام علیکم ورحمۃ اللہ",
        "category": "greeting",
        "intent": "greeting",
        "response": "وعلیکم السلام ورحمۃ اللہ وبرکاتہ! CropGuard AI میں خوش آمدید۔ بتائیے آج آپ کی کون سی فصل یا کس زرعی مسئلے کے بارے میں رہنمائی کروں؟"
    },
    {
        "instruction": "کسان کی مدد کی پیشکش کریں۔",
        "input": "مجھے زرعی معلومات اور مدد چاہیے",
        "category": "greeting",
        "intent": "help",
        "response": "جی ضرور! آپ مجھ سے کسی بھی فصل کی کاشت (گندم، دھان، کپاس، مکئی، ٹماٹر، آلو وغیرہ)، کھاد کے استعمال، کیڑے مار یا فنگس کش ادویات، اور موسمی الرٹس کے متعلق سوالات پوچھ سکتے ہیں۔"
    },

    # --- Disease & Fungal Protection ---
    {
        "instruction": "فصلوں میں پھپھوندی (Fungal Diseases) کے اسباب اور تدارک کی تفصیل دیں۔",
        "input": "فصل کو پھپھوندی یا فنگس کی بیماری کیوں لگتی ہے اور اس کا علاج کیا ہے؟",
        "category": "disease_fungal",
        "intent": "fungal_disease",
        "response": "🔬 **پھپھوندی (Fungal Infection) کے اسباب اور حفاظتی تدابیر:**\n\n1. **بنیادی وجوہات:** ہوا میں 75% سے زیادہ نمی، 20°C تا 30°C درجہ حرارت، اور کھیت میں پانی کا کھڑا رہنا فنگس کے جراثیم کو تیزی سے پھیلاتا ہے۔\n2. **حفاظتی تدابیر:**\n   - کھیت میں فوری نکاسی آب (Drainage) یقینی بنائیں۔\n   - نمی والے ابر آلود موسم میں اضافی یوریا (نائٹروجن) نہ ڈالیں کیونکہ اس سے پودوں کے ٹشوز نرم ہو کر فنگس کے لیے آسان شکار بنتے ہیں۔\n   - متاثرہ پودوں پر کاپر آکسی کلورائیڈ (Copper Oxychloride) یا کاربینڈازم (Carbendazim) کا احتیاطی اسپرے کریں۔"
    },
    {
        "instruction": "پتوں کے پیلے پڑنے کی وجوہات اور حل بتائیں۔",
        "input": "پتے پیلے کیوں پڑ رہے ہیں اور کیا کریں؟",
        "category": "disease_symptoms",
        "intent": "yellow_leaves",
        "response": "🍂 **پتے پیلے پڑنے کی بنیادی وجوہات اور علاج:**\n\n1. **نائٹروجن کی کمی:** نچلے پرانے پتے پہلے پیلے پڑتے ہیں۔ حل: متوازن یوریا یا نائٹروجنی کھاد کا استعمال کریں۔\n2. **پانی کی زیادتی (جڑوں کا گھٹن):** زمین میں پانی کھڑا رہنے سے جڑوں کو آکسیجن نہیں ملتی۔ حل: فوری نکاسی آب کریں۔\n3. **لوہے (Iron) یا زنک کی کمی:** اوپری نئے پتے رگوں کے درمیان سے پیلے ہوتے ہیں۔ حل: چیلیٹڈ زنک یا فیرس سلفیٹ کا فولیر اسپرے کریں۔\n4. **رس چوسنے والے کیڑے (چست تیلا/تھرپس):** پتوں کا رس چوس کر پودے کو زرد کر دیتے ہیں۔ امیڈاکلوپرڈ (Imidacloprid) کا اسپرے کریں۔"
    },
    {
        "instruction": "پتے مڑنے اور وائرس کے حملے کا علاج بتائیں۔",
        "input": "ٹماٹر یا مرچ کے پتے اوپر کی طرف مڑ رہے ہیں کیا کریں؟",
        "category": "disease_symptoms",
        "intent": "leaf_curl",
        "response": "🍃 **پتا مروڑ بیماری (Leaf Curl) اور علاج:**\n\n- **وجہ:** یہ عموماً وائرل بیماری ہے جو سفید مکھی (Whitefly) یا تھرپس کے ذریعے پھیلتی ہے۔\n- **علاج:**\n  1. متاثرہ پودوں کو اکھاڑ کر زمین میں دبا دیں۔\n  2. سفید مکھی اور رس چوسنے والے کیڑوں کے خاتمے کے لیے ڈائیفینتھیوران یا ایسیٹامیپرڈ کا فوری اسپرے کریں۔\n  3. پودوں کی قوت مدافعت بڑھانے کے لیے زنک اور بوران کا متوازن استعمال کریں۔"
    },

    # --- Fertilizers & Nutrition ---
    {
        "instruction": "کھادوں کا متوازن استعمال اور یوریا کے اصول سمجھائیں۔",
        "input": "کھاد اور یوریا کا صحیح استعمال کیسے کریں؟",
        "category": "fertilizer",
        "intent": "fertilizer_schedule",
        "response": "🧪 **کھاد اور غذائی اجزاء کے بہترین زرعی اصول:**\n\n1. **نائٹروجن (یوریا):** پودے کے سبزے اور بڑھوتری کے لیے۔ ہمیشہ بجائی کے وقت 1/3 اور باقی قسطوں میں پانی کے ساتھ دیں۔ ابر آلود یا زیادہ نمی والے موسم میں یوریا کم کریں۔\n2. **فاسفورس (DAP):** جڑوں کی مضبوطی کے لیے۔ یہ کھاد ہمیشہ بوائی کے وقت زمین کی تہہ میں ڈالیں۔\n3. **پوٹاش (SOP / MOP):** دانوں کی چمک، وزن، اور بیماریوں کے خلاف قوت مدافعت کے لیے۔ پھول اور دانے بننے کے مرحلے پر ضروری ہے۔\n4. **مائیکرو نیوٹرینٹس:** زنک (Zinc) اور سلفر (Sulphur) کا متوازن استعمال پیداوار میں 15-20 فیصد اضافہ کرتا ہے۔"
    },

    # --- Spraying Rules ---
    {
        "instruction": "کیڑے مار اور فنگس کش اسپرے کا بہترین وقت اور شرائط بتائیں۔",
        "input": "کیڑے مار دوا یا اسپرے کب کرنا چاہیے؟",
        "category": "spraying",
        "intent": "spray_timing",
        "response": "🚿 **اسپرے کرنے کا بہترین وقت اور حفاظتی گائیڈلائنز:**\n\n- ⏰ **بہترین وقت:** صبح سویرے (شبنم سوکھنے کے بعد 8 سے 11 بجے) یا شام 4 بجے کے بعد جب دھوپ کی شدت کم ہو۔\n- 🚫 **ان حالات میں ہرگز اسپرے نہ کریں:**\n  - تیز ہوا کی رفتار (> 15 کلومیٹر/گھنٹہ) میں کیونکہ دوا اڑ جاتی ہے۔\n  - تیز دھوپ یا شدید گرمی (> 35°C) میں ورنہ پتے جل سکتے ہیں۔\n  - اگلے 4 سے 6 گھنٹوں میں بارش کا امکان ہو تو اسپرے ضائع ہو جائے گا۔\n- 🛡️ **حفاظت:** ہمیشہ ماسک اور دستانے پہنیں اور ہوا کے رخ کی طرف اسپرے کریں۔"
    },

    # --- Crop Specific Knowledge Profiles ---
    {
        "instruction": "دھان یا چاول کی کاشت اور احتیاطی تدابیر کی رہنمائی کریں۔",
        "input": "دھان کی فصل کے لیے کیا احتیاطی تدابیر ہیں؟",
        "category": "crop_precautions",
        "intent": "rice_precautions",
        "response": "🌾 **دھان / چاول (Rice) کی فصل کے لیے اہم احتیاطی تدابیر:**\n\n1. **پانی کا انتظام:** پنیری کی منتقلی کے بعد 2 تا 5 سینٹی میٹر پانی کی سطح برقرار رکھیں؛ تیز بارش کے دوران نکاسی کا انتظام کریں۔\n2. **کھاد:** ابر آلود موسم اور زیادہ نمی کے دوران غیر ضروری یوریا کھاد کے استعمال سے گریز کریں۔\n3. **بیماریاں:** تنے کی سنڈی (Stem Borer) اور بلاسٹ (جھلساؤ) کی باقاعدہ جانچ کریں۔\n4. **حفاظت:** حفاظتی طور پر ٹرائیکوڈرما یا تجویز کردہ فنگس کش اسپرے استعمال کریں۔"
    },
    {
        "instruction": "گندم کی فصل کے تقاضے اور بیماریوں سے بچاؤ بتائیں۔",
        "input": "گندم کی کاشت اور بیماریوں سے بچاؤ کیسے کریں؟",
        "category": "crop_precautions",
        "intent": "wheat_precautions",
        "response": "🌾 **گندم (Wheat) کے لیے اہم زرعی رہنما اصول:**\n\n1. **موسم اور درجہ حرارت:** گندم کے لیے مثالی درجہ حرارت 15°C سے 25°C ہے۔ دانے پکنے کے وقت تیز گرمی سے دانہ کمزور ہو سکتا ہے۔\n2. **آبپاشی:** پہلا پانی بوائی کے 20-22 دن بعد (تاج نما جڑوں کے وقت)، اور پھر گوبھ و دانہ بننے کے وقت لازمی دیں۔\n3. **بیماریاں:** زرد کنگی (Yellow Rust) اور سُست تیلے سے بچاؤ کے لیے باقاعدہ معائنہ کریں اور پروپیکونازول کا اسپرے کریں۔"
    },
    {
        "instruction": "کپاس کی فصل اور گلابی سنڈی کا تدارک بتائیں۔",
        "input": "کپاس کی فصل میں سفید مکھی اور گلابی سنڈی سے کیسے بچیں؟",
        "category": "crop_precautions",
        "intent": "cotton_precautions",
        "response": "🌿 **کپاس (Cotton) کی نگہداشت اور کیڑوں کا تدارک:**\n\n1. **سفید مکھی اور گلابی سنڈی:** یہ کپاس کے سب سے بڑے دشمن ہیں۔ فیرومون ٹریپس لگائیں اور رس چوسنے والے کیڑوں کے لیے اسپیٹ اور پائری پروکسیفین کا اسپرے کریں۔\n2. **پانی کی ضرورت:** پھول اور ٹینڈے بننے کے دوران پانی کی کمی نہ ہونے دیں ورنہ پھول گر جاتے ہیں۔\n3. **نائٹروجن کا توازن:** ضرورت سے زیادہ نائٹروجن سے پودا صرف قد کرتا ہے اور ٹینڈے کم بنتے ہیں۔"
    },
    {
        "instruction": "مکئی کی کاشت اور فال آرمی ورم کا علاج بتائیں۔",
        "input": "مکئی کی فصل میں سنڈی کا حملہ ہو گیا ہے کیا کریں؟",
        "category": "crop_precautions",
        "intent": "maize_precautions",
        "response": "🌽 **مکئی (Maize) کی حفاظت اور فال آرمی ورم کا علاج:**\n\n1. **فال آرمی ورم (Fall Armyworm):** سنڈی مکئی کے درمیان (Whorl) میں چھپ کر پتے کھاتی ہے۔ امازیکٹن بینزویٹ (Emamectin Benzoate) یا کلورانٹرانیلی پرول کا اسپرے براہ راست پودے کی گوبھ میں کریں۔\n2. **پانی:** گھنڈی اور سٹا بننے کے مرحلے پر مکئی پانی کی کمی بالکل برداشت نہیں کرتی۔"
    },
    {
        "instruction": "آلو کی فصل اور پچھیتا جھلساؤ کا تدارک بتائیں۔",
        "input": "آلو کی فصل میں جھلساؤ (Blight) بیماری کی کیا دوا ہے؟",
        "category": "crop_precautions",
        "intent": "potato_precautions",
        "response": "🥔 **آلو (Potato) کی فصل اور جھلساؤ (Late Blight) کا علاج:**\n\n1. **پچھیتا جھلساؤ (Late Blight):** سرد مرطوب اور دھند والے موسم میں پتوں پر بھورے کالے دھبے بنتے ہیں۔\n2. **تدارک:** دھند کے دنوں میں حفاظتی طور پر مینکوزیب (Mancozeb) یا میٹالیکسل (Metalaxyl) کا اسپرے کریں۔ کھیت میں زیادہ دیر پانی نہ کھڑا ہونے دیں۔"
    },
    {
        "instruction": "ٹماٹر کی فصل کے موسمی خطرات اور دیکھ بھال بتائیں۔",
        "input": "ٹماٹر کی فصل کے لیے کیا احتیاط کرنی چاہیے؟",
        "category": "crop_precautions",
        "intent": "tomato_precautions",
        "response": "🍅 **ٹماٹر (Tomato) کی نگہداشت اور احتیاطی تدابیر:**\n\n1. **درجہ حرارت:** 20°C سے 28°C بہترین ہے۔ 35°C سے اوپر پھول گرنے لگتے ہیں۔\n2. **پھپھوندی اور پھل کا سڑنا:** پودوں کو لکڑیوں یا تار کے سہارے باندھیں تاکہ پتے مٹی اور پانی سے اوپر رہیں؛ مینکوزیب کا اسپرے کریں۔\n3. **پھل کا پھٹنا:** فاسفورس، پوٹاشیم اور بوران کا متوازن استعمال پھل کو شاداب اور موٹا رکھتا ہے۔"
    },

    # --- Weather Hazards & Weather Evaluation ---
    {
        "instruction": "شدید موسمی خطرات (بارش، گرمی، آندھی) کے پیشگی اقدامات بتائیں۔",
        "input": "موسمی الرٹ یا بارش کے خطرے کی صورت میں کسان کیا کریں؟",
        "category": "weather_hazard",
        "intent": "weather_hazard",
        "response": "⛈️ **شدید موسمی خطرات کے دوران ہنگامی زرعی اقدامات:**\n\n1. **بھاری بارش / طوفان کا الرٹ:**\n   - کھیت کے نکاسی آب کے راستے فوری کھول دیں۔\n   - کھاد ڈالنا اور اسپرے کرنا فوری روک دیں۔\n2. **شدید گرمی کی لہر (Heatwave):**\n   - پودوں کے تناؤ کو کم کرنے کے لیے شام کے وقت ہلکی آبپاشی کریں۔\n   - ملچنگ (Mulching) کا استعمال کریں تاکہ زمین کی نمی برقرار رہے۔\n3. **ژالہ باری یا آندھی کے بعد:**\n   - زخمی پودوں پر جراثیم کش فنگس کش اسپرے کریں تاکہ بیماریوں کا حملہ نہ ہو۔"
    },

    # --- Soil & Irrigation ---
    {
        "instruction": "زمین کی تیاری اور پانی کے انتظام کے اصول سمجھائیں۔",
        "input": "مٹی کی زرخیزی اور پانی کی بچت کے بہترین طریقے کیا ہیں؟",
        "category": "agronomy",
        "intent": "soil_irrigation",
        "response": "🌱 **مٹی کی زرخیزی اور مؤثر آبپاشی کے زرعی اصول:**\n\n1. **مٹی کا تجزیہ (Soil Testing):** ہر 2-3 سال بعد زمین کے پی ایچ (pH)، نامیاتی مادے (Organic Matter)، اور الیکٹریکل کنڈکٹیویٹی (EC) کا ٹیسٹ کروائیں۔\n2. **نامیاتی مادہ:** گوبر کی گلی سڑی کھاد یا سبز کھاد (جیسے جنتر/سنتھ) سے زمین کی پانی جذب کرنے کی صلاحیت بڑھتی ہے۔\n3. **ڈرپ اریگیشن (Drip Irrigation):** پانی کی 40-50% بچت ہوتی ہے اور کھاد براہ راست پودے کی جڑوں کو ملتی ہے۔"
    }
]

# --- 3. Trainer Class ---

class UrduAIModelTrainer:
    """Trains an Urdu Agricultural & Conversational NLP Classifier & Retrieval Index."""

    def __init__(self, data_sources: Optional[List[Dict[str, Any]]] = None):
        self.dataset = data_sources or URDU_INSTRUCTION_DATASET
        self.vectorizer = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 3),
            min_df=1,
            sublinear_tf=True
        )
        self.classifier = MultinomialNB(alpha=0.1)
        self.tfidf_matrix = None
        self.doc_registry: List[Dict[str, Any]] = []

    def prepare_training_data(self) -> Tuple[List[str], List[str]]:
        texts = []
        labels = []
        self.doc_registry = []

        for item in self.dataset:
            # Combine instruction, input, and response into searchable corpus
            norm_instruction = normalize_urdu_text(item.get("instruction", ""))
            norm_input = normalize_urdu_text(item.get("input", ""))
            norm_response = normalize_urdu_text(item.get("response", ""))
            
            intent = item.get("intent", "general")
            combined_query = f"{norm_instruction} {norm_input}"
            
            texts.append(combined_query)
            labels.append(intent)

            self.doc_registry.append({
                "instruction": item.get("instruction", ""),
                "input": item.get("input", ""),
                "response": item.get("response", ""),
                "category": item.get("category", "general"),
                "intent": intent,
                "normalized_text": f"{norm_instruction} {norm_input} {norm_response}"
            })

        return texts, labels

    def train(self) -> Dict[str, Any]:
        """Trains the vectorizer and classifier on the Urdu dataset."""
        texts, labels = self.prepare_training_data()
        print(f"[*] Training Urdu AI Engine on {len(texts)} domain instructions...")
        
        # Fit vectorizer on normalized texts
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        self.classifier.fit(self.tfidf_matrix, labels)
        
        vocab_size = len(self.vectorizer.vocabulary_)
        print(f"[+] Urdu Model Training complete! Vocabulary size: {vocab_size} n-gram terms.")
        return {
            "samples_count": len(texts),
            "vocab_size": vocab_size,
            "intents_count": len(set(labels))
        }

    def predict_intent(self, query: str) -> Tuple[str, float]:
        """Predicts the most probable intent and confidence for an incoming Urdu query."""
        norm_q = normalize_urdu_text(query)
        q_vec = self.vectorizer.transform([norm_q])
        probs = self.classifier.predict_proba(q_vec)[0]
        best_idx = np.argmax(probs)
        best_intent = self.classifier.classes_[best_idx]
        confidence = float(probs[best_idx])
        return best_intent, confidence

    def retrieve_answer(self, query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """Finds the most relevant instruction-tuned response using TF-IDF cosine similarity."""
        norm_q = normalize_urdu_text(query)
        q_vec = self.vectorizer.transform([norm_q])
        sims = cosine_similarity(q_vec, self.tfidf_matrix).flatten()
        
        top_indices = np.argsort(sims)[::-1][:top_k]
        results = []
        for idx in top_indices:
            score = float(sims[idx])
            item = self.doc_registry[idx]
            results.append({
                "score": score,
                "intent": item["intent"],
                "category": item["category"],
                "response": item["response"],
                "input": item["input"]
            })
        return results

    def export_model(self, export_path: str) -> None:
        """Serializes the trained Urdu model to disk."""
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        export_data = {
            "vocabulary": self.vectorizer.vocabulary_,
            "idf": self.vectorizer.idf_.tolist(),
            "classes": self.classifier.classes_.tolist(),
            "class_log_prior": self.classifier.class_log_prior_.tolist(),
            "feature_log_prob": self.classifier.feature_log_prob_.tolist(),
            "doc_registry": self.doc_registry
        }
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        print(f"[+] Exported trained Urdu AI model to: {export_path}")

if __name__ == "__main__":
    trainer = UrduAIModelTrainer()
    stats = trainer.train()
    print("Training stats:", stats)

    # Self-test sample queries
    test_queries = [
        "دھان کی فصل کے لیے کیا احتیاطی تدابیر ہیں؟",
        "پھپھوندی کی بیماری سے کیسے بچیں؟",
        "کھاد کا صحیح شیڈول کیا ہے؟",
        "پتے پیلے کیوں پڑ رہے ہیں؟",
        "السلام علیکم آپ کون ہیں؟"
    ]

    print("\n--- Model Verification & Evaluation ---")
    for q in test_queries:
        intent, conf = trainer.predict_intent(q)
        top_ans = trainer.retrieve_answer(q, top_k=1)[0]
        print(f"\nQuery: {q}")
        print(f"-> Predicted Intent: {intent} (Confidence: {conf:.2f}, Cosine Score: {top_ans['score']:.2f})")
        print(f"-> Answer snippet: {top_ans['response'][:100]}...")

    export_file = os.path.join(os.path.dirname(__file__), "urdu_ai_model.json")
    trainer.export_model(export_file)
