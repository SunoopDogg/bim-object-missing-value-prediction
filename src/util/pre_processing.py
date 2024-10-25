import re
from sklearn.feature_extraction.text import TfidfVectorizer


def remove_except_parentheses(text):
    # 소괄호 내부를 제외하고 특수문자를 공백으로 치환
    return re.sub(r'(?<!\()[^\w\s()](?![^\(]*\))', ' ', text)


def get_token(text):
    # 소괄호 내부를 제외하고 토큰화
    protected_text = re.findall(r'\([^)]*\)', text)

    for i, match in enumerate(protected_text):
        text = text.replace(match, f'protected_text_{i}')

    tokens = text.split()

    for i, match in enumerate(protected_text):
        tokens = [token.replace(
            f'protected_text_{i}', match) for token in tokens]

    return tokens


def get_tfidf_matrix(corpus):
    # TF-IDF 행렬 생성
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(corpus)
