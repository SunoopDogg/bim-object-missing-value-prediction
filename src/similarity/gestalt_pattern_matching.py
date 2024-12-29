import difflib
import pandas as pd

from util.pre_processing import get_token, remove_except_parentheses


def get_gestalt_pattern_matching(names, values):
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
                    similarity[token].append(difflib.SequenceMatcher(
                        None, str(value), str(token)).ratio())

        df = pd.DataFrame.from_dict(
            similarity, orient='index', columns=values[idx])
        df = df.transpose()

        result.append(df)

    return result


def get_gestalt_pattern_matching_similarity(token, value):
    return difflib.SequenceMatcher(None, str(value), str(token)).ratio()
