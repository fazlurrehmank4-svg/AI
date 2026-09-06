"""
Practical 09: Multilingual Domain-Specific Agricultural & Weather NLP Chatbot (CropGuard AI Assistant)
Supports English, Hindi (हिंदी / Hinglish), and Urdu (اردو) with deep weather knowledge, dynamic agronomic reasoning,
crop disease prevention, and forecast hazard analysis (Zero external LLMs).
"""

import os
import re
import json
import math
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Import Reasoning & Self Learning Engines
import sys
_AI_DIR = os.path.dirname(os.path.abspath(__file__))
if _AI_DIR not in sys.path:
    sys.path.insert(0, _AI_DIR)

try:
    from reasoning_engine import AgriculturalReasoningEngine
except ImportError:
    try:
        from Backend.ai.reasoning_engine import AgriculturalReasoningEngine
    except ImportError:
        from Practical_05_Reasoning.reasoning_engine import AgriculturalReasoningEngine

try:
    from self_learning_engine import SelfLearningEngine
except ImportError:
    try:
        from Backend.ai.self_learning_engine import SelfLearningEngine
    except ImportError:
        from Practical_09_NLP_App.self_learning_engine import SelfLearningEngine

# Comprehensive Multilingual Crop Name Mapping (English, Hindi, Urdu)
CROP_NAME_MAP = {
    # English
    "rice": "Rice", "paddy": "Rice",
    "wheat": "Wheat",
    "maize": "Maize", "corn": "Maize",
    "tomato": "Tomato",
    "potato": "Potato",
    "pepper": "Pepper", "capsicum": "Pepper", "chilli": "Pepper", "chili": "Pepper",
    "apple": "Apple",
    "mango": "Mango",
    "banana": "Banana",
    "grapes": "Grapes", "grape": "Grapes",
    "strawberry": "Strawberry",
    "cherry": "Cherry",
    "peach": "Peach",
    "pomegranate": "Pomegranate",
    "watermelon": "Watermelon",
    "muskmelon": "Muskmelon", "cantaloupe": "Muskmelon",
    "orange": "Orange", "citrus": "Orange",
    "papaya": "Papaya",
    "coconut": "Coconut",
    "cotton": "Cotton",
    "sugarcane": "Sugarcane",
    "chickpea": "Chickpea", "gram": "Chickpea",
    "kidneybeans": "Kidneybeans", "rajma": "Kidneybeans",
    "pigeonpeas": "Pigeonpeas", "arhar": "Pigeonpeas", "tur": "Pigeonpeas", "toor": "Pigeonpeas",
    "mothbeans": "Mothbeans", "moth": "Mothbeans",
    "mungbean": "Mungbean", "moong": "Mungbean",
    "blackgram": "Blackgram", "urad": "Blackgram",
    "lentil": "Lentil", "masoor": "Lentil",
    "jute": "Jute",
    "coffee": "Coffee",

    # Hindi (Devanagari)
    "चावल": "Rice", "धान": "Rice",
    "गेहूं": "Wheat", "गेंहू": "Wheat",
    "मक्का": "Maize", "भुट्टा": "Maize",
    "टमाटर": "Tomato",
    "आलू": "Potato",
    "मिर्च": "Pepper", "शिमला मिर्च": "Pepper",
    "सेब": "Apple",
    "आम": "Mango",
    "केला": "Banana",
    "अंगूर": "Grapes",
    "स्ट्रॉबेरी": "Strawberry",
    "चेरी": "Cherry",
    "आड़ू": "Peach",
    "अनार": "Pomegranate",
    "तरबूज": "Watermelon",
    "खरबूजा": "Muskmelon",
    "संतरा": "Orange", "नारंगी": "Orange",
    "पपीता": "Papaya",
    "नारियल": "Coconut",
    "कपास": "Cotton", "रूई": "Cotton",
    "गन्ना": "Sugarcane", "ईख": "Sugarcane",
    "चना": "Chickpea",
    "राजमा": "Kidneybeans",
    "अरहर": "Pigeonpeas", "तुअर": "Pigeonpeas",
    "मोठ": "Mothbeans",
    "मूंग": "Mungbean",
    "उड़द": "Blackgram",
    "मसूर": "Lentil",
    "जूट": "Jute", "पटसन": "Jute",
    "कॉफी": "Coffee",

    # Urdu (Arabic Script)
    "چاول": "Rice", "دھان": "Rice",
    "گندم": "Wheat", "گیہوں": "Wheat",
    "مکئی": "Maize", "بھٹہ": "Maize",
    "ٹماٹر": "Tomato",
    "آلو": "Potato",
    "مرچ": "Pepper", "شملہ مرچ": "Pepper",
    "سیب": "Apple",
    "آم": "Mango",
    "کیلا": "Banana",
    "انگور": "Grapes",
    "اسٹرابیری": "Strawberry", "سٹرابیری": "Strawberry",
    "چیری": "Cherry",
    "آڑو": "Peach",
    "انار": "Pomegranate",
    "تربوز": "Watermelon",
    "خربوزہ": "Muskmelon",
    "مالٹا": "Orange", "سنترا": "Orange", "کینوں": "Orange",
    "پپیتا": "Papaya",
    "ناریل": "Coconut",
    "کپاس": "Cotton", "روئی": "Cotton",
    "گنا": "Sugarcane",
    "چنا": "Chickpea",
    "راجما": "Kidneybeans", "لال لوبیا": "Kidneybeans",
    "ارہر": "Pigeonpeas", "تور": "Pigeonpeas",
    "مونٹھ": "Mothbeans",
    "مونگ": "Mungbean",
    "ماش": "Blackgram", "اڑد": "Blackgram",
    "مسور": "Lentil",
    "پٹسن": "Jute",
    "کافی": "Coffee"
}

# Romanized Keywords Map (Hinglish & Roman Urdu)
ROMANIZED_CROP_KEYWORDS = {
    "chawal": "Rice", "dhan": "Rice", "gehun": "Wheat", "gehu": "Wheat", "gandum": "Wheat",
    "makka": "Maize", "bhutta": "Maize", "makai": "Maize", "tamatar": "Tomato", "aalu": "Potato",
    "aloo": "Potato", "mirch": "Pepper", "seb": "Apple", "aam": "Mango",
    "kela": "Banana", "angoor": "Grapes", "anar": "Pomegranate",
    "tarbooj": "Watermelon", "tarbooz": "Watermelon", "kharbooja": "Muskmelon", "kharbooza": "Muskmelon",
    "santra": "Orange", "malta": "Orange", "kinnow": "Orange", "papita": "Papaya", "nariyal": "Coconut",
    "kapas": "Cotton", "ganna": "Sugarcane", "chana": "Chickpea", "rajma": "Kidneybeans",
    "arhar": "Pigeonpeas", "moong": "Mungbean", "urad": "Blackgram", "maash": "Blackgram", "masoor": "Lentil"
}

# Multilingual Display Names
CROP_HINDI_NAMES = {
    "Rice": "धान / चावल (Rice)", "Wheat": "गेहूं (Wheat)", "Maize": "मक्का (Maize)",
    "Tomato": "टमाटर (Tomato)", "Potato": "आलू (Potato)", "Pepper": "मिर्च / शिमला मिर्च (Pepper)",
    "Apple": "सेब (Apple)", "Mango": "आम (Mango)", "Banana": "केला (Banana)",
    "Grapes": "अंगूर (Grapes)", "Strawberry": "स्ट्रॉबेरी (Strawberry)", "Cherry": "चेरी (Cherry)",
    "Peach": "आड़ू (Peach)", "Pomegranate": "अनार (Pomegranate)", "Watermelon": "तरबूज (Watermelon)",
    "Muskmelon": "खरबूजा (Muskmelon)", "Orange": "संतरा (Orange)", "Papaya": "पपीता (Papaya)",
    "Coconut": "नारियल (Coconut)", "Cotton": "कपास (Cotton)", "Sugarcane": "गन्ना (Sugarcane)",
    "Chickpea": "चना (Chickpea)", "Kidneybeans": "राजमा (Kidneybeans)", "Pigeonpeas": "अरहर / तुअर (Pigeonpeas)",
    "Mothbeans": "मोठ (Mothbeans)", "Mungbean": "मूंग (Mungbean)", "Blackgram": "उड़द (Blackgram)",
    "Lentil": "मसूर दाल (Lentil)", "Jute": "जूट / पटसन (Jute)", "Coffee": "कॉफी (Coffee)"
}

CROP_URDU_NAMES = {
    "Rice": "دھان / چاول (Rice)", "Wheat": "گندم (Wheat)", "Maize": "مکئی (Maize)",
    "Tomato": "ٹماٹر (Tomato)", "Potato": "آلو (Potato)", "Pepper": "مرچ / شملہ مرچ (Pepper)",
    "Apple": "سیب (Apple)", "Mango": "آم (Mango)", "Banana": "کیلا (Banana)",
    "Grapes": "انگور (Grapes)", "Strawberry": "اسٹرابیری (Strawberry)", "Cherry": "چیری (Cherry)",
    "Peach": "آڑو (Peach)", "Pomegranate": "انار (Pomegranate)", "Watermelon": "تربوز (Watermelon)",
    "Muskmelon": "خربوزہ (Muskmelon)", "Orange": "مالٹا / کینوں (Orange)", "Papaya": "پپیتا (Papaya)",
    "Coconut": "ناریل (Coconut)", "Cotton": "کپاس (Cotton)", "Sugarcane": "گنا (Sugarcane)",
    "Chickpea": "چنا (Chickpea)", "Kidneybeans": "لال لوبیا / راجما (Kidneybeans)", "Pigeonpeas": "ارہر / تور دال (Pigeonpeas)",
    "Mothbeans": "مونٹھ (Mothbeans)", "Mungbean": "مونگ (Mungbean)", "Blackgram": "ماش کی دال (Blackgram)",
    "Lentil": "مسور دال (Lentil)", "Jute": "پٹسن (Jute)", "Coffee": "کافی (Coffee)"
}

# Crop Specific Precautions in Hindi
CROP_PRECAUTIONS_HI = {
    "Rice": [
        "खेत में 2-5 सेमी नियंत्रित जल स्तर बनाए रखें; तेज बारिश के समय जल निकासी करें।",
        "बादल छाए रहने और अधिक नमी के समय अतिरिक्त यूरिया (नाइट्रोजन) का उपयोग न करें।",
        "तना छेदक और झुलसा (Blast) रोग के शुरुआती लक्षणों के लिए नियमित निरीक्षण करें।",
        "संक्रमण की स्थिति में ट्राइकोडर्मा या अनुशंसित जैव कवकनाशी का छिड़काव करें।"
    ],
    "Wheat": [
        "दाना भरते समय 30°C से अधिक तापमान होने पर हल्की सिंचाई करें ताकि गर्मी का तनाव कम हो।",
        "पीला रतुआ (Yellow Rust) के लक्षणों के लिए पत्तियों के नीचे नारंगी-पीले धब्बों की जांच करें।",
        "खेत में जलभराव न होने दें, क्योंकि गेहूं की जड़ें अत्यधिक पानी से सड़ने लगती हैं।",
        "बालियां निकलते समय पोटाश और जिंक का संतुलित छिड़काव करें।"
    ],
    "Maize": [
        "जलभराव से मक्के की फसल तेजी से खराब होती है, अतः खेत में जल निकासी की नालियां तैयार रखें।",
        "फॉल आर्मीवर्म (कीड़ा) से बचाव के लिए पत्तियों के पोरों की नियमित जांच करें।",
        "घुटने की ऊंचाई और फूल आने के समय पर्याप्त नमी बनाए रखें।",
        "नीम तेल (1500 PPM) या अनुशंसित जैव कीटनाशक का शुरुआती छिड़काव करें।"
    ],
    "Tomato": [
        "पत्तियों को गीला होने से बचाने के लिए ड्रिप सिंचाई (टपक सिंचाई) का उपयोग करें।",
        "अगेती व पछेती झुलसा (Blight) से बचाव हेतु पौधों के बीच हवा का प्रवाह बनाए रखें।",
        "पौधों को सहारा (Staking) दें ताकि फल और पत्तियां जमीन की नमी के संपर्क में न आएं।",
        "अधिक नमी होने पर कॉपर ऑक्सीक्लोराइड या मैंकोजेब का सुरक्षात्मक छिड़काव करें।"
    ],
    "Potato": [
        "आलू की मेड़ों पर मिट्टी चढ़ाएं ताकि कंद धूप और फफूंद के सीधे संपर्क में न आएं।",
        "मौसम में कोहरा और 80% से अधिक नमी होने पर लेट ब्लाइट (पछेती झुलसा) का छिड़काव करें।",
        "खुदाई से 10-12 दिन पहले सिंचाई पूरी तरह बंद कर दें ताकि छिलका मजबूत हो सके।",
        "जलभराव से कंद सड़न रोग होता है, अतः पानी तुरंत निकालें।"
    ],
    "Pepper": [
        "पत्ती मरोड़ रोग (Leaf Curl Virus) फैलाने वाले थ्रिप्स और सफेद मक्खी पर नियंत्रण रखें।",
        "अत्यधिक नमी और तापमान के उतार-चढ़ाव से फूल झड़ने की समस्या होती है, संतुलित सिंचाई करें।",
        "जल निकासी का विशेष ध्यान रखें, मिर्च की जड़ें अधिक पानी बर्दाश्त नहीं करतीं।",
        "जैविक कीटनाशक जैसे नीम का काढ़ा या इमिडाक्लोप्रिड का उचित छिड़काव करें।"
    ],
    "Apple": [
        "सेब स्कैब (Scab) और पाउडरी मिल्ड्यू से बचाव हेतु प्रूनिंग (छंटाई) करके धूप और हवा का संचार बढ़ाएं।",
        "फूल आने के समय और फल बनने के समय जल की कमी न होने दें।",
        "पतझड़ के समय गिरी हुई संक्रमित पत्तियों को बाग से हटाकर नष्ट करें।",
        "सर्दियों में बोर्डो मिश्रण या कॉपर फंगीसाइड का सुरक्षात्मक लेप लगाएं।"
    ],
    "Mango": [
        "बौर (फूल) आते समय और फल सेट होते समय हॉपर कीट और पाउडरी मिल्ड्यू से बचाव करें।",
        "बौर खिलने के दौरान भारी सिंचाई न करें, इससे फूल झड़ सकते हैं।",
        "एंथ्रेक्नोज (काले धब्बे) रोग से बचाव के लिए कॉपर फफूंदनाशक का छिड़काव करें।",
        "पेड़ के मुख्य तने पर गोंद रिसाव (Gummosis) होने पर बोर्डो पेस्ट लगाएं।"
    ],
    "Banana": [
        "पनामा विल्ट और सिगाटोका लीफ स्पॉट रोग से बचाव के लिए उचित जल निकासी रखें।",
        "तेज आंधी-तूफान से पौधों को गिरने से बचाने के लिए बांस का सहारा (Propping) दें।",
        "सूखी व रोगग्रस्त पत्तियों को समय-समय पर काटकर बाग से बाहर करें।",
        "पोटाश और जैविक खाद का नियमित उपयोग फल के वजन और गुणवत्ता को बढ़ाता है।"
    ],
    "Cotton": [
        "गुलाबी सुंडी (Pink Bollworm) और सफेद मक्खी से बचाव के लिए फेरोमोन ट्रैप लगाएं।",
        "खेत में पानी जमा न होने दें, क्योंकि कपास में जड़ सड़न रोग तेजी से फैलता है।",
        "फूल और टिंडे बनते समय पोटाश और बोरॉन का पर्णीय छिड़काव करें।",
        "नाइट्रोजन की अत्यधिक मात्रा न दें, इससे वानस्पतिक वृद्धि ज्यादा और फल कम होते हैं।"
    ],
    "Sugarcane": [
        "लाल सड़न (Red Rot) और तना छेदक कीट के लक्षण दिखने पर तुरंत रोगग्रस्त पौधे उखाड़ें।",
        "गर्मियों में 8-10 दिन के अंतराल पर सिंचाई करें और मेड़ों पर सूखी पत्तियों की मल्चिंग करें।",
        "भारी बारिश से पहले जल निकासी नाली साफ करें ताकि गन्ने की जड़ें सुरक्षित रहें।",
        "मिट्टी चढ़ाएं ताकि तेज हवाओं में गन्ना गिरे नहीं।"
    ]
}

