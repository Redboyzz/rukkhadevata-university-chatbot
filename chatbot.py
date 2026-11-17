import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FAQ_PATH = PROJECT_ROOT / "data" / "faq.json"


def load_faqs():
    """Read the demonstration FAQ records from the project's JSON file."""
    with FAQ_PATH.open(encoding="utf-8") as faq_file:
        return json.load(faq_file)


def prepare_matcher(faqs):
    """Build TF-IDF vectors for each FAQ question and its example phrasings."""
    searchable_phrases = []
    faq_indices = []

    for index, faq in enumerate(faqs):
        phrases = [faq["question"], *faq.get("examples", [])]
        searchable_phrases.extend(phrases)
        faq_indices.extend([index] * len(phrases))

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    faq_vectors = vectorizer.fit_transform(searchable_phrases)
    return vectorizer, faq_vectors, faq_indices


def get_answer(question, faqs, matcher, threshold=0.18):
    """Return a relevant FAQ answer, or a friendly fallback if confidence is low."""
    normalized_question = question.lower()
    location_words = ("where", "location", "located", "address")
    place_words = ("university", "college", "campus")
    if any(word in normalized_question for word in location_words) and any(
        word in normalized_question for word in place_words
    ):
        location_faq = next(
            (faq for faq in faqs if faq["question"] == "Where is the university located?"),
            None,
        )
        if location_faq:
            return location_faq["answer"]

    vectorizer, faq_vectors, faq_indices = matcher
    question_vector = vectorizer.transform([question])
    scores = cosine_similarity(question_vector, faq_vectors).ravel()

    if not scores.size:
        return "I don't have that information yet. Please try a college-related question."

    best_phrase_index = int(scores.argmax())
    if scores[best_phrase_index] < threshold:
        return (
            "Sorry, I couldn't find a close match in the demo FAQs. "
            "Try asking about courses, admissions, documents, timings, scholarships, "
            "the library, examinations, or hostel facilities."
        )

    matched_faq_index = faq_indices[best_phrase_index]
    return faqs[matched_faq_index]["answer"]
