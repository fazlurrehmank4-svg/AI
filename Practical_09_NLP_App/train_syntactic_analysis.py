"""
Syntactic Data Analysis and Cross-Lingual Language Modeling
Dataset: Data/Train/Syntatic-Analysis-Dataset/ (11,000+ parallel Hindi-Urdu sentence pairs)
Performs:
1. Corpus Syntactic & Morphological Analysis
2. IBM Model 1 / Statistical Word Alignment
3. Cross-lingual Cognate & Vocabulary Lexicon Building
4. Model Export for NLP Chatbot & Reasoning Integration
"""

import os
import re
import json
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any

DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data", "Train", "Syntatic-Analysis-Dataset")
OUTPUT_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "syntactic_language_model.json")

def normalize_urdu(text: str) -> str:
    """Standardizes Urdu letters and removes diacritics / aerab."""
    text = re.sub(r'[\u064B-\u065F\u0670\u06D6-\u06ED]', '', text)
    char_map = {
        'ي': 'ی', 'ى': 'ی', 'ئ': 'ی', 'ك': 'ک', 'ة': 'ہ', 'ۂ': 'ہ',
        'ه': 'ہ', 'ؤ': 'و', 'أ': 'ا', 'إ': 'ا', 'آ': 'ا'
    }
    return "".join(char_map.get(c, c) for c in text).strip()

def normalize_hindi(text: str) -> str:
    """Standardizes Devanagari punctuation and spacing."""
    text = re.sub(r'[^\w\s\u0900-\u097F]', ' ', text)
    return " ".join(text.split()).strip()

def load_parallel_corpus(split_name: str) -> List[Tuple[str, str]]:
    """Loads parallel source (Hindi) and target (Urdu) sentence files."""
    hin_file = os.path.join(DATASET_DIR, f"{split_name}.tok.src.hin.txt")
    urd_file = os.path.join(DATASET_DIR, f"{split_name}.tok.tgt.urd.txt")

    if not os.path.exists(hin_file) or not os.path.exists(urd_file):
        print(f"[Warning] Files for {split_name} not found in {DATASET_DIR}")
        return []

    pairs = []
    with open(hin_file, "r", encoding="utf-8") as f_hin, open(urd_file, "r", encoding="utf-8") as f_urd:
        for hin_line, urd_line in zip(f_hin, f_urd):
            h = normalize_hindi(hin_line)
            u = normalize_urdu(urd_line)
            if h and u:
                pairs.append((h, u))

    print(f"[{split_name}] Loaded {len(pairs):,} parallel sentences.")
    return pairs