# Crop Specific Precautions in Urdu
CROP_PRECAUTIONS_UR = {
    "Rice": [
        "کھیت میں 2 سے 5 سینٹی میٹر پانی کی سطح برقرار رکھیں؛ تیز بارش کے دوران نکاسی کا انتظام کریں۔",
        "ابر آلود موسم اور زیادہ نمی کے دوران غیر ضروری یوریا (نائٹروجن) کھاد کے استعمال سے گریز کریں۔",
        "تنے کی سنڈی اور بلاسٹ (جھلساؤ) کی بیماری کی باقاعدہ جانچ کریں۔",
        "حفاظتی طور پر ٹرائیکوڈرما یا تجویز کردہ فنگس کش اسپرے استعمال کریں۔"
    ],
    "Wheat": [
        "دانہ بنتے وقت درجہ حرارت 30 ڈگری سے زیادہ ہو تو ہلکی آبپاشی کریں تاکہ گرمی کا تناؤ کم ہو۔",
        "پیلے رسٹ (Yellow Rust) سے بچاؤ کے لیے پتوں پر پیلے اور نارنجی دھبوں کا معائنہ کریں۔",
        "کھیت میں پانی کھڑا نہ ہونے دیں کیونکہ اضافی نمی سے گندم کی جڑیں گلنے لگتی ہیں۔",
        "سٹہ نکلتے وقت پوٹاش اور زنک کا متوازن اسپرے کریں۔"
    ],
    "Maize": [
        "مکئی کی فصل میں پانی کا کھڑا ہونا نقصان دہ ہے، لہٰذا پانی کے نکاس کی نالیاں صاف رکھیں۔",
        "فال آرمی ورم (سنڈی) سے بچاؤ کے لیے کونپلوں کا باقاعدگی سے معائنہ کریں۔",
        "چھلی بننے کے دوران کھیت میں مناسب وتر اور نمی برقرار رکھیں۔",
        "شروعات میں نیم کا تیل یا تجویز کردہ کیڑے مار دوا کا اسپرے کریں۔"
    ],
    "Tomato": [
        "پتوں کو خشک رکھنے کے لیے ڈرپ اریگیشن (قطرہ قطرہ آبپاشی) کا طریقہ اپنائیں۔",
        "اگیتی اور پچھیتی جھلساؤ بیماری سے بچاؤ کے لیے پودوں کے درمیان مناسب فاصلہ رکھیں۔",
        "پودوں کو بانس یا رسی کا سہارا دیں تاکہ پھل زمین کی نمی سے خراب نہ ہوں۔",
        "زیادہ نمی کی صورت میں کاپر آکسی کلورائیڈ کا حفاظتی اسپرے کریں۔"
    ],
    "Potato": [
        "آلو کی پٹریوں پر مٹی چڑھائیں تاکہ آلو دھوپ اور فنگس سے محفوظ رہیں۔",
        "دھند اور زیادہ نمی میں پچھیتے جھلساؤ (Late Blight) سے بچاؤ کا اسپرے بروقت کریں۔",
        "کٹائی سے 10 تا 12 دن پہلے پانی دینا بند کر دیں تاکہ چھلکا پکا ہو جائے۔",
        "پانی کے کھڑے ہونے سے آلو گل جاتے ہیں، لہٰذا فوری نکاسی کریں۔"
    ],
    "Pepper": [
        "پتا مروڑ وائرس پھیلانے والی سفید مکھی اور تھرپس کا بروقت تدارک کریں۔",
        "ضرورت سے زیادہ پانی یا درجہ حرارت کے اتار چڑھاؤ سے پھول گر سکتے ہیں، معتدل پانی دیں۔",
        "مرچ کی جڑیں زیادہ پانی برداشت نہیں کرتیں، نکاس کا خاص دھیان رکھیں۔",
        "نیم کا کاڑھا یا مناسب کیڑے مار دوا کا اسپرے کریں۔"
    ],
    "Apple": [
        "سیب کے اسکیب اور پھپھوندی سے بچاؤ کے لیے شاخ تراشی کریں تاکہ دھوپ اور ہوا کا گزر ہو۔",
        "پھول اور پھل بننے کے مرحلے پر پانی کی کمی نہ ہونے دیں۔",
        "خزاں میں متاثرہ گرے ہوئے پتوں کو باغ سے باہر نکال کر تلف کریں۔",
        "سردیوں میں بورڈو مکسچر یا کاپر فنگسائیڈ کا حفاظتی لیپ کریں۔"
    ],
    "Mango": [
        "بور (پھول) نکلتے اور پھل بنتے وقت ہاپر کیڑے اور سفوفی پھپھوندی سے تحفظ کریں۔",
        "بور کھلنے کے دوران زیادہ پانی نہ دیں ورنہ پھول گر سکتے ہیں۔",
        "کالے دھبوں (اینتھراکنوز) کی بیماری سے بچاؤ کے لیے کاپر فنگس کش دوا اسپرے کریں۔",
        "تنے سے گوند بہنے پر بورڈو پیسٹ کا لیپ کریں۔"
    ],
    "Banana": [
        "پناما ولٹ اور سگاٹوکا بیماری سے بچاؤ کے لیے بہترین نکاسی کا نظام رکھیں۔",
        "تیز آندھی اور طوفان سے گرنے سے بچانے کے لیے پودوں کو بانس کا سہارا دیں۔",
        "سوکھے اور بیمار پتوں کو کاٹ کر باغ سے دور کریں۔",
        "پوٹاش اور گوبر کی کھاد کا باقاعدہ استعمال پھل کے وزن کو بڑھاتا ہے۔"
    ],
    "Cotton": [
        "گلابی سنڈی اور سفید مکھی سے بچاؤ کے لیے فیرومون ٹریپس لگائیں۔",
        "کھیت میں پانی کھڑا نہ ہونے دیں ورنہ جڑ گلنے کا روگ پھیلتا ہے۔",
        "پھول اور ٹینڈے بنتے وقت پوٹاش اور بوران کا اسپرے کریں۔",
        "نائٹروجن کی زیادہ مقدار نہ دیں تاکہ پودا صرف پتے نہ بڑھائے۔"
    ],
    "Sugarcane": [
        "رتہ روگ (Red Rot) اور تنے کے کیڑے کی علامات ظاہر ہونے پر متاثرہ پودے فوری تلف کریں۔",
        "گرمیوں میں 8 تا 10 دن کے وقفے سے پانی دیں اور سوکھے پتوں کی ملچنگ کریں۔",
        "بارشوں سے قبل نالیاں صاف رکھیں تاکہ پانی گنے کی جڑوں میں نہ رکے۔",
        "مٹی چڑھائیں تاکہ تیز ہواؤں میں گنا گرنے سے محفوظ رہے۔"
    ]
}

# Crop Specific Diseases in Hindi
CROP_DISEASES_HI = {
    "Rice": [
        {"name": "जीवाणु झुलसा (Bacterial Leaf Blight)", "symptoms": "पत्तियों के किनारों से सूखना और पीली-सफेद धारियां बनना।", "precautions": "अत्यधिक यूरिया न डालें, खेत से पानी निकालें और कॉपर फफूंदनाशक का छिड़काव करें।"},
        {"name": "धान का ब्लास्ट रोग (Rice Blast)", "symptoms": "पत्तियों पर आंख या नाव के आकार के भूरे-सफेद धब्बे।", "precautions": "पौधों में पर्याप्त दूरी रखें और ट्राइसायक्लाजोल या जैव कवकनाशी का छिड़काव करें।"}
    ],
    "Wheat": [
        {"name": "पीला रतुआ (Yellow Rust)", "symptoms": "पत्तियों पर पीले रंग की धारियों के रूप में पाउडर जैसा चूर्ण।", "precautions": "तापमान बढ़ने पर प्रोपिकोनाजोल (टिल्ट) का 0.1% छिड़काव करें।"},
        {"name": "करनाल बंट (Karnal Bunt)", "symptoms": "दानों का काला चूर्ण में बदलना और सड़ी मछली जैसी गंध आना।", "precautions": "प्रमाणित बीजों का उपयोग करें और फूल आते समय हल्की सिंचाई रखें।"}
    ],
    "Maize": [
        {"name": "फॉल आर्मीवर्म (Fall Armyworm)", "symptoms": "पत्तियों में बड़े छेद और भुट्टे के पोरों में कीड़े का मल दिखना।", "precautions": "नीम तेल या एमामेक्टिन बेंजोएट का तने के बीच में छिड़काव करें।"},
        {"name": "लीफ ब्लाइट (Turcicum Leaf Blight)", "symptoms": "पत्तियों पर बड़े नाव के आकार के भूरे धब्बे।", "precautions": "मैंकोजेब या एजोक्सीस्ट्रोबिन का सुरक्षात्मक छिड़काव करें।"}
    ],
    "Tomato": [
        {"name": "अगेती व पछेती झुलसा (Early & Late Blight)", "symptoms": "पत्तियों और फलों पर गहरे भूरे-काले छल्लेदार धब्बे।", "precautions": "ड्रिप सिंचाई अपनाएं और कॉपर ऑक्सीक्लोराइड या सिमोक्सानिल का छिड़काव करें।"},
        {"name": "पत्ती मरोड़ रोग (Leaf Curl Virus)", "symptoms": "पत्तियां ऊपर की ओर मुड़ना, सिकुड़ना और पौधे का बौना रह जाना।", "precautions": "सफेद मक्खी पर नियंत्रण हेतु पीला चिपचिपा ट्रैप (Yellow Sticky Trap) लगाएं।"}
    ],
    "Potato": [
        {"name": "पछेती झुलसा (Late Blight)", "symptoms": "पत्तियों के सिरों पर काले-भूरे पानीदार धब्बे जो तेजी से फैलते हैं।", "precautions": "कोहरा और अधिक नमी होते ही मैंकोजेब या रेडोमिल का तुरंत छिड़काव करें।"},
        {"name": "काली रूसी (Black Scurf)", "symptoms": "आलू के कंद पर काले रंग की पपड़ी जैसी परत जमना।", "precautions": "बीज आलू को ट्राइकोडर्मा या कार्बेंडाजिम से उपचारित करके ही बोएं।"}
    ],
    "Pepper": [
        {"name": "मिर्च का मरोड़िया रोग (Chilli Leaf Curl)", "symptoms": "पत्तियां नाव की तरह मुड़ जाना और आकार छोटा हो जाना।", "precautions": "थ्रिप्स व माइट्स कीटों के लिए नीम तेल और अनुशंसित कीटनाशक का छिड़काव करें।"},
        {"name": "एंथ्रेक्नोज / फल सड़न (Anthracnose)", "symptoms": "पके फलों पर धंसे हुए गोल काले धब्बे।", "precautions": "कॉपर फफूंदनाशक का छिड़काव करें और खेत में जलभराव न होने दें।"}
    ]
}

# Crop Specific Diseases in Urdu
CROP_DISEASES_UR = {
    "Rice": [
        {"name": "بیکٹیریل لیف بلائٹ (Bacterial Leaf Blight)", "symptoms": "پتوں کے کناروں کا سوکھنا اور پیلی سفید لکیریں بننا۔", "precautions": "اضافی نائٹروجن سے پرہیز کریں، پانی کی نکاسی کریں اور کاپر فنگس کش دوا اسپرے کریں۔"},
        {"name": "دھان کا بلاسٹ روگ (Rice Blast)", "symptoms": "پتوں پر آنکھ یا کشتی کی شکل کے سرمئی و بھورے دھبے۔", "precautions": "پودوں میں مناسب فاصلہ رکھیں اور ٹرائی سائیکلازول یا مناسب اسپرے کریں۔"}
    ],
    "Wheat": [
        {"name": "پیلا رسٹ / کنگی (Yellow Rust)", "symptoms": "پتوں پر پیلے رنگ کی دھاریاں اور پاؤڈر جیسا مادہ۔", "precautions": "موسم بدلتے ہی پروپیکونازول (Tilt) کا 0.1% اسپرے کریں۔"},
        {"name": "کرنال بنٹ (Karnal Bunt)", "symptoms": "دانوں کا سیاہ سفوف میں تبدیل ہونا اور بدبو آنا۔", "precautions": "صاف و تصدیق شدہ بیج استعمال کریں اور پھول کے وقت ہلکا پانی دیں۔"}
    ],
    "Maize": [
        {"name": "فال آرمی ورم سنڈی (Fall Armyworm)", "symptoms": "پتوں میں بڑے سوراخ اور کونپلوں میں کیڑے کی موجودگی۔", "precautions": "نیم کا تیل یا ایما مائل بینزویٹ کا کونپلوں کے درمیان اسپرے کریں۔"},
        {"name": "لیف بلائٹ جھلساؤ (Turcicum Leaf Blight)", "symptoms": "پتوں پر کشتی نما بڑے بھورے دھبے۔", "precautions": "مینکوزیب یا ایزوکسسٹروبن کا اسپرے کریں۔"}
    ],
    "Tomato": [
        {"name": "جھلساؤ کی بیماری (Early & Late Blight)", "symptoms": "پتوں اور پھل پر سیاہ بھورے گول دھبے۔", "precautions": "پتوں کو خشک رکھیں اور کاپر آکسی کلورائیڈ کا اسپرے کریں۔"},
        {"name": "پتا مروڑ وائرس (Leaf Curl Virus)", "symptoms": "پتے اوپر کی جانب مڑنا اور پودے کا بڑھنا رک جانا۔", "precautions": "سفید مکھی کے خاتمے کے لیے پیلے اسٹیکی ٹریپس اور کیڑے مار اسپرے کریں۔"}
    ],
    "Potato": [
        {"name": "پچھیتا جھلساؤ (Late Blight)", "symptoms": "پتوں کے کونوں پر سیاہ نمدار دھبے جو تیزی سے پھیلتے ہیں۔", "precautions": "دھند اور سردی کے دوران مینکوزیب یا ریڈومل کا حفاظتی اسپرے کریں۔"},
        {"name": "کالی پپڑی (Black Scurf)", "symptoms": "آلو کے چھلکے پر سیاہ رنگ کی سخت پرت جم جانا۔", "precautions": "بیج کو پھپھوند کش دوا سے زہر آلود کر کے کاشت کریں۔"}
    ],
    "Pepper": [
        {"name": "مرچ کا چڑمڑ روگ (Leaf Curl)", "symptoms": "پتوں کا سکڑنا اور اوپر کی طرف مڑ جانا۔", "precautions": "تھرپس اور سفید مکھی کے لیے نیم کا تیل اور تجویز کردہ اسپرے کریں۔"},
        {"name": "اینتھراکنوز / پھل سڑن (Anthracnose)", "symptoms": "پکے ہوئے پھلوں پر سیاہ دھبے اور پھل کا گلنا۔", "precautions": "کاپر فنگس کش دوا اسپرے کریں اور نکاسی بہتر بنائیں۔"}
    ]
}

