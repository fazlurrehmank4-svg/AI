"""
Practical 09: Self-Learning Knowledge & Feedback Engine for CropGuard AI
Enables online continuous learning, query intent clustering, feedback ingestion,
and incremental TF-IDF knowledge base expansion (Zero external LLMs).
"""

import os
import re
import json
import time
from typing import Dict, List, Any, Optional, Tuple
import numpy as np

LEARNED_KB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Data", "knowledge_base", "learned_knowledge.json"
)

class SelfLearningEngine:
    """
    Self-improving agricultural intelligence engine that persists, clusters,
    and indexes new query patterns, user feedback, and domain facts.
    """

    def __init__(self, storage_path: str = LEARNED_KB_PATH):
        self.storage_path = storage_path
        self.learned_store: Dict[str, Any] = {
            "version": "1.0",
            "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_queries_processed": 0,
            "learned_entries": [],
            "query_feedback": [],
            "custom_synonyms": {}
        }
        self._load_store()

    def _load_store(self) -> None:
        """Loads learned knowledge from disk if present."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.learned_store.update(data)
            except Exception as e:
                print(f"[SelfLearningEngine] Warning loading store: {e}")

    def _save_store(self) -> None:
        """Saves current learned knowledge to disk."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.learned_store["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.learned_store, f, ensure_ascii=False, indent=2)

    def record_interaction(
        self,
        query: str,
        response: Dict[str, Any],
        active_crop: Optional[str] = None,
        language: str = "en"
    ) -> None:
        """
        Records an interaction and autonomously reinforces high-confidence patterns.
        """
        self.learned_store["total_queries_processed"] += 1
        conf = response.get("confidence", 0.0)
        topic = response.get("matched_topic", "unknown")

        # Auto-learn: If user query was answered with high confidence (> 0.85),
        # add query to known templates for that topic if not already present
        if conf >= 0.85 and topic not in ["empty_query", "fallback_help"]:
            self._auto_reinforce_topic(query, topic, response.get("answer", ""), active_crop, language)

        # Periodic auto-save every 5 interactions
        if self.learned_store["total_queries_processed"] % 5 == 0:
            self._save_store()

    def _auto_reinforce_topic(
        self,
        query: str,
        topic: str,
        answer: str,
        crop: Optional[str],
        language: str
    ) -> None:
        """Adds novel query phrasing to the learned knowledge index."""
        cleaned_q = query.strip().lower()
        if len(cleaned_q) < 4:
            return

        entries = self.learned_store.get("learned_entries", [])
        # Check if topic entry exists
        found = False
        for entry in entries:
            if entry.get("topic") == topic:
                templates = entry.get("query_templates", [])
                if cleaned_q not in [t.lower() for t in templates]:
                    templates.append(query.strip())
                    entry["query_templates"] = templates
                    entry["sample_count"] = entry.get("sample_count", 1) + 1
                found = True
                break

        if not found:
            entries.append({
                "topic": topic,
                "crop": crop or "General",
                "language": language,
                "query_templates": [query.strip()],
                "answer_en": answer if language == "en" else "",
                "answer_hi": answer if language == "hi" else "",
                "answer_ur": answer if language == "ur" else "",
                "sample_count": 1,
                "learned_at": time.strftime("%Y-%m-%d %H:%M:%S")
            })

        self.learned_store["learned_entries"] = entries

    def ingest_feedback(
        self,
        query: str,
        rating: int, # +1 (helpful) or -1 (unhelpful)
        corrected_answer: Optional[str] = None,
        suggested_topic: Optional[str] = None,
        crop: Optional[str] = None,
        language: str = "auto"
    ) -> Dict[str, Any]:
        """
        Ingests direct user or teacher feedback to immediately adapt future responses.
        """
        feedback_entry = {
            "query": query,
            "rating": rating,
            "corrected_answer": corrected_answer,
            "suggested_topic": suggested_topic,
            "crop": crop,
            "language": language,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.learned_store.setdefault("query_feedback", []).append(feedback_entry)

        # If positive correction provided, create a primary learned entry
        if corrected_answer and corrected_answer.strip():
            topic_name = suggested_topic or f"custom_{int(time.time())}"
            self.learned_store.setdefault("learned_entries", []).append({
                "topic": topic_name,
                "crop": crop or "General",
                "language": language,
                "query_templates": [query.strip()],
                "answer_en": corrected_answer if language == "en" else "",
                "answer_hi": corrected_answer if language == "hi" else "",
                "answer_ur": corrected_answer if language == "ur" else "",
                "sample_count": 5, # boosted weight for explicit human feedback
                "learned_at": time.strftime("%Y-%m-%d %H:%M:%S")
            })

        self._save_store()
        return {
            "status": "success",
            "message": "Feedback ingested and knowledge base updated dynamically.",
            "total_learned_entries": len(self.learned_store.get("learned_entries", []))
        }

    def get_learned_corpus(self) -> List[Dict[str, Any]]:
        """Returns all dynamically learned entries formatted for TF-IDF training."""
        return self.learned_store.get("learned_entries", [])

    def get_learning_stats(self) -> Dict[str, Any]:
        """Returns telemetry and learning stats."""
        return {
            "total_queries_processed": self.learned_store.get("total_queries_processed", 0),
            "total_learned_entries": len(self.learned_store.get("learned_entries", [])),
            "total_feedbacks_received": len(self.learned_store.get("query_feedback", [])),
            "last_updated": self.learned_store.get("last_updated", "N/A")
        }
