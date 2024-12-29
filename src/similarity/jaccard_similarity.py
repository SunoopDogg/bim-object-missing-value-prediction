import pandas as pd

from util.pre_processing import get_token, remove_except_parentheses


def jaccard_sim(A, B):
    return len(A & B) / len(A | B)


def get_jaccard_similarity(names, values):
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
                    value_tokens = get_token(
                        remove_except_parentheses(str(value)))
                    similarity[token].append(
                        jaccard_sim(set(value_tokens), set([token])))

        df = pd.DataFrame.from_dict(
            similarity, orient='index', columns=values[idx])
        df = df.transpose()

        result.append(df)

    return result


def get_jaccard_similarity_similarity(token, value):
    return jaccard_sim(set(get_token(remove_except_parentheses(str(value)))), set([token]))