# Crop Fertilizer Advice in Hindi, Urdu, English
CROP_FERTILIZER_GUIDE = {
    "Rice": {
        "en": "🌾 **Rice Fertilizer Schedule:**\n• **Basal (Transplanting):** 100% DAP (Phosphorus) + 50% Potash + 25% Urea.\n• **Tillering Stage (20-25 days):** Top-dress 50% Nitrogen (Urea) with Zinc Sulfate (25 kg/ha).\n• **Panicle Initiation (40-45 days):** Apply remaining 25% Urea + 50% Potash for heavy grain filling.",
        "hi": "🌾 **धान (चावल) के लिए खाद प्रबंधन:**\n• **रोपाई के समय (बेसल):** पूरी डीएपी (फास्फोरस) + 50% पोटाश + 25% यूरिया डालें।\n• **कल्ले फूटते समय (20-25 दिन):** 50% यूरिया के साथ 25 किग्रा जिंक सल्फेट डालें।\n• **बाली निकलते समय (40-45 दिन):** शेष 25% यूरिया और 50% पोटाश डालें ताकि दाना वजनदार और चमकदार बने।",
        "ur": "🌾 **دھان (چاول) کے لیے کھاد کا شیڈول:**\n• **پنیری لگاتے وقت:** تمام ڈی اے پی + 50% پوٹاش + 25% یوریا دیں۔\n• **شاخیں نکلتے وقت (20-25 دن):** 50% یوریا کے ساتھ زنک سلفیٹ دیں۔\n• **گوپ / سٹہ بنتے وقت (40-45 دن):** بقیہ 25% یوریا اور 50% پوٹاش دیں تاکہ دانے وزنی بنیں۔"
    },
    "Wheat": {
        "en": "🌾 **Wheat Fertilizer Schedule:**\n• **Sowing:** Full dose of DAP (50-60 kg/acre) + Potash (20 kg/acre) + 1/3rd Urea.\n• **1st Irrigation (CRI Stage / 21 days):** Top-dress 1/3rd Urea with Zinc Sulfate.\n• **2nd Irrigation (Jointing / 45 days):** Apply remaining 1/3rd Urea.",
        "hi": "🌾 **गेहूं की फसल के लिए खाद प्रबंधन:**\n• **बुवाई के समय:** पूरी डीएपी (1 बोरी/एकड़) + पोटाश (20-25 किग्रा) + 1/3 यूरिया डालें।\n• **पहली सिंचाई (21 दिन / सीआरआई अवस्था):** 1/3 यूरिया के साथ जिंक सल्फेट डालें।\n• **दूसरी सिंचाई (40-45 दिन / कल्ले निकलते समय):** शेष 1/3 यूरिया का छिड़काव करें।",
        "ur": "🌾 **گندم کی فصل کے لیے کھاد کا شیڈول:**\n• **بجائی کے وقت:** پوری ڈی اے پی (1 بوری فی ایکڑ) + پوٹاش + 1/3 یوریا دیں۔\n• **پہلے پانی پر (21 دن / کور کا پانی):** 1/3 یوریا کے ساتھ زنک سلفیٹ دیں۔\n• **دوسرے پانی پر (40-45 دن / گبھے کی حالت):** بقیہ 1/3 یوریا ڈالیں۔"
    },
    "General": {
        "en": "🌱 **General Balanced Fertilizer Rules:**\n1) Apply full Phosphorus (DAP) & Potash as basal dose at sowing.\n2) Split Nitrogen (Urea) into 2-3 top-dressings during active growth stages.\n3) Avoid applying urea right before rain or in standing flood water.\n4) Supplement with micronutrients (Zinc, Boron) for strong root and grain health.",
        "hi": "🌱 **संतुलित खाद प्रबंधन के मुख्य नियम:**\n1) बुवाई के समय डीएपी (फास्फोरस) और पोटाश की पूरी मात्रा बेसल डोज के रूप में दें।\n2) यूरिया (नाइट्रोजन) को 2-3 किस्तों में बांटकर दें (कल्ले निकलते समय और बढ़वार काल में)।\n3) भारी बारिश से ठीक पहले या खेत में पानी भरा होने पर यूरिया न डालें।\n4) फसल में जिंक और बोरॉन जैसे सूक्ष्म पोषक तत्वों का संतुलित प्रयोग करें।",
        "ur": "🌱 **متوازن کھاد کے بنیادی اصول:**\n1) بجائی کے وقت ڈی اے پی (فاسفورس) اور پوٹاش کی پوری مقدار بنیادی طور پر دیں۔\n2) یوریا کو 2 سے 3 اقساط میں بانٹ کر دیں تاکہ ضائع نہ ہو۔\n3) بارش سے پہلے یا پانی کھڑا ہونے پر یوریا کھاد نہ ڈالیں۔\n4) زنک اور بوران جیسے مائیکرو نیوٹرینٹس کا متوازن استعمال کریں۔"
    }
}

# Synonyms for Normalization (English, Hindi, Urdu)
SYNONYM_MAP = {
    "warm": "temperature", "hot": "temperature", "cold": "temperature",
    "chilly": "temperature", "heat": "temperature", "garmi": "temperature",
    "sardi": "temperature", "thand": "temperature", "taapman": "temperature",
    "तापमान": "temperature", "गर्मी": "temperature", "सर्दी": "temperature", "ठंड": "temperature",
    "درجہ حرارت": "temperature", "گرمی": "temperature", "سردی": "temperature", "ٹھنڈ": "temperature",

    "moist": "humidity", "moisture": "humidity", "humid": "humidity",
    "damp": "humidity", "nami": "humidity", "umas": "humidity",
    "नमी": "humidity", "आर्द्रता": "humidity", "उमस": "humidity",
    "نمی": "humidity", "حبس": "humidity",

    "rain": "rainfall", "precipitation": "rainfall", "downpour": "rainfall",
    "rains": "rainfall", "barish": "rainfall", "paani": "rainfall", "barsat": "rainfall",
    "बारिश": "rainfall", "वर्षा": "rainfall", "पानी": "rainfall", "बरसात": "rainfall",
    "بارش": "rainfall", "بارشیں": "rainfall", "برسات": "rainfall", "پانی": "rainfall",

    "windy": "wind", "gale": "wind", "storm": "wind", "hawa": "wind", "aandhi": "wind",
    "हवा": "wind", "आंधी": "wind", "तूफान": "wind",
    "ہوا": "wind", "آندھی": "wind", "طوفان": "wind",

    "yellowing": "yellow_leaves", "yellow": "yellow_leaves", "peeli": "yellow_leaves",
    "पीली": "yellow_leaves", "पीला": "yellow_leaves", "पीलापन": "yellow_leaves",
    "پیلے": "yellow_leaves", "پیلا": "yellow_leaves", "پیلاہٹ": "yellow_leaves",

    "fungus": "fungal", "fungi": "fungal", "mold": "fungal", "mildew": "fungal",
    "blight": "fungal", "fafund": "fungal", "झुलसा": "fungal", "फफूंद": "fungal", "फफूंदी": "fungal",
    "پھپھوند": "fungal", "پھپھوندی": "fungal", "فنگس": "fungal", "جھلساؤ": "fungal",

    "remedy": "precaution", "treatment": "precaution", "prevent": "precaution",
    "measure": "precaution", "advice": "precaution", "cure": "precaution",
    "care": "precaution", "safety": "precaution", "savdhani": "precaution",
    "bachav": "precaution", "upchar": "precaution", "upaay": "precaution", "ehtiyat": "precaution",
    "उपाय": "precaution", "सावधानी": "precaution", "सावधानियां": "precaution",
    "बचाव": "precaution", "इलाज": "precaution", "सुरक्षा": "precaution", "रोकथाम": "precaution",
    "احتیاط": "precaution", "تدابیر": "precaution", "بچاؤ": "precaution", "علاج": "precaution", "حفاظت": "precaution",

    "disease": "disease_risk", "risk": "disease_risk", "problem": "disease_risk",
    "khatra": "disease_risk", "bimari": "disease_risk", "rog": "disease_risk",
    "रोग": "disease_risk", "बीमारी": "disease_risk", "खतरा": "disease_risk", "नुकसान": "disease_risk",
    "بیماری": "disease_risk", "خطرہ": "disease_risk", "نقصان": "disease_risk", "روگ": "disease_risk",

    "mausam": "weather", "climate": "weather", "forecast": "weather",
    "मौसम": "weather", "जलवायु": "weather", "पूर्वानुमान": "weather",
    "موسم": "weather", "پیشگوئی": "weather",

    "fertilizer": "fertilizer", "khad": "fertilizer", "urea": "fertilizer",
    "खाद": "fertilizer", "उर्वरक": "fertilizer", "यूरिया": "fertilizer", "डीएपी": "fertilizer",
    "کھاد": "fertilizer", "یوریا": "fertilizer", "ڈی اے پی": "fertilizer",

    "pesticide": "spray", "insecticide": "spray", "fungicide": "spray",
    "कीटनाशक": "spray", "फफूंदनाशक": "spray", "छिड़काव": "spray", "दवा": "spray",
    "کیڑے مار": "spray", "فنگس کش": "spray", "اسپرے": "spray", "دوائی": "spray"
}

# Stopwords (English, Hindi, Urdu)
STOPWORDS = {
    "a", "about", "above", "after", "again", "all", "am", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself",
    "me", "more", "most", "my", "myself", "no", "nor", "not", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same",
    "she", "should", "so", "some", "such", "t", "than", "that", "the", "their", "theirs",
    "them", "themselves", "then", "there", "these", "they", "this", "those", "through",
    "to", "too", "under", "until", "up", "very", "was", "we", "were", "what", "when",
    "where", "which", "while", "who", "whom", "why", "will", "with", "you", "your", "yours",
    "hai", "kya", "kaise", "kare", "karna", "hoga", "mein", "par", "ko", "se", "aur", "hota", "hoti",
    "है", "क्या", "कैसे", "करें", "होगा", "में", "पर", "को", "से", "और", "का", "की", "के", "लिए", "होता", "होती",
    "ہے", "کیا", "کیسے", "کریں", "کرنا", "ہوگا", "میں", "پر", "کو", "سے", "اور", "کا", "کی", "کے", "لیے", "ہوتا", "ہوتی"
}

