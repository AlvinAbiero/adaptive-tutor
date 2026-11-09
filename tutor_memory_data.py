_FIELDS = ("id", "kind", "topic", "text", "importance", "age_days")

_RAW = [
    ("M01", "goal", "python", "Wants to build a small web scraper in Python by December.", 5, 40),
    ("M02", "knowledge", "lists", "Understands that list indexing starts at zero.", 3, 35),
    ("M03", "knowledge", "lists", "Can use len() to count the items in a list.", 2, 35),
    ("M04", "misconception", "tuples", "Believes tuples can be changed after they are created, like lists.", 4, 30),
    ("M05", "preference", "teaching", "Learns best from real-life analogies rather than formal definitions.", 5, 28),
    ("M06", "knowledge", "recursion", "Understood recursion after the Russian dolls analogy.", 3, 27),
    ("M07", "misconception", "recursion", "Thinks a recursive function does not need a base case.", 4, 26),
    ("M08", "knowledge", "loops", "Can write a for loop over a list.", 3, 24),
    ("M09", "misconception", "loops", "Expects range(5) to give 1 to 5 and forgets that it starts at 0.", 3, 22),
    ("M10", "knowledge", "functions", "Knows how to define a function with parameters and call it.", 3, 20),
    ("M11", "misconception", "functions", "Believes a function must print its result instead of returning it.", 4, 19),
    ("M12", "preference", "sessions", "Prefers short sessions of about 20 minutes.", 3, 18),
    ("M13", "knowledge", "strings", "Can join and slice strings.", 2, 17),
    ("M14", "misconception", "strings", "Thinks strings can be modified in place.", 3, 16),
    ("M15", "goal", "career", "Hopes to use Python to move into data analysis work.", 4, 15),
    ("M16", "knowledge", "dicts", "Understands that dictionaries store values by key.", 3, 14),
    ("M17", "misconception", "dicts", "Expects dictionary keys to be kept in alphabetical order.", 2, 13),
    ("M18", "preference", "practice", "Likes to solve a small exercise right after each explanation.", 4, 12),
    ("M19", "knowledge", "errors", "Can read a simple traceback to find the failing line.", 3, 11),
    ("M20", "misconception", "errors", "Treats every error message as a sign that the whole program is wrong.", 2, 10),
    ("M21", "knowledge", "http", "Has seen how to fetch a web page with the requests library.", 3, 8),
    ("M22", "misconception", "http", "Believes a 404 status means the internet connection is down.", 3, 7),
    ("M23", "knowledge", "html", "Knows that HTML pages are made of nested tags.", 3, 6),
    ("M24", "goal", "scraper", "Wants to scrape product prices from one shopping site.", 4, 5),
    ("M25", "preference", "feedback", "Wants to be told directly when an answer is wrong, without softening.", 4, 4),
    ("M26", "knowledge", "conditionals", "Is comfortable with if, elif and else.", 3, 45),
    ("M27", "misconception", "conditionals", "Uses = instead of == when comparing values.", 3, 44),
    ("M28", "preference", "teaching", "Prefers formal definitions with precise terminology.", 3, 120),
]

MEMORIES = [dict(zip(_FIELDS, row)) for row in _RAW]

# relevant: memory ids that should come back. stale: an outdated memory that must rank below relevant[0].
QUERIES = [
    {"id": "Q01", "text": "What is the learner trying to achieve?", "relevant": ["M01", "M15", "M24"]},
    {"id": "Q02", "text": "How should I explain a new concept to this learner?", "relevant": ["M05", "M18"], "stale": ["M28"]},
    {"id": "Q03", "text": "Does the learner understand tuples?", "relevant": ["M04"]},
    {"id": "Q04", "text": "Is the learner ready to write a recursive function?", "relevant": ["M06", "M07"]},
    {"id": "Q05", "text": "my loop printed 0 to 4 but I expected 1 to 5", "relevant": ["M09"]},
    {"id": "Q06", "text": "Can the learner return values from functions?", "relevant": ["M10", "M11"]},
    {"id": "Q07", "text": "What does the learner know about fetching web pages?", "relevant": ["M21", "M22"]},
    {"id": "Q08", "text": "How long should the next session be?", "relevant": ["M12"]},
    {"id": "Q09", "text": "How blunt should feedback be?", "relevant": ["M25"]},
    {"id": "Q10", "text": "my if statement says invalid syntax when I compare two numbers", "relevant": ["M27"]},
    {"id": "Q11", "text": "What does the learner believe about changing strings?", "relevant": ["M14"]},
    {"id": "Q12", "text": "Can the learner read error messages?", "relevant": ["M19", "M20"]},
]