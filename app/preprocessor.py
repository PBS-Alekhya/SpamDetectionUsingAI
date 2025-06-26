import re
import emoji
from sklearn.base import BaseEstimator, TransformerMixin

# Hinglish Dictionary for  Normalization 
NORMALIZATION_DICT = {
    "hello": "hello", "hi": "hi", "namaste": "hello", "bhai": "bro", "dost": "friend",
    "jeeto": "win", "kamaye": "earn", "kamana": "earn", "paye": "get", "le": "take", "leja": "take",
    "leliya": "took", "click": "click", "bina": "without", "signup": "signup", "register": "register",
    "join": "join", "free": "free", "paise": "money", "paisa": "money", "offer": "offer",
    "fatafat": "quick", "abhi": "now", "turant": "immediately", "instant": "instant", "lo": "take",
    "mil": "get", "milta": "get", "milgaya": "got", "bhejo": "send", "bhej": "send", "pao": "get",
    "paoge": "get", "recharge": "recharge", "cashback": "cashback", "gift": "gift",
    "voucher": "voucher", "prize": "prize", "rewards": "rewards", "points": "points", "lakh": "lakh",
    "crore": "crore", "rupees": "rupees", "rs": "rupees", "rs.": "rupees", "inr": "rupees",
    "whatsapp": "whatsapp", "sms": "sms", "msg": "message", "message": "message", "link": "link",
    "app": "app", "mobile": "mobile", "number": "number", "phone": "phone", "kya": "what",
    "hai": "is", "hoga": "will", "kar": "do", "karo": "do", "karte": "doing", "ab": "now",
    "bahut": "very", "zyada": "very", "accha": "good", "achha": "good", "mast": "great",
    "bindaas": "cool", "best": "best", "urgent": "urgent", "important": "important", "last": "last",
    "chance": "chance", "limited": "limited", "alert": "alert", "verify": "verify", "otp": "otp",
    "account": "account", "block": "block", "blocked": "blocked", 'pls':'please'
}

# stopwords in Hindi and english
HINGLISH_STOP_WORDS = list(set([
    "hai", "ka", "ki", "ke", "ko", "se", "mein", "par", "tha", "thi", "nahi", "na", "bhi", "ye", "wo",
    "kya", "ho", "raha", "hoga", "kar", "karo", "hua", "ab", "jab", "sab", "tum", "aap", "hum", "unka",
    "suno", "unki", "tumki", "mera", "meri", "mere", "i", "me", "my", "myself", "we", "our", "ours",
    "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", 
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", 
    "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", 
    "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", 
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", 
    "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", 
    "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", 
    "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", 
    "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", 
    "nor", "not", "only", "own", "same", "so", "than", "too", "very", "can", "will", "just", 
    "don", "should", "now", "though"
]))

#  preprocessing transformer
class Preprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, norm_dict):
        self.norm_dict = norm_dict

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [self._clean_normalize_text(text) for text in X]

    def _clean_normalize_text(self, text):
        if not isinstance(text, str):
            text = str(text)
        text = text.lower()
        text = re.sub(r"http\S+|www\S+|https\S+", "<URL>", text)
        text = ''.join(c for c in text if c.isalnum() or c.isspace() or emoji.is_emoji(c) or c in ['<', '>'])
        text = re.sub(r'\b[a-zA-Z]*\d+[a-zA-Z]*\b', '', text)
        text = re.sub(r'\b\d+\b', '', text)
        text = re.sub(r'(.)\1{2,}', r'\1\1', text)
        text = re.sub(r'\s+', ' ', text).strip()
        words = text.split()
        normalized = [self.norm_dict.get(word, word) for word in words]
        filtered = [word for word in normalized if word not in HINGLISH_STOP_WORDS]
        if not filtered:
            return "<EMPTY>"
        return " ".join(filtered)