# Expanded Domain Agricultural Knowledge Corpus for Retrieval
AGRICULTURAL_CORPUS = [
    {
        "topic": "wheat_temperature",
        "crop": "Wheat",
        "query_templates": [
            "what is the best temperature for wheat", "optimal temperature for wheat growing",
            "wheat weather requirements", "gehun ke liye sahi taapman", "गेहूं के लिए अनुकूल तापमान",
            "गेहूं की खेती के लिए सही तापमान क्या है", "گندم کے لیے بہترین درجہ حرارت کیا ہے",
            "گندم کی کاشت کے لیے موزوں درجہ حرارت"
        ],
        "answer_en": "Wheat thrives best in cool to moderate temperatures between 15°C and 25°C. Temperatures exceeding 30°C during the grain-filling stage trigger terminal heat stress, causing shriveled grains and premature leaf drying.",
        "answer_hi": "गेहूं की अच्छी फसल के लिए 15°C से 25°C का ठंडा और सुहावना तापमान सबसे उपयुक्त होता है। दाना भरते समय 30°C से अधिक तापमान होने पर गर्मी का तनाव (Heat Stress) होता है, जिससे दाने सिकुड़ जाते हैं।",
        "answer_ur": "گندم کی اچھی پیداوار کے لیے 15°C سے 25°C کا ٹھنڈا اور معتدل درجہ حرارت بہترین ہے۔ دانہ بننے کے مرحلے پر 30°C سے زیادہ درجہ حرارت گرمی کے تناؤ (Heat Stress) کا سبب بنتا ہے، جس سے دانے سوکھ اور سکڑ جاتے ہیں۔"
    },
    {
        "topic": "rice_conditions",
        "crop": "Rice",
        "query_templates": [
            "what conditions are good for rice", "best temperature and humidity for rice",
            "rice weather requirements", "rainfall requirement for paddy rice",
            "dhan ke liye mausam", "धान के लिए मौसम और पानी की आवश्यकता", "धान की खेती के लिए अनुकूल मौसम",
            "چاول اور دھان کے لیے موزوں موسم کیا ہے", "دھان کی فصل کے لیے درجہ حرارت اور پانی"
        ],
        "answer_en": "Rice requires warm and humid conditions, with optimal temperatures between 22°C and 32°C, relative humidity of 70% to 85%, and high rainfall (150-300 mm). Extreme heat (>38°C) during flowering can cause floret sterility.",
        "answer_hi": "धान की खेती के लिए गर्म और आर्द्र (humid) मौसम चाहिए। इसके लिए 22°C से 32°C तापमान, 70% से 85% नमी और 150-300 मिमी पानी की आवश्यकता होती है। फूल आते समय 38°C से ज्यादा तापमान से पैदावार घटती है।",
        "answer_ur": "چاول (دھان) کی کاشت کے لیے گرم اور مرطوب موسم درکار ہوتا ہے۔ اس کے لیے 22°C تا 32°C درجہ حرارت، 70% سے 85% ہوا میں نمی اور 150 تا 300 ملی میٹر پانی ضروری ہے۔ پھول آنے پر 38°C سے زیادہ گرمی پیداوار کم کر دیتی ہے۔"
    },
    {
        "topic": "crop_disease_risk_general",
        "crop": "General",
        "query_templates": [
            "why is my crop at risk", "why do crops get disease", "crop health risk causes",
            "fasal ko rog kyu lagta hai", "fasal ko bimari ka khatra kyu hai",
            "फसल को रोग का खतरा क्यों है", "फसल में रोग क्यों लगते हैं", "फसल खतरे में क्यों आती है",
            "रोग का खतरा क्यों है", "मेरी फसल को क्या बीमारी हो सकती है",
            "فصل کو بیماری یا خطرہ کیوں ہوتا ہے", "فصل میں بیماریاں کیوں لگتی ہیں", "فصل کو بیماری کا خطرہ کیوں ہے"
        ],
        "answer_en": "Crops face disease and health risks primarily due to: 1) High atmospheric humidity (>80%) combined with prolonged leaf wetness triggering fungal pathogens; 2) Field waterlogging choking roots of oxygen; 3) Heat or drought stress weakening plant immunity; and 4) Nutrient imbalances (e.g. excessive nitrogen or micronutrient deficiency). Protective action: Ensure proper field drainage, optimize plant spacing, and apply preventive bio-fungicides.",
        "answer_hi": "फसल में रोग और स्वास्थ्य जोखिम के 4 प्रमुख वैज्ञानिक कारण होते हैं:\n1) **हवा में अत्यधिक नमी (>80%):** पत्तियों पर लगातार ओस या पानी रहने से फफूंद (Fungus) और झुलसा रोग तेजी से पनपते हैं।\n2) **जलभराव (Waterlogging):** खेत में पानी भरने से जड़ों को ऑक्सीजन नहीं मिलती और जड़ सड़न रोग होता है।\n3) **तापमान का उतार-चढ़ाव:** अत्यधिक गर्मी या ठंड से पौधों की रोग प्रतिरोधक क्षमता कमजोर होती है।\n4) **असंतुलित खाद:** अधिक यूरिया (नाइट्रोजन) देने से कीट व बीमारियां ज्यादा आकर्षित होती हैं।\n\n**उपाय:** खेत में जल निकासी नालियां साफ रखें, पौधों के बीच हवा का प्रवाह बनाएं और जैविक फफूंदनाशक (ट्राइकोडर्मा/नीम तेल) का समय पर छिड़काव करें।",
        "answer_ur": "فصل کو بیماری اور خطرہ لاحق ہونے کی 4 بڑی وجوہات ہیں:\n1) **ہوا میں زیادہ نمی (>80%):** پتوں پر دیر تک پانی یا اوس رہنے سے فنگس (پھپھوندی) تیزی سے پھیلتی ہے۔\n2) **پانی کا کھڑا ہونا (Waterlogging):** کھیت میں پانی رکنے سے جڑوں کو آکسیجن نہیں ملتی اور جڑیں گلنے لگتی ہیں۔\n3) **درجہ حرارت میں شدید اتار چڑھاؤ:** شدید گرمی یا سردی پودوں کی قوت مدافعت کمزور کر دیتی ہے۔\n4) **غیر متوازن کھاد:** اضافی یوریا کا استعمال کیڑوں اور بیماریوں کو دعوت دیتا ہے۔\n\n**حفاظتی تدابیر:** کھیت میں نکاسی آب کا مناسب انتظام رکھیں، پودوں میں مناسب فاصلہ رکھیں اور ضرورت پڑنے پر بر وقت فنگس کش اسپرے کریں۔"
    },
    {
        "topic": "fertilizer_guidance",
        "crop": "General",
        "query_templates": [
            "how to use fertilizer properly", "best time to apply urea npk", "fertilizer precautions in crop",
            "khad kab deni chahiye", "urea dalkar fasal kaise bachaye", "उर्वरक और खाद का सही उपयोग",
            "खाद कब और कैसे डालें", "यूरिया और डीएपी का छिड़काव", "کھاد اور یوریا کا صحیح استعمال کیسے کریں",
            "ڈی اے پی اور یوریا کھاد ڈالنے کا طریقہ", "کون سی کھاد اچھی ہے", "khad kab dale"
        ],
        "answer_en": "Fertilizer best practices: 1) Apply basal doses of Phosphorus (DAP) and Potash during sowing; 2) Top-dress Nitrogen (Urea) in split doses during active tillering/vegetative stages; 3) Avoid spraying fertilizer right before heavy rains to prevent leaching; 4) Balance with micronutrients (Zinc, Boron).",
        "answer_hi": "उर्वरक (खाद) प्रबंधन के मुख्य नियम:\n1) बुवाई के समय डीएपी (फास्फोरस) और पोटाश की पूरी मात्रा दें।\n2) यूरिया (नाइट्रोजन) को 2-3 किस्तों में बांटकर दें (कल्ले फूटते समय व वृद्धि काल में)।\n3) बारिश आने से ठीक पहले या खेत में पानी भरा होने पर यूरिया न डालें, इससे खाद बह जाती है।\n4) जिंक और बोरॉन जैसे सूक्ष्म पोषक तत्वों का संतुलित प्रयोग करें।",
        "answer_ur": "کھاد کے استعمال کے اہم اصول:\n1) بجائی کے وقت ڈی اے پی (فاسفورس) اور پوٹاش کی بنیادی مقدار دیں۔\n2) یوریا (نائٹروجن) کو 2 سے 3 اقساط میں دیں تاکہ ضائع نہ ہو۔\n3) بارش سے عین قبل یا پانی کھڑا ہونے پر یوریا نہ ڈالیں کیونکہ کھاد بہہ جاتی ہے۔\n4) زنک اور بوران جیسے مائیکرو نیوٹرینٹس کا متوازن استعمال کریں۔"
    },
    {
        "topic": "pesticide_spraying_rules",
        "crop": "General",
        "query_templates": [
            "when to spray pesticide or fungicide", "best weather for spraying crops",
            "dawa ka chhidkaw kab kare", "kitnashak chhidkaw ke niyam", "कीटनाशक का छिड़काव कब करना चाहिए",
            "दवा छिड़कने का सही समय और मौसम", "फफूंदनाशक का स्प्रे कब करें", "dawa kab dale",
            "کیڑے مار اور فنگس کش دوا کا اسپرے کب کریں", "اسپرے کرنے کا بہترین وقت اور طریقہ", "دوا کا اسپرے کب کریں"
        ],
        "answer_en": "Safe pesticide spraying rules: 1) Spray during calm morning or late afternoon hours (wind speed < 12 km/h); 2) Avoid spraying if rain is expected within 4-6 hours; 3) Do not spray during peak afternoon heat (>32°C) to prevent leaf scorch; 4) Always wear protective gear and maintain proper dilution.",
        "answer_hi": "कीटनाशक व फफूंदनाशक छिड़काव के मुख्य नियम:\n1) छिड़काव हमेशा सुबह या शाम के शांत मौसम में करें (हवा की गति 12 किमी/घंटे से कम हो)।\n2) यदि अगले 4-6 घंटों में बारिश की संभावना हो तो दवा का छिड़काव टाल दें।\n3) दोपहर की तेज धूप और गर्मी (>32°C) में छिड़काव न करें, इससे पत्तियां जल सकती हैं।\n4) दवा का सही अनुपात रखें और सुरक्षात्मक मास्क का उपयोग करें।",
        "answer_ur": "اسپرے کے محفوظ اور مؤثر طریقے:\n1) اسپرے ہمیشہ صبح یا شام کے پرسکون وقت میں کریں جب ہوا کی رفتار کم ہو۔\n2) اگر اگلے 4 تا 6 گھنٹوں میں بارش کا امکان ہو تو اسپرے نہ کریں۔\n3) دوپہر کی شدید دھوپ (>32°C) میں اسپرے نہ کریں ورنہ پتے جل سکتے ہیں۔\n4) دوا کی درست مقدار رکھیں اور ماسک و حفاظتی سامان استعمال کریں۔"
    },
    {
        "topic": "yellow_leaves_causes",
        "crop": "General",
        "query_templates": [
            "why are my leaves turning yellow", "causes of yellow leaves in crops", "leaf chlorosis remedy",
            "pattiya peeli kyu hoti hai", "patte peele pad rahe hai", "पत्तियां पीली क्यों हो रही हैं",
            "पत्ते पीले पड़ने का कारण और उपचार", "पत्तियों में पीलापन कैसे ठीक करें",
            "پتے پیلے کیوں پڑ رہے ہیں", "پتوں کی زردی کی وجوہات اور علاج", "پتے پیلے ہونے کا علاج"
        ],
        "answer_en": "Common causes of yellowing leaves (chlorosis): 1) Nitrogen deficiency (starts in older lower leaves); 2) Root overwatering or waterlogging starving roots of oxygen; 3) Iron/Zinc deficiency (yellowing between veins in new leaves); 4) Sap-sucking pests (aphids, whiteflies, thrips). Remedy: Check field moisture, apply balanced urea/zinc spray, and inspect undersides of leaves for pests.",
        "answer_hi": "पत्तियों के पीले पड़ने (Chlorosis) के मुख्य कारण एवं उपाय:\n1) **नाइट्रोजन की कमी:** पुरानी और निचली पत्तियां सबसे पहले पीली पड़ती हैं -> यूरिया की हल्की मात्रा दें।\n2) **जलभराव (अधिक पानी):** जड़ों को हवा न मिलने से पौधा पीला पड़ता है -> खेत से तुरंत पानी निकालें।\n3) **सूक्ष्म पोषक तत्वों (जिंक/आयरन) की कमी:** नई पत्तियों की शिराओं के बीच पीलापन -> 0.5% जिंक सल्फेट या सूक्ष्म पोषक स्प्रे करें।\n4) **रस चूसक कीट:** सफेद मक्खी या थ्रिप्स -> नीम तेल (5ml/L) का छिड़काव करें।",
        "answer_ur": "پتوں کے پیلے ہونے (کلوروسس) کی اہم وجوہات اور علاج:\n1) **نائٹروجن کی کمی:** سب سے پہلے نچلے اور پرانے پتے پیلے ہوتے ہیں -> یوریا کی معتدل مقدار دیں۔\n2) **اضافی پانی اور نمی:** جڑوں کو ہوا نہ ملنے سے پودا پیلا پڑتا ہے -> کھیت سے فالتو پانی نکالیں۔\n3) **زنک یا آئرن کی کمی:** نئے پتوں کے رگوں کے درمیان زردی -> زنک سلفیٹ کا ہلکا اسپرے کریں۔\n4) **رس چوسنے والے کیڑے:** سفید مکھی یا تھرپس -> نیم کا تیل یا مناسب کیڑے مار دوا استعمال کریں۔"
    },
    {
        "topic": "fungal_disease_causes",
        "crop": "General",
        "query_templates": [
            "what causes fungal disease", "how does fungus spread in crops", "fungal infection prevention",
            "faphund rog kyu hota hai", "fungus kaise lagti hai", "फफूंद रोग किस कारण होता है",
            "फंगल इन्फेक्शन से कैसे बचाएं", "फफूंद की बीमारी का कारण",
            "پھپھوندی کی کیا وجوہات ہیں", "فنگس کیسے پھیلتی ہے", "فنگل بیماری سے بچاؤ"
        ],
        "answer_en": "Fungal diseases (Blight, Rust, Mildew, Rot) spread through: 1) High atmospheric humidity (>75%) coupled with moderate temperatures (20-30°C); 2) Wet leaf canopy from overhead watering or dense unpruned planting; 3) Rain splashes carrying spores from infected soil/residues. Prevention: Prune lower leaves for aeration, avoid evening irrigation, and apply preventive bio-fungicides (Trichoderma or Copper Oxychloride).",
        "answer_hi": "फफूंद (Fungus) जनित रोग फैलने के प्रमुख वैज्ञानिक कारण:\n1) **अत्यधिक नमी (>75%) व अनुकूल तापमान (20-30°C):** यह मौसम फंगल बीजाणुओं के अंकुरण के लिए सबसे अनुकूल होता है।\n2) **पत्तियों पर लगातार गीलापन:** ऊपर से पानी देने या घना रोपण होने से धूप व हवा नहीं पहुंचती।\n3) **संक्रमित मिट्टी व अवशेष:** पिछली फसल के अवशेषों से फफूंद नई फसल में फैलती है।\n\n**रोकथाम:** खेत में उचित दूरी और हवा का संचार रखें, जलभराव से बचें और कॉपर फफूंदनाशक या ट्राइकोडर्मा का सुरक्षात्मक छिड़काव करें।",
        "answer_ur": "پھپھوندی (فنگس) کی بیماری پھیلنے کی اہم وجوہات:\n1) **زیادہ ہوا میں نمی (>75%) اور معتدل درجہ حرارت (20-30°C):** یہ موسم فنگس کے جراثیم کی نشوونما کے لیے سازگار ہوتا ہے۔\n2) **پتوں کا مسلسل گیلا رہنا:** گھنے پودوں اور سورج کی روشنی نہ پہنچنے سے نمی جمع رہتی ہے۔\n3) **پچھلی فصل کے جراثیم:** زمین میں موجود پرانے متاثرہ پودوں کے باقیات سے فنگس پھیلتی ہے۔\n\n**بچاؤ:** پودوں کے درمیان مناسب فاصلہ رکھیں، شام کے وقت پانی دینے سے گریز کریں اور حفاظتی کاپر فنگس کش دوا کا اسپرے کریں۔"
    },
    {
        "topic": "irrigation_management",
        "crop": "General",
        "query_templates": [
            "how often to irrigate crop", "water requirements in farming", "best irrigation practice",
            "sinchai kab aur kaise kare", "pani kab lagana chahiye", "सिंचाई कब और कैसे करें",
            "फसल में पानी देने का सही नियम", "खेत में कब पानी लगाएं",
            "آبپاشی کا صحیح طریقہ", "فصل کو پانی کب دیں", "کتنے دنوں بعد پانی لگائیں"
        ],
        "answer_en": "Irrigation guidelines: 1) Irrigate based on critical crop growth stages (crown root initiation, flowering, grain-filling); 2) Prefer early morning or evening irrigation to minimize evaporation; 3) Adopt drip or furrow irrigation to save 40-50% water and reduce fungal humidity stress; 4) Stop irrigation 10-15 days before harvest.",
        "answer_hi": "सिंचाई प्रबंधन के मुख्य नियम:\n1) फसल के महत्वपूर्ण चरणों में पानी अवश्य दें (जैसे कल्ले फूटते समय, फूल आने पर और दाना भरते समय)।\n2) हमेशा सुबह या शाम के समय सिंचाई करें ताकि वाष्पीकरण से पानी बर्बाद न हो।\n3) ड्रिप या फव्वारा सिंचाई अपनाएं जिससे 40% तक पानी बचता है और फफूंद का खतरा घटता है।\n4) फसल पकने और कटाई से 10-15 दिन पहले सिंचाई बंद कर दें।",
        "answer_ur": "آبپاشی کے بنیادی اور اہم اصول:\n1) فصل کے نازک مراحل (شاخیں نکلتے وقت، پھول آنے پر اور دانہ بنتے وقت) پر وتر لازمی رکھیں۔\n2) پانی ہمیشہ صبح کے وقت یا شام ڈھلے لگائیں تاکہ بخارات کی صورت میں پانی ضائع نہ ہو۔\n3) ڈرپ یا قطرہ قطرہ آبپاشی کا طریقہ اپنائیں تاکہ پانی کی بچت ہو اور فنگس کے حملے سے بچا جا سکے۔\n4) کٹائی سے 10 تا 15 دن قبل پانی دینا بند کر دیں۔"
    },
    {
        "topic": "crop_yield_improvement",
        "crop": "General",
        "query_templates": [
            "how to increase crop yield", "tips to improve production", "bumper harvest guide",
            "paidavar kaise badhaye", "fasal ki upaj badhane ke upay", "पैदावार कैसे बढ़ाएं",
            "फसल की उपज बढ़ाने के उपाय", "अधिक उत्पादन कैसे प्राप्त करें", "बंपर पैदावार की तकनीक",
            "پیداوار بڑھانے کے طریقے", "فصل کی پیداوار میں اضافہ کیسے کریں", "اچھی فصل اور زیادہ پیداوار"
        ],
        "answer_en": "5 Golden Rules to Maximize Crop Yield:\n1) Certified Seeds & Bio-Treatment: Inoculate seeds with Trichoderma or Rhizobium prior to sowing.\n2) Balanced NPK + Micronutrients: Avoid urea overuse; provide balanced Basal DAP, Potash, and foliar Zinc/Boron.\n3) Critical Irrigation Timing: Maintain root-zone moisture during tillering, flowering, and grain filling.\n4) Weed Management: Eliminate weeds within the first 25-30 days to stop nutrient competition.\n5) Integrated Pest Management: Apply preventive neem oil (5ml/L) and install pheromone/yellow sticky traps.",
        "answer_hi": "🌾 **फसल की बंपर पैदावार प्राप्त करने के 5 मुख्य वैज्ञानिक नियम:**\n\n1) **प्रमाणित बीज एवं बीज शोधन:** बुवाई से पहले बीजों को ट्राइकोडर्मा या फफूंदनाशक से उपचारित करें।\n2) **संतुलित खाद (NPK + सूक्ष्म पोषक):** सिर्फ यूरिया पर निर्भर न रहें; डीएपी, पोटाश, जिंक और सल्फर का संतुलित प्रयोग करें।\n3) **क्रांतिक अवस्थाओं पर सिंचाई:** कल्ले फूटते समय, फूल आने पर और दाना भरते समय खेत में नमी बनाए रखें।\n4) **खरपतवार नियंत्रण:** बुवाई के 20-30 दिनों के भीतर निराई-गुड़ाई करके खरपतवार हटाएं ताकि खाद की बर्बादी न हो।\n5) **एकीकृत कीट प्रबंधन:** कीटों के शुरुआती प्रकोप पर नीम तेल (5ml/लीटर) और पीले चिपचिपे ट्रैप का उपयोग करें।",
        "answer_ur": "🌾 **فصل کی شاندار پیداوار حاصل کرنے کے 5 سنہری اصول:**\n\n1) **تصدیق شدہ بیج اور بیج کا علاج:** بوائی سے قبل بیج کو فنگس کش دوا یا ٹرائیکوڈرما سے ٹریٹ کریں۔\n2) **متوازن کھاد کا استعمال:** مٹی کے ٹیسٹ کی بنیاد پر ڈی اے پی، یوریا، پوٹاش اور زنک کی متوازن مقدار دیں۔\n3) **نازک مراحل پر بروقت آبپاشی:** شاخیں نکلتے وقت، پھول آنے پر اور دانہ بنتے وقت وتر کی کمی نہ ہونے دیں۔\n4) **جڑی بوٹیوں کی تلفی:** فصل کے ابتدائی 30 دنوں میں جڑی بوٹیاں تلف کریں تاکہ کھاد اور پانی ضائع نہ ہو۔\n5) **بروقت کیڑوں کی روک تھام:** رس چوسنے والے کیڑوں کے لیے شروع میں نیم کا تیل اور پیلے اسٹیکی کارڈز استعمال کریں۔"
    },
    {
        "topic": "pest_control_and_insects",
        "crop": "General",
        "query_templates": [
            "how to control insects and pests", "safed makkhi keede se bachav", "pest attack remedy",
            "keede lag gaye hai kya kare", "fasal me keede se kaise bache", "कीड़े लग गए हैं क्या करें",
            "फसल में कीड़ों से बचाव के उपाय", "सफेद मक्खी और सुंडी की रोकथाम", "कीट प्रबंधन",
            "کیڑوں سے بچاؤ کے طریقے", "فصل میں کیڑے لگ جائیں تو کیا کریں", "سنڈی اور سفید مکھی کا علاج"
        ],
        "answer_en": "Integrated Pest Management (IPM) Protocols:\n1) Sap-Sucking Pests (Whiteflies, Aphids, Thrips): Install yellow sticky traps (15-20 per acre) and spray 5ml/L cold-pressed neem oil.\n2) Caterpillars, Borers & Armyworms: Spray Emamectin Benzoate 5% SG or Bacillus thuringiensis (Bt) at initial larval stages.\n3) Application Rules: Spray during cool morning or evening hours with wind speed < 12 km/h; avoid midday heat.",
        "answer_hi": "🐛 **फसल सुरक्षा एवं कीट प्रबंधन मार्गदर्शिका:**\n\n• **रस चूसक कीट (सफेद मक्खी, माहू, थ्रिप्स):** खेत में पीले चिपचिपे ट्रैप लगाएं और 5ml/लीटर नीम तेल का छिड़काव करें।\n• **सुंडी एवं तना छेदक कीट:** प्रारंभिक प्रकोप पर इमामेक्टिन बेंजोएट (5% SG) या जैविक कीटनाशक का प्रयोग करें।\n• **छिड़काव नियम:** हमेशा सुबह या शाम के शांत समय में स्प्रे करें, तेज धूप में छिड़काव न करें।",
        "answer_ur": "🐛 **فصلوں میں کیڑوں کے جامع انسداد کی گائیڈ:**\n\n• **رس چوسنے والے کیڑے (سفید مکھی، تھرپس):** پیلے چپکنے والے کارڈز (Yellow Traps) لگائیں اور نیم کا تیل (5ml فی لیٹر) اسپرے کریں۔\n• **تنے کی سنڈی اور فال آرمی ورم:** ابتدائی حالت میں ایما مائل بینزویٹ یا تجویز کردہ کیڑے مار دوا دیں۔\n• **حفاظتی اقدام:** دوپہر کی شدید دھوپ میں اسپرے نہ کریں تاکہ دوا کا پورا اثر ہو۔"
    }
]

