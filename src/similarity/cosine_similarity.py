import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm

from util.pre_processing import get_token, remove_except_parentheses


def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))


def make_matrix(feats, words):
    matrix = []
    for feat in feats:
        freq = sum([1 for word in words if word in feat])
        matrix.append(freq)
    return matrix


def get_cosine_similarity(names, values):
    result = []
    for idx, name in enumerate(names):
        tokens = get_token(remove_except_parentheses(name))

        similarity = {}
        for token in tokens:
            if similarity.get(token) is None:
                similarity[token] = []
            else:
                continue

            for value in values[idx]:
                if pd.isna(value):
                    similarity[token].append(0)
                else:
                    value_tokens = get_token(str(value))
                    set_tokens = set(value_tokens + tokens)
                    A = make_matrix(set_tokens, value_tokens)
                    B = make_matrix(set_tokens, token)
                    similarity[token].append(cos_sim(A, B).item())

        df = pd.DataFrame.from_dict(
            similarity, orient='index', columns=values[idx])
        df = df.transpose()

        result.append(df)

    return result
