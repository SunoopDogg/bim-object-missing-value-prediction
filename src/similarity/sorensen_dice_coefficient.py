import pandas as pd

from util.pre_processing import get_tfidf_matrix, get_token, remove_except_parentheses


def get_sorensen_dice_coefficient(names, values):
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
                    value_tokens = set(get_token(
                        remove_except_parentheses(str(value))))
                    similarity[token].append(
                        2 * len(set([token]) & value_tokens) /
                        (len(set([token])) + len(value_tokens))
                    )

        df = pd.DataFrame.from_dict(
            similarity, orient='index', columns=values[idx])
        df = df.transpose()

        result.append(df)

    return result