class LocalFarmerChatbot:
    """
    Local domain-specific agricultural & weather conversational assistant.
    Supports English, Hindi, and Urdu with zero external LLM API dependencies.
    Features autonomous continuous self-learning, intent classification, and real-time knowledge adaptation.
    """
    def __init__(self, knowledge_base_path: Optional[str] = None):
        self.reasoning_engine = AgriculturalReasoningEngine()
        self.knowledge_base = {}

        ai_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(ai_dir)
        root_dir = os.path.dirname(base_dir)

        # 1. Load Crop Knowledge Base
        kb_candidates = [
            knowledge_base_path,
            os.path.join(base_dir, "data", "knowledge_base", "crop_knowledge.json"),
            os.path.join(root_dir, "Data", "knowledge_base", "crop_knowledge.json"),
            os.path.join("Data", "knowledge_base", "crop_knowledge.json")
        ]
        for candidate in kb_candidates:
            if candidate and os.path.exists(candidate):
                try:
                    with open(candidate, "r", encoding="utf-8") as f:
                        self.knowledge_base = json.load(f)
                    break
                except Exception:
                    pass

        # 2. Initialize Self-Learning Knowledge & Feedback Engine
        self.self_learning_engine = SelfLearningEngine()
        self.learning_engine = self.self_learning_engine

        # 3. Syntactic Model (loaded lazily if needed to keep RAM under 512MB)
        self._syntactic_model = None
        self._syntax_candidates = [
            os.path.join(ai_dir, "syntactic_language_model.json"),
            os.path.join(ai_dir, "saved_models", "syntactic_language_model.json"),
            os.path.join(root_dir, "Practical_09_NLP_App", "syntactic_language_model.json"),
            "Practical_09_NLP_App/syntactic_language_model.json"
        ]

        # 4. Load Trained Urdu Instruction & Agricultural AI Model
        self.urdu_instruct_model = []
        urdu_candidates = [
            os.path.join(ai_dir, "urdu_ai_model.json"),
            os.path.join(ai_dir, "saved_models", "urdu_ai_model.json"),
            os.path.join(root_dir, "Practical_09_NLP_App", "urdu_ai_model.json"),
            "Practical_09_NLP_App/urdu_ai_model.json"
        ]
        for uc in urdu_candidates:
            if uc and os.path.exists(uc):
                try:
                    with open(uc, "r", encoding="utf-8") as f:
                        u_data = json.load(f)
                        self.urdu_instruct_model = u_data.get("doc_registry", []) or u_data.get("instruction_dataset", [])
                    break
                except Exception:
                    pass

        # Build TF-IDF index over base corpus, knowledge_base crops, Urdu instruct, and learned entries
        self.rebuild_index()

    def rebuild_index(self) -> None:
        """Rebuilds the TF-IDF retrieval matrix combining base corpus, crop knowledge base, Urdu instruct model, and learned entries."""
        self.corpus_entries = []
        self.corpus_documents = []

        # 1. Base Agricultural Corpus
        for entry in AGRICULTURAL_CORPUS:
            combined_text = (
                " ".join(entry["query_templates"])
                + " " + entry["answer_en"]
                + " " + entry.get("answer_hi", "")
                + " " + entry.get("answer_ur", "")
            )
            clean_text = self.preprocess_text(combined_text)
            self.corpus_entries.append(entry)
            self.corpus_documents.append(clean_text)

        # 2. Ingest All Crops from Crop Knowledge Base in Multilingual Form
        for crop_name, c_info in self.knowledge_base.items():
            crop_hi = CROP_HINDI_NAMES.get(crop_name, crop_name)
            crop_ur = CROP_URDU_NAMES.get(crop_name, crop_name)
            
            # Crop Profile Entry
            profile_entry = {
                "topic": f"{crop_name.lower()}_agronomic_guide",
                "crop": crop_name,
                "query_templates": [
                    f"{crop_name} farming guide", f"{crop_name} cultivation", f"{crop_name} requirements",
                    f"{crop_hi} की खेती", f"{crop_hi} की जानकारी", f"{crop_hi} का मौसम",
                    f"{crop_ur} کی کاشت", f"{crop_ur} کی معلومات", f"{crop_ur} کا طریقہ"
                ],
                "answer_en": f"{crop_name} optimal conditions: Temp {c_info.get('temp_optimal', (20,30))[0]}-{c_info.get('temp_optimal', (20,30))[1]}°C, Humidity {c_info.get('humidity_optimal', (50,70))[0]}-{c_info.get('humidity_optimal', (50,70))[1]}%, Rainfall {c_info.get('rainfall_optimal', (50,150))[0]}-{c_info.get('rainfall_optimal', (50,150))[1]} mm. Soil: {c_info.get('soil_type', 'Loam')}.",
                "answer_hi": f"{crop_hi} की सफल खेती के लिए अनुकूल तापमान {c_info.get('temp_optimal', (20,30))[0]}°C से {c_info.get('temp_optimal', (20,30))[1]}°C, नमी {c_info.get('humidity_optimal', (50,70))[0]}% से {c_info.get('humidity_optimal', (50,70))[1]}% और उपयुक्त मिट्टी {c_info.get('soil_type', 'दोमट')} है।",
                "answer_ur": f"{crop_ur} کی اچھی پیداوار کے لیے موزوں درجہ حرارت {c_info.get('temp_optimal', (20,30))[0]}°C تا {c_info.get('temp_optimal', (20,30))[1]}°C، ہوا میں نمی {c_info.get('humidity_optimal', (50,70))[0]}% تا {c_info.get('humidity_optimal', (50,70))[1]}% اور موزوں زمین {c_info.get('soil_type', 'زرخیز میرا')} ہے۔"
            }
            clean_text = self.preprocess_text(" ".join(profile_entry["query_templates"]) + " " + profile_entry["answer_en"] + " " + profile_entry["answer_hi"] + " " + profile_entry["answer_ur"])
            self.corpus_entries.append(profile_entry)
            self.corpus_documents.append(clean_text)

            # Crop Precautions Entry
            precautions_hi = CROP_PRECAUTIONS_HI.get(crop_name, [])
            precautions_ur = CROP_PRECAUTIONS_UR.get(crop_name, [])
            precautions_en = c_info.get("precautions", [])
            prec_entry = {
                "topic": f"{crop_name.lower()}_precautions",
                "crop": crop_name,
                "query_templates": [
                    f"{crop_name} precautions", f"{crop_name} care guidelines", f"{crop_name} protection",
                    f"{crop_hi} की सावधानियां", f"{crop_hi} का बचाव", f"{crop_hi} की सुरक्षा",
                    f"{crop_ur} کی احتیاطی تدابیر", f"{crop_ur} کا بچاؤ", f"{crop_ur} کی دیکھ بھال"
                ],
                "answer_en": f"🌾 **Key Precautions & Protection Guidelines for {crop_name}:**\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(precautions_en[:4])]),
                "answer_hi": f"🌾 **{crop_hi} की फसल के लिए मुख्य सावधानियां:**\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(precautions_hi[:4]) if precautions_hi] or [f"{i+1}. {p}" for i, p in enumerate(precautions_en[:4])]),
                "answer_ur": f"🌾 **{crop_ur} کی فصل کے لیے اہم احتیاطی تدابیر:**\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(precautions_ur[:4]) if precautions_ur] or [f"{i+1}. {p}" for i, p in enumerate(precautions_en[:4])])
            }
            clean_text = self.preprocess_text(" ".join(prec_entry["query_templates"]) + " " + prec_entry["answer_en"] + " " + prec_entry["answer_hi"] + " " + prec_entry["answer_ur"])
            self.corpus_entries.append(prec_entry)
            self.corpus_documents.append(clean_text)

        # 3. Ingest Urdu Instruction Dataset
        for item in self.urdu_instruct_model:
            inst = item.get("instruction", "") or item.get("input", "")
            inp = item.get("input", "")
            out = item.get("response", "") or item.get("output", "")
            intent = item.get("intent", "urdu_instruct_qa")
            if out:
                templates = [t for t in [inst, inp] if t]
                u_entry = {
                    "topic": intent,
                    "crop": item.get("crop", "General"),
                    "query_templates": templates if templates else [out[:30]],
                    "answer_en": out,
                    "answer_hi": out,
                    "answer_ur": out
                }
                clean_text = self.preprocess_text(" ".join(u_entry["query_templates"]) + " " + out)
                self.corpus_entries.append(u_entry)
                self.corpus_documents.append(clean_text)

        # 4. Ingest Dynamically Learned Entries from Self-Learning Engine
        learned_entries = self.self_learning_engine.get_learned_corpus()
        for entry in learned_entries:
            combined_text = (
                " ".join(entry.get("query_templates", []))
                + " " + entry.get("answer_en", "")
                + " " + entry.get("answer_hi", "")
                + " " + entry.get("answer_ur", "")
            )
            clean_text = self.preprocess_text(combined_text)
            self.corpus_entries.append(entry)
            self.corpus_documents.append(clean_text)

        # Build Unicode-aware TF-IDF Vectorizer with strict float32 and max_features to fit 512MB RAM
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            token_pattern=r'[\u0900-\u097F\u0600-\u06FF\w]+',
            max_features=3000,
            dtype=np.float32,
            min_df=1
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus_documents)
        import gc; gc.collect()

    @property
    def syntactic_model(self):
        if self._syntactic_model is None:
            self._syntactic_model = {}
            for sc in self._syntax_candidates:
                if sc and os.path.exists(sc):
                    try:
                        with open(sc, "r", encoding="utf-8") as f:
                            self._syntactic_model = json.load(f)
                        break
                    except Exception:
                        pass
        return self._syntactic_model

    def detect_language(self, text: str) -> str:
        """
        Detects whether text is Urdu ('ur'), Hindi ('hi'), or English ('en').
        """
        # Urdu / Arabic Unicode Block
        if re.search(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', text):
            return "ur"
        # Devanagari Unicode Block (Hindi)
        if re.search(r'[\u0900-\u097F]', text):
            return "hi"

        # Romanized keywords
        lower = text.lower()
        words = lower.split()
        urdu_roman_markers = ["gandum", "makai", "ehtiyat", "tadabeer", "hifazat", "spray", "abpashi", "chawal", "khad", "dawa", "kare", "karna", "mausam"]
        hindi_roman_markers = ["gehun", "tamatar", "savdhani", "upchar", "upaay", "chhidkaw", "barish", "taapman", "peeli", "patti", "kya", "kaise", "hai", "hain"]
        
        if any(w in urdu_roman_markers for w in words):
            return "ur"
        if any(w in hindi_roman_markers for w in words):
            return "hi"

        return "en"

    def preprocess_text(self, text: str) -> str:
        """
        Tokenization, lowercasing, synonym mapping, and stopword filtering across EN, HI, UR.
        """
        if re.search(r'[\u0600-\u06FF]', text):
            text = re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED]', '', text)
            char_map = {'ي': 'ی', 'ى': 'ی', 'ئ': 'ی', 'ك': 'ک', 'ة': 'ہ', 'ۂ': 'ہ', 'ه': 'ہ', 'ؤ': 'و', 'أ': 'ا', 'إ': 'ا', 'آ': 'ا'}
            text = "".join(char_map.get(c, c) for c in text)

        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\u0900-\u097F\u0600-\u06FF\s]', ' ', text)
        tokens = text.split()

        cleaned_tokens = []
        for t in tokens:
            normalized = SYNONYM_MAP.get(t, t)
            if normalized not in STOPWORDS and len(normalized) > 1:
                cleaned_tokens.append(normalized)

        return " ".join(cleaned_tokens)

    def detect_crop_in_text(self, text: str) -> Optional[str]:
        """
        Identifies crop names in English, Hindi, Urdu, or Romanized transcripts.
        """
        norm_text = text
        if re.search(r'[\u0600-\u06FF]', text):
            norm_text = re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED]', '', text)
            char_map = {'ي': 'ی', 'ى': 'ی', 'ئ': 'ی', 'ك': 'ک', 'ة': 'ہ', 'ۂ': 'ہ', 'ه': 'ہ', 'ؤ': 'و', 'أ': 'ا', 'إ': 'ا', 'آ': 'ا'}
            norm_text = "".join(char_map.get(c, c) for c in norm_text)

        text_lower = norm_text.lower()

        # 1. Match from multi-script CROP_NAME_MAP
        sorted_keys = sorted(CROP_NAME_MAP.items(), key=lambda x: len(x[0]), reverse=True)
        for key, crop_name in sorted_keys:
            if key.isascii():
                if re.search(r'\b' + re.escape(key) + r'\b', text_lower):
                    return crop_name
            else:
                pattern = r'(?<![\u0900-\u097F\u0600-\u06FF\w])' + re.escape(key) + r'(?![\u0900-\u097F\u0600-\u06FF\w])'
                if re.search(pattern, norm_text):
                    return crop_name

        # 2. Match from Romanized keywords
        for key, crop_name in ROMANIZED_CROP_KEYWORDS.items():
            if re.search(r'\b' + re.escape(key) + r'\b', text_lower):
                return crop_name

        return None

    @staticmethod
    def normalize_urdu(text: str) -> str:
        """Standardizes Urdu letters and removes aerab/diacritics."""
        if not text:
            return ""
        text = re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED]', '', text)
        char_map = {'ي': 'ی', 'ى': 'ی', 'ئ': 'ی', 'ك': 'ک', 'ة': 'ہ', 'ۂ': 'ہ', 'ه': 'ہ', 'ؤ': 'و', 'أ': 'ا', 'إ': 'ا', 'آ': 'ا'}
        return "".join(char_map.get(c, c) for c in text).lower()

    def ask(
        self,
        question: str,
        active_crop: Optional[str] = None,
        current_prediction: Optional[Dict[str, Any]] = None,
        language: Optional[str] = "auto"
    ) -> Dict[str, Any]:
        """
        Contextual & Intent-Driven Question Answering across English, Hindi, and Urdu.
        Features accurate intent classification, weather stress correlation, and autonomous self-learning.
        """
        target_lang = language if language in ["en", "hi", "ur"] else self.detect_language(question)
        is_hindi = (target_lang == "hi")
        is_urdu = (target_lang == "ur")

        if not question or not question.strip():
            if is_urdu:
                empty_msg = "براہ کرم اپنی فصل یا موسم کے بارے میں کوئی سوال درج کریں۔"
            elif is_hindi:
                empty_msg = "कृपया अपनी फसल या मौसम से संबंधित कोई प्रश्न पूछें।"
            else:
                empty_msg = "Please enter a specific question regarding your crop or current weather conditions."

            return {
                "answer": empty_msg,
                "confidence": 0.0,
                "matched_topic": "empty_query",
                "category": "system",
                "reasoning_summary": "No input provided."
            }

        cleaned_query = self.preprocess_text(question)
        detected_crop = self.detect_crop_in_text(question) or active_crop or (current_prediction.get("crop") if current_prediction else None)
        lower_raw = self.normalize_urdu(question.lower())

        curr_weather = {}
        if current_prediction and "weather" in current_prediction:
            curr_weather = current_prediction["weather"]

        result = None

        # =========================================================================
        # INTENT -1: Active Prediction Context Follow-up ("What should I do?", etc.)
        # =========================================================================
        is_advice_query = any(w in lower_raw for w in [
            "what should i do", "what to do", "how to proceed", "advice", "recommendation", "kya karu", "kya kare",
            "kya karna chahiye", "kya upchar kare", "کیا کروں", "کیا کریں", "کیا کرنا چاہیے", "کیا تدبیر ہے",
            "क्या करूं", "क्या करें", "क्या करना चाहिए", "क्या उपाय करें"
        ])

        if current_prediction and is_advice_query:
            c_name = current_prediction.get("crop", detected_crop or "Crop")
            h_status = current_prediction.get("health_status", "Evaluated")
            r_level = current_prediction.get("risk_level", "Moderate")
            causes = current_prediction.get("causes", [])
            precautions = current_prediction.get("precautions", [])
            explanation = current_prediction.get("ai_explanation", "")

            if is_urdu:
                crop_disp = CROP_URDU_NAMES.get(c_name, c_name)
                prec_list = "\n".join([f"• {p}" for p in precautions[:3]]) if precautions else "• کھیت میں مناسب وتر اور نکاسی رکھیں۔"
                causes_list = "\n".join([f"• {c}" for c in causes[:2]]) if causes else ""
                ans = (
                    f"🌾 **{crop_disp} کی موجودہ حالت ({h_status} - خطرہ: {r_level}):**\n\n"
                    f"**اہم حفاظتی تدابیر:**\n{prec_list}\n\n"
                    + (f"**وجوہات:**\n{causes_list}\n\n" if causes_list else "")
                    + f"**تجزیہ:** {explanation}"
                )
            elif is_hindi:
                crop_disp = CROP_HINDI_NAMES.get(c_name, c_name)
                prec_list = "\n".join([f"• {p}" for p in precautions[:3]]) if precautions else "• खेत में उचित नमी और जल निकासी बनाए रखें।"
                causes_list = "\n".join([f"• {c}" for c in causes[:2]]) if causes else ""
                ans = (
                    f"🌾 **{crop_disp} की वर्तमान स्थिति ({h_status} - जोखिम: {r_level}):**\n\n"
                    f"**मुख्य सावधानियां एवं उपाय:**\n{prec_list}\n\n"
                    + (f"**कारण:**\n{causes_list}\n\n" if causes_list else "")
                    + f"**विश्लेषण:** {explanation}"
                )
            else:
                prec_list = "\n".join([f"• {p}" for p in precautions[:3]]) if precautions else "• Maintain optimal field drainage and soil moisture."
                causes_list = "\n".join([f"• {c}" for c in causes[:2]]) if causes else ""
                ans = (
                    f"🌾 **Current Analysis for {c_name} ({h_status} - Risk: {r_level}):**\n\n"
                    f"**Recommended Actions & Precautions:**\n{prec_list}\n\n"
                    + (f"**Causes Identified:**\n{causes_list}\n\n" if causes_list else "")
                    + f"**AI Explanation:** {explanation}"
                )

            result = {
                "answer": ans,
                "confidence": 0.96,
                "matched_topic": f"{c_name.lower()}_context_advice",
                "category": "context_advisory",
                "reasoning_summary": f"Synthesized advice from active prediction context for {c_name}."
            }

        # =========================================================================
        # INTENT 0: Greetings & Conversational Introductions (Hindi, Urdu, English)
        # =========================================================================
        greeting_patterns = [
            r'\b(?:namaste|namaskar|pranam|ram ram|radhe radhe|kaise ho|kya haal|kaise hain|kya hal)\b',
            r'(?:नमस्ते|नमस्कार|प्रणाम|राम राम|कैसे हो|कैसे हैं|क्या हाल|हालचाल)',
            r'\b(?:salam|assalam|adaab|kese ho|kia hal|kia haal|khush amdeed|khushamdeed)\b',
            r'(?:سلام|السلام علیکم|آداب|کیسے ہیں|کیسے ہو|کیا حال|خیریت)',
            r'\b(?:hello|hey|good morning|good afternoon|good evening|how are you|who are you|what can you do)\b',
            r'^(?:hi|salam|hello)$'
        ]
        is_greeting = any(re.search(p, lower_raw) for p in greeting_patterns)

        if is_greeting:
            if is_urdu:
                ans = (
                    "وعلیکم السلام! میں **CropGuard AI معاون** ہوں، آپ کا مقامی زرعی اور موسمیاتی مشیر۔\n\n"
                    "میں فصلوں کی حفاظت، امراض کی تشخیص، موسمی خطرات، کھاد اور اسپرے کے شیڈول میں آپ کی مدد کے لیے تیار ہوں۔\n\n"
                    "آپ مجھ سے کسی بھی فصل کے بارے میں سوال پوچھ سکتے ہیں یا نیچے دیے گئے تجاویز پر کلک کر سکتے ہیں۔"
                )
            elif is_hindi:
                ans = (
                    "नमस्ते! मैं **CropGuard AI सहायक** हूँ, आपका स्थानीय कृषि एवं मौसम सलाहकार।\n\n"
                    "मैं फसलों के स्वास्थ्य, रोग निवारण, मौसम के खतरे, खाद और कीटनाशक छिड़काव के नियमों में आपकी पूरी सहायता कर सकता हूँ।\n\n"
                    "आप मुझसे किसी भी फसल के बारे में पूछ सकते हैं या नीचे दिए गए सुझावों में से चुन सकते हैं।"
                )
            else:
                ans = (
                    "Namaste! I am the **CropGuard AI Assistant**, your local agricultural intelligence advisor.\n\n"
                    "I am ready to help you with crop disease diagnosis, weather hazard assessment, fertilizer schedules, and precautions.\n\n"
                    "Feel free to ask any question about your crops or current weather conditions."
                )

            result = {
                "answer": ans,
                "confidence": 0.98,
                "matched_topic": "greeting_conversation",
                "category": "conversation",
                "reasoning_summary": "Handled multilingual farmer greeting."
            }

        # =========================================================================
        # INTENT 1: Crop Disease / Pest / Symptoms / Probable Problems / Damage / Risks
        # =========================================================================
        is_disease_query = any(w in lower_raw for w in [
            "problem", "problems", "probable problem", "probable problems", "issue", "issues",
            "risk", "risks", "threat", "threats", "what could go wrong", "damage", "danger",
            "trouble", "disease", "diseases", "pest", "pests", "insect", "insects", "leaf curl",
            "blight", "rust", "blast", "fungus", "spot", "worms", "rog", "bimari", "keeda", "kida",
            "sundi", "jholas", "marna", "safed makkhi", "thrips", "peeli", "yellow", "curl", "wilt", "rot",
            "mildew", "powdery", "downy", "black rot", "measles", "esca",
            "रोग", "बीमारी", "कीड़ा", "कीड़े", "सुंडी", "झुलसा", "रतुआ", "मरोड़िया", "धब्बे", "फफूंद", "पीली", "मुड़", "सिकुड़",
            "समस्या", "समस्याएं", "परेशानी", "नुकसान", "दिक्कत", "खतरा", "जोखिम",
            "بیماری", "کیڑا", "کیڑے", "سنڈی", "پھپھوندی", "مروڑ", "پتہ مروڑ", "دھبے", "نقصان", "پیلا", "پیلے", "مڑ", "مڑنا", "سکڑ", "سڑن", "سفید مکھی",
            "مسئلہ", "مسائل", "خرابی", "پریشانی", "خطرہ", "خطرات", "امراض"
        ])

        if is_disease_query and detected_crop and detected_crop in self.knowledge_base:
            crop_info = self.knowledge_base[detected_crop]
            diseases_en = crop_info.get("diseases", [])
            precautions_en = crop_info.get("precautions", [])
            
            w_context_en, w_context_hi, w_context_ur = "", "", ""
            if curr_weather:
                t = curr_weather.get("temperature", 25.0)
                h = curr_weather.get("humidity", 60.0)
                if h > 60:
                    w_context_en = f"\n\n🌡️ **Current Weather Context ({t:.1f}°C, {h:.1f}% RH):** Elevated humidity ({h:.1f}%) creates a favorable microclimate for fungal spore germination and foliar infections. Ensure adequate canopy airflow."
                    w_context_hi = f"\n\n🌡️ **वर्तमान मौसम प्रभाव ({t:.1f}°C, {h:.1f}% नमी):** अधिक नमी ({h:.1f}%) के कारण फफूंद जनित रोगों और पत्तियों के संक्रमण का खतरा बढ़ जाता है। वायु संचार बनाए रखें।"
                    w_context_ur = f"\n\n🌡️ **موجودہ موسم کا اثر ({t:.1f}°C، {h:.1f}% نمی):** زیادہ نمی ({h:.1f}%) فنگس کے جراثیم پھیلنے اور پتوں کے امراض کا خطرہ بڑھاتی ہے۔ پودوں میں ہوا کی آمدورفت یقینی بنائیں۔"
                else:
                    w_context_en = f"\n\n🌡️ **Current Weather Context ({t:.1f}°C, {h:.1f}% RH):** Weather is moderately dry; monitor for sap-sucking pests and leaf scorch during peak afternoon hours."
                    w_context_hi = f"\n\n🌡️ **वर्तमान मौसम प्रभाव ({t:.1f}°C, {h:.1f}% नमी):** मौसम सामान्य है; दोपहर की धूप में रस चूसने वाले कीटों पर नज़र रखें।"
                    w_context_ur = f"\n\n🌡️ **موجودہ موسم کا اثر ({t:.1f}°C، {h:.1f}% نمی):** موسم معتدل ہے؛ کیڑوں اور پتوں کے جھلسنے سے حفاظت کریں۔"

            if is_urdu:
                crop_display = CROP_URDU_NAMES.get(detected_crop, detected_crop)
                diseases_ur = CROP_DISEASES_UR.get(detected_crop, [])
                precautions_ur = CROP_PRECAUTIONS_UR.get(detected_crop, [])
                
                dis_text = ""
                if diseases_ur:
                    dis_text = "\n\n**اہم امراض، مسائل اور علامات:**\n" + "\n".join([
                        f"• **{d.get('name')}:** {d.get('symptoms', '')}\n  *بچاؤ:* {d.get('precautions', 'تجویز کردہ اسپرے کریں۔')}"
                        for d in diseases_ur
                    ])
                elif diseases_en:
                    dis_text = "\n\n**اہم امراض اور علامات:**\n" + "\n".join([
                        f"• **{d.get('name')}:** {d.get('symptoms', '')} (*تدبیر:* {d.get('precautions', '')})"
                        for d in diseases_en
                    ])
                prec_text = "\n\n**حفاظتی تدابیر:**\n" + "\n".join([f"• {p}" for p in (precautions_ur[:2] if precautions_ur else precautions_en[:2])])
                ans = f"🔬 **{crop_display} کے متوقع مسائل، امراض اور بچاؤ کے طریقے:**{dis_text}{w_context_ur}{prec_text}"
            elif is_hindi:
                crop_display = CROP_HINDI_NAMES.get(detected_crop, detected_crop)
                diseases_hi = CROP_DISEASES_HI.get(detected_crop, [])
                precautions_hi = CROP_PRECAUTIONS_HI.get(detected_crop, [])

                dis_text = ""
                if diseases_hi:
                    dis_text = "\n\n**संभावित रोग, समस्याएं एवं लक्षण:**\n" + "\n".join([
                        f"• **{d.get('name')}:** {d.get('symptoms', '')}\n  *बचाव:* {d.get('precautions', 'जैविक फफूंदनाशक का छिड़काव करें।')}"
                        for d in diseases_hi
                    ])
                elif diseases_en:
                    dis_text = "\n\n**संभावित रोग एवं लक्षण:**\n" + "\n".join([
                        f"• **{d.get('name')}:** {d.get('symptoms', '')} (*उपाय:* {d.get('precautions', '')})"
                        for d in diseases_en
                    ])
                prec_text = "\n\n**सुरक्षात्मक सावधानियां:**\n" + "\n".join([f"• {p}" for p in (precautions_hi[:2] if precautions_hi else precautions_en[:2])])
                ans = f"🔬 **{crop_display} की संभावित समस्याएं, रोग लक्षण एवं रोकथाम:**{dis_text}{w_context_hi}{prec_text}"
            else:
                dis_text = ""
                if diseases_en:
                    dis_text = "\n\n**Probable Diseases & Problem Indicators:**\n" + "\n".join([
                        f"• **{d.get('name')}:** {d.get('symptoms', '')}\n  *Causes & Risk Trigger:* {d.get('causes', d.get('risk_trigger', ''))}\n  *Recommended Action:* {d.get('precautions', '')}"
                        for d in diseases_en
                    ])
                prec_text = "\n\n**Key Protective Measures:**\n" + "\n".join([f"• {p}" for p in precautions_en[:2]])
                ans = f"🔬 **Probable Problems & Disease Diagnosis for {detected_crop}:**{dis_text}{w_context_en}{prec_text}"

            result = {
                "answer": ans,
                "confidence": 0.96,
                "matched_topic": f"{detected_crop.lower()}_probable_problems",
                "category": "crop_disease",
                "reasoning_summary": f"Retrieved probable diseases, symptoms, and risk triggers for {detected_crop}."
            }

        # =========================================================================
        # INTENT 2: Weather Hazards / Warnings / Danger / Environmental Stress
        # =========================================================================
        is_hazard_query = any(w in lower_raw for w in [
            "hazard", "hazards", "any hazard", "weather hazard", "weather hazards", "weather risk", "alert", "warning", "danger",
            "is it safe", "current weather", "today weather", "weather good", "weather condition", "aaj ka mausam", "mausam kaisa",
            "mausam sahi hai", "mausam ka khatra", "mausam ka asar", "khatra", "nuksan", "barish ka khatra", "garmi ka khatra",
            "मौसम कैसा", "आज का मौसम", "मौसम अनुकूल", "मौसम का खतरा", "अलर्ट", "चेतावनी", "खतरा", "आपदा", "लू", "पाला", "भारी बारिश",
            "موسم کیسا", "آج کا موسم", "موسم موزوں", "موسم کی صورتحال", "موسمی خطرہ", "الرٹ", "وارننگ", "طوفان", "گرمی کی لہر", "سیلاب", "خطرہ"
        ])

        if not result and is_hazard_query and curr_weather and detected_crop:
            t = curr_weather.get("temperature", 25.0)
            h = curr_weather.get("humidity", 60.0)
            r = curr_weather.get("rainfall", 0.0)
            w_spd = curr_weather.get("wind_speed", 10.0)
            loc = curr_weather.get("location_name", "Local Farm")

            crop_info = self.knowledge_base.get(detected_crop, {})
            t_min, t_max = crop_info.get("temp_optimal", (18.0, 28.0))
            h_min, h_max = crop_info.get("humidity_optimal", (50.0, 75.0))
            r_min, r_max = crop_info.get("rainfall_optimal", (40.0, 150.0))

            stress_factors_en, stress_factors_hi, stress_factors_ur = [], [], []

            if t < t_min:
                stress_factors_en.append(f"Temperature ({t:.1f}°C) is below optimal ({t_min}°C), which slows vegetative growth and fruit set.")
                stress_factors_hi.append(f"तापमान ({t:.1f}°C) न्यूनतम सीमा ({t_min}°C) से कम है, जिससे फसल की बढ़वार धीमी हो सकती है।")
                stress_factors_ur.append(f"درجہ حرارت ({t:.1f}°C) مطلوبہ حد ({t_min}°C) سے کم ہے، جس سے پودے کی بڑھوتری سست ہو سکتی ہے۔")
            elif t > t_max:
                stress_factors_en.append(f"Temperature ({t:.1f}°C) exceeds the optimal threshold ({t_max}°C). Heat stress hazard; ensure adequate canopy shading and soil moisture.")
                stress_factors_hi.append(f"तापमान ({t:.1f}°C) अधिकतम सीमा ({t_max}°C) से अधिक है। गर्मी और लू का खतरा है; नमी बनाए रखें।")
                stress_factors_ur.append(f"درجہ حرارت ({t:.1f}°C) زیادہ سے زیادہ حد ({t_max}°C) سے زیادہ ہے۔ گرمی کا تناؤ ہو سکتا ہے؛ زمین میں نمی برقرار رکھیں۔")
            else:
                stress_factors_en.append(f"Temperature ({t:.1f}°C) is within safe limits ({t_min}°C - {t_max}°C).")

            if h > h_max:
                stress_factors_en.append(f"Relative humidity ({h:.1f}%) is elevated (optimal: {h_min}-{h_max}%), increasing fungal spore germination hazard.")
                stress_factors_hi.append(f"हवा में नमी ({h:.1f}%) अधिक है (अनुकूल: {h_min}-{h_max}%), जिससे फफूंद और सड़न का खतरा है।")
                stress_factors_ur.append(f"ہوا میں نمی ({h:.1f}%) زیادہ ہے (مطلوبہ: {h_min}-{h_max}%)، جس سے فنگس اور بیماری کا خطرہ بڑھتا ہے۔")
            elif h < h_min:
                stress_factors_en.append(f"Relative humidity ({h:.1f}%) is low (optimal: {h_min}-{h_max}%), increasing transpiration and mite risk.")
                stress_factors_hi.append(f"हवा में नमी ({h:.1f}%) कम है, जिससे पत्तियां सूखने और कीटों का जोखिम बढ़ सकता है।")
                stress_factors_ur.append(f"ہوا میں نمی ({h:.1f}%) کم ہے، جس سے خشکی اور کیڑوں کا حملہ ہو سکتا ہے۔")

            if r > r_max:
                stress_factors_en.append(f"High rainfall hazard ({r:.1f} mm); watch for field waterlogging and root rot.")
                stress_factors_hi.append(f"भारी बारिश का खतरा ({r:.1f} मिमी); खेत में जल निकासी की तुरंत व्यवस्था करें।")
                stress_factors_ur.append(f"زیادہ بارش کا خطرہ ({r:.1f} ملی میٹر)؛ کھیت سے پانی کی فوری نکاسی کا انتظام کریں۔")

            if w_spd > 25.0:
                stress_factors_en.append(f"High wind hazard ({w_spd:.1f} km/h); risk of lodging or branch breakage.")
                stress_factors_hi.append(f"तेज हवा का खतरा ({w_spd:.1f} किमी/घंटा); पौधों के गिरने का जोखिम।")
                stress_factors_ur.append(f"تیز ہوا کا خطرہ ({w_spd:.1f} کلومیٹر/گھنٹہ)؛ پودوں کے گرنے کا خدشہ۔")

            crop_display = CROP_URDU_NAMES.get(detected_crop, detected_crop) if is_urdu else (CROP_HINDI_NAMES.get(detected_crop, detected_crop) if is_hindi else detected_crop)
            has_hazards = (t < t_min or t > t_max or h > h_max or r > r_max or w_spd > 25.0)

            if is_urdu:
                status_header = "⚠️ **موسمی خطرات کا تفصیلی جائزہ:**" if has_hazards else "✅ **موسمی صورتحال: کوئی بڑا خطرہ نہیں ہے (موزوں حالت)**"
                ans = (
                    f"⛈️ **{crop_display} کے لیے موسمی جائزہ ({loc}):**\n\n"
                    f"{status_header}\n\n"
                    f"• **درجہ حرارت:** {t:.1f}°C (موزوں: {t_min}–{t_max}°C)\n"
                    f"• **ہوا میں نمی:** {h:.1f}% (موزوں: {h_min}–{h_max}%)\n"
                    f"• **بارش:** {r:.1f} mm • **ہوا کی رفتار:** {w_spd:.1f} km/h\n\n"
                    + "\n".join([f"• {s}" for s in stress_factors_ur])
                )
            elif is_hindi:
                status_header = "⚠️ **मौसम संबंधी खतरे एवं चेतावनी:**" if has_hazards else "✅ **मौसम की स्थिति: कोई गंभीर खतरा नहीं (अनुकूल स्थिति)**"
                ans = (
                    f"⛈️ **{crop_display} के लिए मौसम और खतरे का विश्लेषण ({loc}):**\n\n"
                    f"{status_header}\n\n"
                    f"• **तापमान:** {t:.1f}°C (अनुकूल सीमा: {t_min}–{t_max}°C)\n"
                    f"• **हवा में नमी:** {h:.1f}% (अनुकूल सीमा: {h_min}–{h_max}%)\n"
                    f"• **वर्षा:** {r:.1f} mm • **हवा की गति:** {w_spd:.1f} km/h\n\n"
                    + "\n".join([f"• {s}" for s in stress_factors_hi])
                )
            else:
                status_header = "⚠️ **Hazard Alert:** Specific environmental stress detected." if has_hazards else "✅ **Hazard Assessment:** Conditions are currently favorable with low immediate hazard."
                ans = (
                    f"⛈️ **Weather Hazard Assessment for {detected_crop} at {loc}:**\n\n"
                    f"{status_header}\n\n"
                    f"• **Temperature:** {t:.1f}°C (Optimal: {t_min}–{t_max}°C)\n"
                    f"• **Relative Humidity:** {h:.1f}% (Optimal: {h_min}–{h_max}%)\n"
                    f"• **Rainfall:** {r:.1f} mm • **Wind Speed:** {w_spd:.1f} km/h\n\n"
                    + "\n".join([f"• {s}" for s in stress_factors_en])
                )

            result = {
                "answer": ans,
                "confidence": 0.96,
                "matched_topic": f"{detected_crop.lower()}_weather_hazard_evaluation",
                "category": "weather_intelligence",
                "reasoning_summary": f"Evaluated dynamic weather hazards for {detected_crop}."
            }

        # =========================================================================
        # INTENT 3: Fertilizer / Khad / Urea / DAP / Nutrients
        # =========================================================================
        is_fertilizer_query = any(w in lower_raw for w in [
            "fertilizer", "fertilizers", "urea", "dap", "npk", "potash", "zinc", "nutrient",
            "khad", "urvarak", "खाद", "उर्वरक", "यूरिया", "डीएपी", "पोटाश", "जिंक",
            "کھاد", "یوریا", "ڈی اے پی", "پوٹاش"
        ])

        if not result and is_fertilizer_query:
            crop_key = detected_crop if (detected_crop and detected_crop in CROP_FERTILIZER_GUIDE) else "General"
            guide = CROP_FERTILIZER_GUIDE.get(crop_key, CROP_FERTILIZER_GUIDE["General"])
            
            if is_urdu:
                ans = guide.get("ur", guide["en"])
            elif is_hindi:
                ans = guide.get("hi", guide["en"])
            else:
                ans = guide.get("en", "")

            result = {
                "answer": ans,
                "confidence": 0.95,
                "matched_topic": f"{crop_key.lower()}_fertilizer_guidance",
                "category": "fertilizer_management",
                "reasoning_summary": f"Retrieved optimal nutrient management schedule for {crop_key}."
            }

        # =========================================================================
        # INTENT 4: Pesticide / Spraying Rules & Timings
        # =========================================================================
        is_spray_query = any(w in lower_raw for w in [
            "spray", "pesticide", "fungicide", "insecticide", "dawa", "chhidkaw", "chhidkao", "chhidkav",
            "कीटनाशक", "फफूंदनाशक", "छिड़काव", "दवा", "कीड़े मार", "فنگس کش", "اسپرے", "دوائی"
        ])

        if not result and is_spray_query:
            if is_urdu:
                ans = (
                    "🚿 **کیڑے مار اور فنگس کش دوا کے اسپرے کے محفوظ اصول:**\n\n"
                    "1) **صحیح وقت:** ہمیشہ صبح یا شام کے ٹھنڈے اور پرسکون وقت میں اسپرے کریں جب ہوا کی رفتار 12 کلومیٹر فی گھنٹہ سے کم ہو۔\n"
                    "2) **موسم کی جانچ:** اگر اگلے 4 تا 6 گھنٹوں میں بارش کا امکان ہو تو اسپرے فوری طور پر مؤخر کر دیں۔\n"
                    "3) **دوپہر کی دھوپ سے پرہیز:** دوپہر کی شدید گرمی (>32°C) میں اسپرے کرنے سے پتے جل جاتے ہیں۔\n"
                    "4) **حفاظتی تدابیر:** دوا کا درست تناسب رکھیں اور چہرے پر ماسک اور دستانے پہنیں۔"
                )
            elif is_hindi:
                ans = (
                    "🚿 **कीटनाशक एवं फफूंदनाशक छिड़काव के जरूरी नियम:**\n\n"
                    "1) **उचित समय:** छिड़काव हमेशा सुबह या शाम के शांत मौसम में करें जब हवा की गति 12 किमी/घंटे से कम हो।\n"
                    "2) **मौसम का पूर्वानुमान:** यदि अगले 4-6 घंटों में बारिश की संभावना हो तो छिड़काव टाल दें।\n"
                    "3) **दोपहर की धूप से बचाव:** दोपहर की तेज धूप (>32°C) में कभी भी स्प्रे न करें, इससे पत्तियां झुलस सकती हैं।\n"
                    "4) **सुरक्षा उपाय:** दवा का सही अनुपात रखें और मुंह पर मास्क व दस्तानों का उपयोग करें।"
                )
            else:
                ans = (
                    "🚿 **Safe Spraying Guidelines for Pesticides & Fungicides:**\n\n"
                    "1) **Optimal Timing:** Spray during calm morning or late afternoon hours (wind speed < 12 km/h).\n"
                    "2) **Rain Check:** Postpone spraying if rain is forecast within 4-6 hours.\n"
                    "3) **Avoid Peak Heat:** Never spray in scorching afternoon heat (>32°C) to prevent leaf scorching.\n"
                    "4) **Protective Gear:** Always maintain proper dilution and wear protective gear."
                )

            result = {
                "answer": ans,
                "confidence": 0.95,
                "matched_topic": "pesticide_spraying_rules",
                "category": "crop_spraying",
                "reasoning_summary": "Provided safe pesticide and bio-fungicide spraying rules."
            }

        # =========================================================================
        # INTENT 5: Crop Precautions / Care Checklist
        # =========================================================================
        is_precaution_query = any(w in lower_raw for w in [
            "precaution", "precautions", "care", "how to protect", "protect", "prevent", "remedy", "protection",
            "savdhani", "savdhaniya", "bachav", "upaay", "upchar", "suraksha", "ehtiyat", "tadabeer",
            "सावधानी", "सावधानियां", "बचाव", "उपाय", "उपचार", "सुरक्षा", "रोकथाम",
            "احتیاط", "تدابیر", "بچاؤ", "علاج", "حفاظت"
        ])

        if not result and detected_crop and is_precaution_query and detected_crop in self.knowledge_base:
            if is_urdu:
                crop_display = CROP_URDU_NAMES.get(detected_crop, detected_crop)
                precautions_ur = CROP_PRECAUTIONS_UR.get(detected_crop, [])
                ans = f"🌾 **{crop_display} کی فصل کے لیے اہم احتیاطی تدابیر:**\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(precautions_ur[:4])])
            elif is_hindi:
                crop_display = CROP_HINDI_NAMES.get(detected_crop, detected_crop)
                precautions_hi = CROP_PRECAUTIONS_HI.get(detected_crop, [])
                ans = f"🌾 **{crop_display} की फसल के लिए मुख्य सावधानियां:**\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(precautions_hi[:4])])
            else:
                precautions_en = self.knowledge_base[detected_crop].get("precautions", [])
                ans = f"🌾 **Key Precautions & Protection Guidelines for {detected_crop}:**\n\n" + "\n".join([f"{i+1}. {p}" for i, p in enumerate(precautions_en[:4])])

            result = {
                "answer": ans,
                "confidence": 0.95,
                "matched_topic": f"{detected_crop.lower()}_precautions",
                "category": "crop_precautions",
                "reasoning_summary": f"Retrieved specific crop precautions for {detected_crop}."
            }

        # =========================================================================
        # INTENT 6: Crop Agronomic Profile / Requirements (Explicit Inquiries Only)
        # =========================================================================
        is_profile_query = any(w in lower_raw for w in [
            "requirement", "requirements", "optimal condition", "optimal conditions", "ideal condition", "ideal conditions",
            "temperature range", "rainfall requirement", "profile", "about crop", "grow", "cultivation", "information", "details",
            "kheti ki jankari", "kaisa mausam chahiye", "tapman kitna", "zaroorat", "shartein", "paddhati",
            "معلومات", "کاشت کا طریقہ", "کتنا درجہ حرارت", "ضروریات", "پروفائل"
        ])

        if not result and detected_crop and is_profile_query and detected_crop in self.knowledge_base:
            crop_info = self.knowledge_base[detected_crop]
            t_min, t_max = crop_info.get("temp_optimal", (18.0, 28.0))
            h_min, h_max = crop_info.get("humidity_optimal", (50.0, 75.0))
            r_min, r_max = crop_info.get("rainfall_optimal", (40.0, 100.0))
            emoji = crop_info.get("emoji", "🌱")

            if is_urdu:
                crop_display = CROP_URDU_NAMES.get(detected_crop, detected_crop)
                ans = (
                    f"{emoji} **{crop_display} زراعت گائیڈ:**\n\n"
                    f"• **موزوں درجہ حرارت:** {t_min}°C – {t_max}°C\n"
                    f"• **ہوا میں نمی:** {h_min}% – {h_max}%\n"
                    f"• **سالانہ بارش / پانی:** {r_min} – {r_max} mm\n\n"
                    f"**اہم مشورہ:** مناسب نکاسی آب رکھیں اور کیڑوں کے حملے سے بروقت بچاؤ کریں۔"
                )
            elif is_hindi:
                crop_display = CROP_HINDI_NAMES.get(detected_crop, detected_crop)
                ans = (
                    f"{emoji} **{crop_display} कृषि मार्गदर्शिका:**\n\n"
                    f"• **अनुकूल तापमान:** {t_min}°C – {t_max}°C\n"
                    f"• **अनुकूल नमी:** {h_min}% – {h_max}%\n"
                    f"• **वार्षिक वर्षा:** {r_min} – {r_max} mm\n\n"
                    f"**मुख्य सलाह:** खेत में जल निकासी का उचित प्रबंध रखें और समय पर निराई-गुड़ाई करें।"
                )
            else:
                ans = (
                    f"{emoji} **{detected_crop} Agronomic Profile:**\n\n"
                    f"• **Optimal Temperature:** {t_min}°C – {t_max}°C\n"
                    f"• **Optimal Humidity:** {h_min}% – {h_max}%\n"
                    f"• **Rainfall Requirement:** {r_min} – {r_max} mm"
                )

            result = {
                "answer": ans,
                "confidence": 0.94,
                "matched_topic": f"{detected_crop.lower()}_agronomic_profile",
                "category": "agronomic_envelope",
                "reasoning_summary": f"Retrieved comprehensive agronomic profile for {detected_crop}."
            }

        # =========================================================================
        # INTENT 7: Cross-Lingual & Syntactically-Expanded TF-IDF Retrieval
        # =========================================================================
        if not result and cleaned_query.strip():
            # Build cross-lingual expanded query using learned syntactic alignments
            expanded_tokens = cleaned_query.split()
            if self.syntactic_model:
                h_to_u = self.syntactic_model.get("hindi_to_urdu_lexicon", {})
                u_to_h = self.syntactic_model.get("urdu_to_hindi_lexicon", {})
                for tok in cleaned_query.split():
                    if tok in h_to_u and h_to_u[tok]:
                        expanded_tokens.append(h_to_u[tok][0][0])
                    elif tok in u_to_h and u_to_h[tok]:
                        expanded_tokens.append(u_to_h[tok][0][0])

            search_query = " ".join(expanded_tokens)
            try:
                query_vec = self.vectorizer.transform([search_query])
                similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
                best_idx = int(np.argmax(similarities))
                best_score = float(similarities[best_idx])

                if best_score >= 0.05:
                    matched_entry = self.corpus_entries[best_idx]
                    confidence_pct = round(min(0.96, max(0.72, best_score * 1.8)), 2)
                    if is_urdu:
                        ans = matched_entry.get("answer_ur") or matched_entry.get("answer_en", "")
                    elif is_hindi:
                        ans = matched_entry.get("answer_hi") or matched_entry.get("answer_en", "")
                    else:
                        ans = matched_entry.get("answer_en", "")

                    result = {
                        "answer": ans,
                        "confidence": confidence_pct,
                        "matched_topic": matched_entry.get("topic", "general_qa"),
                        "category": "retrieval_qa",
                        "reasoning_summary": f"Matched topic '{matched_entry.get('topic')}' via syntactic TF-IDF similarity ({best_score:.3f})."
                    }
            except Exception:
                pass

        # =========================================================================
        # INTENT 8: Intelligent Domain Agricultural Advisory & Out-of-Domain Guard
        # =========================================================================
        if not result:
            agri_keywords = [
                "crop", "crops", "farm", "farming", "farmer", "plant", "plants", "field", "soil", "agriculture",
                "weather", "rain", "temperature", "humidity", "fertilizer", "pest", "disease", "yield", "water", "irrigate",
                "fasal", "kheti", "kisan", "paani", "mausam", "khad", "keeda", "rog", "bimari", "upaj", "paidavar", "zameen", "mitti",
                "फसल", "खेती", "किसान", "पानी", "मौसम", "खाद", "कीड़ा", "रोग", "बीमारी", "उपज", "पैदावार", "मिट्टी", "जमीन",
                "فصل", "کاشتکاری", "کسان", "پانی", "موسم", "کھاد", "کیڑا", "بیماری", "امراض", "پیداوار", "زمین", "مٹی", "آبپاشی"
            ]
            is_agri_related = detected_crop is not None or any(w in lower_raw for w in agri_keywords)

            crop_name = detected_crop or ("आपकी फसल" if is_hindi else ("آپ کی فصل" if is_urdu else "your crop"))

            if any(w in lower_raw for w in ["paidavar", "utpadan", "yield", "achhi fasal", "پیداوار", "پیداوار بڑھانے", "पैदावार", "उत्पादन"]):
                if is_urdu:
                    adv = (
                        "🌾 **فصل کی شاندار پیداوار حاصل کرنے کے 5 سنہری اصول:**\n\n"
                        "1) **تصدیق شدہ بیج اور بیج کا علاج:** بوائی سے قبل بیج کو فنگس کش دوا یا ٹرائیکوڈرما سے ٹریٹ کریں۔\n"
                        "2) **متوازن کھاد کا استعمال:** مٹی کے ٹیسٹ کی بنیاد پر ڈی اے پی، یوریا اور پوٹاش کی متوازن مقدار دیں۔\n"
                        "3) **نازک مراحل پر بروقت آبپاشی:** پھول آنے اور دانہ بننے کے وقت وتر کی کمی نہ ہونے دیں۔\n"
                        "4) **جڑی بوٹیوں کی تلفی:** فصل کے ابتدائی 30 دنوں میں جڑی بوٹیاں تلف کریں تاکہ کھاد اور پانی ضائع نہ ہو۔\n"
                        "5) **بروقت کیڑوں کی روک تھام:** رس چوسنے والے کیڑوں کے لیے شروع میں نیم کا تیل اسپرے کریں۔"
                    )
                elif is_hindi:
                    adv = (
                        "🌾 **फसल की बंपर पैदावार प्राप्त करने के 5 मुख्य वैज्ञानिक नियम:**\n\n"
                        "1) **प्रमाणित बीज एवं बीज शोधन:** बुवाई से पहले बीजों को ट्राइकोडर्मा या फफूंदनाशक से उपचारित करें।\n"
                        "2) **संतुलित खाद (NPK):** सिर्फ यूरिया पर निर्भर न रहें; डीएपी, पोटाश और जिंक का संतुलित प्रयोग करें।\n"
                        "3) **क्रांतिक अवस्थाओं पर सिंचाई:** कल्ले फूटते समय, फूल आने पर और दाना भरते समय नमी बनाए रखें।\n"
                        "4) **खरपतवार नियंत्रण:** बुवाई के 20-30 दिनों के भीतर निराई-गुड़ाई करके खरपतवार हटाएं।\n"
                        "5) **जैविक कीट रोकथाम:** सफेद मक्खी व थ्रिप्स के लिए नीम तेल (5ml/लीटर) का सुरक्षात्मक छिड़काव करें।"
                    )
                else:
                    adv = (
                        "🌾 **5 Golden Rules for Maximum Crop Yield:**\n\n"
                        "1) **Certified Seeds & Seed Treatment:** Treat seeds with bio-fungicides prior to sowing.\n"
                        "2) **Balanced Nutrition (NPK + Zinc):** Apply balanced basal DAP/Potash and split nitrogen.\n"
                        "3) **Critical Stage Irrigation:** Never let the field suffer water stress during flowering & grain-filling.\n"
                        "4) **Weed Control:** Clear weeds within the first 30 days of growth.\n"
                        "5) **Integrated Pest Management:** Apply preventive neem oil or bio-pesticides at first sign of infestation."
                    )
                result = {
                    "answer": adv,
                    "confidence": 0.88,
                    "matched_topic": "domain_advisory_synthesis",
                    "category": "agronomic_advisory",
                    "reasoning_summary": "Synthesized actionable agronomic yield advisory."
                }
            elif any(w in lower_raw for w in ["keeda", "keede", "pest", "insect", "sundi", "कीड़ा", "कीड़े", "सुंडी", "کیڑا", "کیڑے", "سنڈی"]):
                if is_urdu:
                    adv = (
                        "🐛 **فصلوں میں کیڑوں کے جامع انسداد کی گائیڈ:**\n\n"
                        "• **رس چوسنے والے کیڑے (سفید مکھی، تھرپس):** پیلے چپکنے والے کارڈز (Yellow Traps) لگائیں اور نیم کا تیل (5ml فی لیٹر) اسپرے کریں۔\n"
                        "• **تنے کی سنڈی اور فال آرمی ورم:** ابتدائی حالت میں ایما مائل بینزویٹ یا تجویز کردہ کیڑے مار دوا دیں۔\n"
                        "• **حفاظتی اقدام:** دوپہر کی شدید دھوپ میں اسپرے نہ کریں تاکہ دوا کا پورا اثر ہو۔"
                    )
                elif is_hindi:
                    adv = (
                        "🐛 **फसल सुरक्षा एवं कीट प्रबंधन मार्गदर्शिका:**\n\n"
                        "• **रस चूसक कीट (सफेद मक्खी, माहू, थ्रिप्स):** खेत में पीले चिपचिपे ट्रैप लगाएं और 5ml/लीटर नीम तेल का छिड़काव करें।\n"
                        "• **सुंडी एवं तना छेदक कीट:** प्रारंभिक प्रकोप पर इमामेक्टिन बेंजोएट या जैविक कीटनाशक का प्रयोग करें।\n"
                        "• **छिड़काव नियम:** हमेशा सुबह या शाम के शांत समय में स्प्रे करें।"
                    )
                else:
                    adv = (
                        "🐛 **Comprehensive Integrated Pest Management (IPM):**\n\n"
                        "• **Sap-Sucking Pests (Whitefly, Thrips, Aphids):** Deploy yellow sticky traps and spray neem oil (5ml/L).\n"
                        "• **Caterpillars & Borers:** Apply Emamectin Benzoate or recommended bio-pesticides.\n"
                        "• **Spraying Rule:** Apply early morning or evening for optimal residual efficacy."
                    )
                result = {
                    "answer": adv,
                    "confidence": 0.88,
                    "matched_topic": "domain_advisory_synthesis",
                    "category": "agronomic_advisory",
                    "reasoning_summary": "Synthesized actionable agronomic pest advisory."
                }
            elif is_agri_related:
                if is_urdu:
                    adv = (
                        f"🌱 **{crop_name} کی زراعت اور حفاظت کے بنیادی رہنما اصول:**\n\n"
                        f"1) **پانی اور وتر:** زمین میں مناسب وتر رکھیں اور پانی کھڑا نہ ہونے دیں،\n"
                        f"2) **امراض سے بچاؤ:** نمی زیادہ ہونے کی صورت میں فنگس کش دوا کا بروقت اسپرے کریں،\n"
                        f"3) **کھاد کا انتظام:** فاسفورس بوائی کے وقت اور نائٹروجن (یوریا) کو 2 تا 3 قسطوں میں دیں،\n"
                        f"4) **نگہداشت:** پودوں کا باقاعدگی سے معائنہ کریں تاکہ بیماریوں کا بر وقت تدارک ہو سکے۔"
                    )
                elif is_hindi:
                    adv = (
                        f"🌱 **{crop_name} की खेती एवं फसल सुरक्षा के प्रमुख दिशानिर्देश:**\n\n"
                        f"1) **सिंचाई व जल निकासी:** खेत में जलभराव न होने दें और उचित समय पर पानी लगाएं,\n"
                        f"2) **रोग एवं फफूंद से बचाव:** अधिक नमी में कॉपर फफूंदनाशक का सुरक्षात्मक छिड़काव करें,\n"
                        f"3) **संतुलित उर्वरक:** बुवाई के समय डीएपी/पोटाश और वृद्धि के समय यूरिया को किस्तों में दें,\n"
                        f"4) **नियमित निगरानी:** कीटों और पत्तियों के रंग की साप्ताहिक जांच करें।"
                    )
                else:
                    adv = (
                        f"🌱 **Core Agronomic Care & Best Practices for {crop_name}:**\n\n"
                        f"1) **Soil & Moisture:** Maintain adequate root-zone aeration and avoid prolonged standing water,\n"
                        f"2) **Disease Prevention:** Apply preventive bio-fungicide during humid microclimates,\n"
                        f"3) **Balanced Fertilization:** Apply basal DAP/Potash and top-dress Urea in split doses,\n"
                        f"4) **Scouting:** Inspect underside of leaves weekly for early pathogen detection."
                    )
                result = {
                    "answer": adv,
                    "confidence": 0.88,
                    "matched_topic": "domain_advisory_synthesis",
                    "category": "agronomic_advisory",
                    "reasoning_summary": "Synthesized actionable agronomic advisory."
                }
            else:
                if is_urdu:
                    adv = "میں CropGuard AI معاون ہوں، جو خصوصی طور پر زراعت، فصلوں اور موسم کے لیے تیار کیا گیا ہے۔ میرے پاس اس غیر زرعی سوال کے لیے کافی معلومات نہیں ہیں۔ براہ کرم فصل، بیماریوں، کھاد یا موسم کے بارے میں پوچھیں۔"
                elif is_hindi:
                    adv = "मैं CropGuard AI सहायक हूँ, जो विशेष रूप से कृषि, फसलों और मौसम के लिए तैयार किया गया है। मेरे पास इस गैर-कृषि प्रश्न के लिए पर्याप्त ज्ञान उपलब्ध नहीं है। कृपया फसल, रोग, खाद या मौसम के बारे में पूछें।"
                else:
                    adv = "I do not have sufficient agricultural knowledge to answer that query, as I am specialized strictly in crops, agriculture, plant diseases, fertilizers, and weather. Please ask an agriculture-related question."
                result = {
                    "answer": adv,
                    "confidence": 0.20,
                    "matched_topic": "out_of_domain",
                    "category": "system",
                    "reasoning_summary": "Query is outside agricultural and weather domain."
                }

        # Autonomous Continuous Self-Learning Ingestion
        try:
            self.self_learning_engine.record_interaction(
                query=question,
                response=result,
                active_crop=detected_crop,
                language=target_lang
            )
        except Exception:
            pass

        return result
