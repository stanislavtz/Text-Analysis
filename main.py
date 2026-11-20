import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer


def find_word_occurrence(text, word):
    """ Finds how many times 'word' appears in 'text' """
    word_pattern = rf"\b{word}\b"
    matches = re.findall(word_pattern, text, re.IGNORECASE)
    return len(matches)


def get_words(text):
    """ Returns a list of tuples (word, count) of all words and their counts in 'text' """
    words = {}
    word_pattern = r"[a-z]+(?:'[a-z]+)?"
    words_matches = re.findall(word_pattern, text.lower())

    for word in words_matches:
        if word not in words:
            words[word] = 0
        words[word] += 1

    sorted_words = sorted(sorted(words.items()),
                          key=lambda k: k[1],
                          reverse=True)
    # for key, value in sorted_words:
    #     print(f"{key} => {value}")

    return sorted_words


# Read text file content and decode text content in utf-8
with open("miracle_in_the_andes.txt", "r+b") as file:
    content = file.read()

text = content.decode("utf-8", errors="ignore")

# Finds how many chapters are in the text
chapters_pattern = r"chapter\s+\d+"
matches = re.findall(chapters_pattern, text, re.IGNORECASE)
print(f"Chapters number is: {len(matches)}")

# Two different patterns to count sentences that contains 'love' word.
sentence_pattern1 = r'[^.!?]*\blove\b[^.!?]*[.!?]'
matches1 = re.findall(sentence_pattern1, text)
print(f"Number of sentences that contains 'love' is: {len(matches1)}")

sentence_pattern2 = r'[A-Z]{1}[^.]*[^a-zA-Z]+love[^a-zA-Z]+[^.]*.'
matches2 = re.findall(sentence_pattern2, text)
print(f"Number of sentences that contains 'love' is: {len(matches2)}")

# Count how many times every single word appears in the text
words_count = len(get_words(text))
print(f"We found {words_count} different words.")

# Counts how many paragraphs contain word 'love'
paragraph_pattern = r"^(?=(?:[^\n]+\n)*?[^\n]*\blove\b)[^\n]+(?:\n[^\n]+)*"
love_paragraphs = re.findall(paragraph_pattern, text, re.MULTILINE | re.IGNORECASE)
print("Love paragraphs:", len(love_paragraphs))

# Prints names of all chapters
chapters_titles_pattern =  r"^Chapter\s+\d+\n+([^\n]+)$"
title_matches = re.findall(chapters_titles_pattern, text, re.MULTILINE)
print(title_matches)

# Finds how many times given word appear in the text
word = "love"
word_count = find_word_occurrence(text, word)

if word_count > 0:
    print(f"The {word} has appear {word_count} times.")
else:
    print(f"The {word} not appear.")

# Filters out stop words from the list that holds tuples (word, count)
stop_words = stopwords.words('english')
text_words = get_words(text)

filtered_words = [word for word in text_words if word[0] not in stop_words]
print(filtered_words[:5])

# Sentimen analysis. Finds which chapter is most positive in the text
sentiment = SentimentIntensityAnalyzer()
chapter_split_pattern = r"^(?=Chapter\s+\d+\n)"
chapters = re.split(chapter_split_pattern, text, flags=re.MULTILINE)

chapters = [c for c in chapters if c]

positive = -1
most_positive = ""
for chapter in chapters:
    s = sentiment.polarity_scores(chapter)
    current_positive = s["pos"]
    if current_positive > positive:
        positive = current_positive
        most_positive = chapter

chapter_name_pattern = r"^Chapter\s+\d+\n+([^\n]+)$"
chapter_name_obj = re.findall(chapter_name_pattern, most_positive, re.MULTILINE)
chapter_name = chapter_name_obj[0]

print(f"The most positive chapter is '{chapter_name.strip()}'.")