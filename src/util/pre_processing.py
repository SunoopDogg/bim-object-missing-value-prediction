import re
from itertools import permutations

# from sklearn.feature_extraction.text import TfidfVectorizer


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


def combine_two_tokens(tokens, delimiter):
    """
    토큰 리스트에서 두 개의 토큰을 주어진 구분자로 결합하는 함수

    Args:
        tokens (list): 토큰 리스트
        delimiter (str): 토큰을 결합할 구분자

    Returns:
        list: 두 개의 토큰이 결합된 새로운 토큰 리스트
    """
    combined_tokens = []
    for token1, token2 in permutations(tokens, 2):
        combined_tokens.append(token1 + delimiter + token2)
    return combined_tokens

# def get_tfidf_matrix(corpus):
#     # TF-IDF 행렬 생성
#     vectorizer = TfidfVectorizer()
#     return vectorizer.fit_transform(corpus)