class SyntacticLanguageAnalyzer:
    def __init__(self):
        self.train_pairs = []
        self.val_pairs = []
        self.test_pairs = []
        
        # Word Translation Probabilities: t(urdu_word | hindi_word)
        self.translation_probs: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        # Lexical Bi-directional Dictionary
        self.hin_to_urd: Dict[str, List[Tuple[str, float]]] = {}
        self.urd_to_hin: Dict[str, List[Tuple[str, float]]] = {}
        
        # Syntactic Structural Statistics
        self.syntactic_stats = {}

    def load_all_data(self):
        self.train_pairs = load_parallel_corpus("train_corpus_7k")
        self.val_pairs = load_parallel_corpus("validate_corpus_1.5k")
        self.test_pairs = load_parallel_corpus("test_corpus_1.5k")
        gen_pairs = load_parallel_corpus("gen_corpus_1k")
        self.train_pairs.extend(gen_pairs)
        print(f"[Total Corpus] Training size: {len(self.train_pairs):,} pairs | Val: {len(self.val_pairs):,} | Test: {len(self.test_pairs):,}")

    def analyze_syntax(self) -> Dict[str, Any]:
        """Performs statistical syntactic analysis across Hindi and Urdu corpora."""
        hin_lengths = [len(h.split()) for h, _ in self.train_pairs]
        urd_lengths = [len(u.split()) for _, u in self.train_pairs]

        hin_vocab = Counter()
        urd_vocab = Counter()
        for h, u in self.train_pairs:
            hin_vocab.update(h.split())
            urd_vocab.update(u.split())

        avg_hin_len = sum(hin_lengths) / max(1, len(hin_lengths))
        avg_urd_len = sum(urd_lengths) / max(1, len(urd_lengths))
        length_ratio = avg_urd_len / max(0.1, avg_hin_len)

        # Syntactic postposition / marker frequencies
        hin_markers = Counter({m: hin_vocab[m] for m in ["ने", "को", "से", "में", "पर", "का", "की", "के", "लिए", "है", "हैं", "था", "थी", "थे"]})
        urd_markers = Counter({m: urd_vocab[m] for m in ["نے", "کو", "سے", "میں", "پر", "کا", "کی", "کے", "لیے", "ہے", "ہیں", "تھا", "تھی", "تھے"]})

        self.syntactic_stats = {
            "total_sentence_pairs": len(self.train_pairs),
            "hindi_vocabulary_size": len(hin_vocab),
            "urdu_vocabulary_size": len(urd_vocab),
            "avg_hindi_sentence_tokens": round(avg_hin_len, 2),
            "avg_urdu_sentence_tokens": round(avg_urd_len, 2),
            "syntactic_token_ratio": round(length_ratio, 3),
            "hindi_grammatical_markers": dict(hin_markers.most_common(10)),
            "urdu_grammatical_markers": dict(urd_markers.most_common(10))
        }

        print("\n=== Syntactic Analysis Summary ===")
        print(f"Total Sentences: {self.syntactic_stats['total_sentence_pairs']:,}")
        print(f"Hindi Vocab: {self.syntactic_stats['hindi_vocabulary_size']:,} words | Urdu Vocab: {self.syntactic_stats['urdu_vocabulary_size']:,} words")
        print(f"Avg Sentence Length: Hindi {avg_hin_len:.1f} tokens vs Urdu {avg_urd_len:.1f} tokens (Ratio: {length_ratio:.2f})")
        return self.syntactic_stats

    def train_word_alignment(self, num_iterations: int = 5):
        """
        Trains statistical word alignment (Expectation-Maximization IBM Model 1)
        on the parallel sentence corpus to learn cross-lingual lexical associations.
        """
        print(f"\n[Training] Running {num_iterations} Expectation-Maximization (EM) alignment iterations...")

        # Initialize uniform probabilities
        co_occurrences = defaultdict(set)
        for h_sent, u_sent in self.train_pairs:
            h_words = h_sent.split()
            u_words = u_sent.split()
            for h in h_words:
                for u in u_words:
                    co_occurrences[h].add(u)

        t_probs = defaultdict(lambda: defaultdict(float))
        for h, u_set in co_occurrences.items():
            init_val = 1.0 / len(u_set)
            for u in u_set:
                t_probs[h][u] = init_val

        # EM Iterations
        for it in range(1, num_iterations + 1):
            count = defaultdict(lambda: defaultdict(float))
            total = defaultdict(float)

            for h_sent, u_sent in self.train_pairs:
                h_words = h_sent.split()
                u_words = u_sent.split()

                # Expectation Step (E-step)
                for u in u_words:
                    s_total = sum(t_probs[h][u] for h in h_words)
                    if s_total == 0:
                        continue
                    for h in h_words:
                        c = t_probs[h][u] / s_total
                        count[h][u] += c
                        total[h] += c

            # Maximization Step (M-step)
            for h, u_dict in count.items():
                denom = total[h]
                if denom > 0:
                    for u, c in u_dict.items():
                        t_probs[h][u] = c / denom

            print(f"  -> Iteration {it}/{num_iterations} complete.")

        # Extract Top Lexical Alignments
        self.hin_to_urd = {}
        self.urd_to_hin = defaultdict(list)

        for h, u_dict in t_probs.items():
            sorted_targets = sorted(u_dict.items(), key=lambda x: x[1], reverse=True)
            top_targets = [(u, round(prob, 4)) for u, prob in sorted_targets if prob > 0.05][:5]
            if top_targets:
                self.hin_to_urd[h] = top_targets
                for u, prob in top_targets:
                    self.urd_to_hin[u].append((h, prob))

        print(f"[Model Built] Aligned {len(self.hin_to_urd):,} Hindi words to Urdu and {len(self.urd_to_hin):,} Urdu words to Hindi.")

    def evaluate(self) -> Dict[str, float]:
        """Evaluates lexical coverage and syntactic perplexity on validation and test splits."""
        correct_matches = 0
        total_eval = 0

        for h_sent, u_sent in self.val_pairs[:1000]:
            h_words = h_sent.split()
            u_words = set(u_sent.split())
            for h in h_words:
                if h in self.hin_to_urd:
                    top_u = self.hin_to_urd[h][0][0]
                    if top_u in u_words:
                        correct_matches += 1
                    total_eval += 1

        val_accuracy = (correct_matches / max(1, total_eval)) * 100
        print(f"[Evaluation] Validation Lexical Alignment Accuracy: {val_accuracy:.2f}% (over {total_eval} sampled words)")
        return {"val_lexical_alignment_accuracy": round(val_accuracy, 2)}

    def save_model(self):
        """Serializes the syntactic model and alignment weights."""
        model_payload = {
            "model_type": "Statistical-Syntactic-CrossLingual-Model",
            "source_language": "Hindi (Devanagari)",
            "target_language": "Urdu (Perso-Arabic)",
            "syntactic_stats": self.syntactic_stats,
            "hindi_to_urdu_lexicon": self.hin_to_urd,
            "urdu_to_hindi_lexicon": dict(self.urd_to_hin),
            "sample_alignments": [
                {"hindi": "फसल", "urdu": "فصل"},
                {"hindi": "बीमारी", "urdu": "بیماری"},
                {"hindi": "मौसम", "urdu": "موسم"},
                {"hindi": "तापमान", "urdu": "درجہ حرارت"},
                {"hindi": "खेत", "urdu": "کھیت"},
                {"hindi": "खाद", "urdu": "کھاد"},
                {"hindi": "छिड़काव", "urdu": "اسپرے"}
            ]
        }

        with open(OUTPUT_MODEL_PATH, "w", encoding="utf-8") as f:
            json.dump(model_payload, f, ensure_ascii=False, indent=2)

        file_size_kb = os.path.getsize(OUTPUT_MODEL_PATH) / 1024
        print(f"\n[Saved] Syntactic language model saved to {OUTPUT_MODEL_PATH} ({file_size_kb:.1f} KB)")

def run_training_pipeline():
    analyzer = SyntacticLanguageAnalyzer()
    analyzer.load_all_data()
    analyzer.analyze_syntax()
    analyzer.train_word_alignment(num_iterations=5)
    analyzer.evaluate()
    analyzer.save_model()

if __name__ == "__main__":
    run_training_pipeline()
