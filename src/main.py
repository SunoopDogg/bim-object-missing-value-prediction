from util.pre_processing import combine_two_tokens, get_token, remove_except_parentheses

from similarity.gestalt_pattern_matching import get_gestalt_pattern_matching_similarity
from similarity.jaccard_similarity import get_jaccard_similarity_similarity

from db.mongo_insert import insert_json_to_collection
from db.mongo_select import find_all_documents

# 사용할 파일 이름 설정
FILE_NAME = '속성테이블(프로세스)'

DELIMITER_LIST = ['_', ' ', '-']


def get_similarity_each_values(tokens, bim_object, func):
    """
    BIM 객체의 각 값에 대해 유사도를 계산하는 함수

    Args:
        tokens (list): 토큰 리스트
        bim_object (dict): BIM 객체
        func (function): 유사도 계산 함수

    Returns:
        dict: 유사도 결과
    """
    result = {}

    for k, v in bim_object.items():
        if isinstance(v, dict):
            # 값이 딕셔너리인 경우 재귀 호출
            result[k] = get_similarity_each_values(tokens, v, func)
        else:
            similarity = {}

            if v == '':
                continue
            else:
                for token in tokens:
                    similarity[token] = func(token, v)

            result[k] = {str(v): similarity}

    return result


if __name__ == '__main__':
    # 'bim' 데이터베이스에서 모든 문서 조회
    bim_objects = find_all_documents('bim', FILE_NAME)

    for bim_object in bim_objects[:1]:
        # BIM 객체의 이름 가져오기
        object_name = bim_object['Name']

        # 특정 키를 제외한 새로운 BIM 객체 생성
        new_bim_object = {k: v for k, v in bim_object.items(
        ) if k not in ['_id', 'Name', 'ObjectType', 'GlobalID', 'PredefinedType']}

        # 객체 이름에서 토큰 추출
        tokens = get_token(remove_except_parentheses(object_name))
        # 토큰 조합하여 확장
        extended_tokens = tokens.copy()
        for delimiter in DELIMITER_LIST:
            extended_tokens.extend(combine_two_tokens(tokens, delimiter))

        # 유사도 계산
        similarity_object = get_similarity_each_values(
            extended_tokens, new_bim_object, get_jaccard_similarity_similarity)

        # 결과 객체 생성
        result_object = {}
        result_object['Name'] = object_name
        # result_object['Method'] = 'Gestalt Pattern Matching'
        result_object['Method'] = 'Jaccard Similarity'
        result_object.update(similarity_object)

        # 결과를 'bim_similarity' 컬렉션에 삽입
        insert_json_to_collection('bim_similarity', FILE_NAME, [result_object])
