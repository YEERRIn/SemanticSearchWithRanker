import pandas as pd
from kiwipiepy import Kiwi

# Kiwi 형태소 분석기 초기화
kiwi = Kiwi()

# 데이터 로드
data = pd.read_csv("marketkurlyData.csv")

# 형태소 분석을 통해 유의미한 명사, 형용사 추출하는 함수
def extract_keywords(text):
    # 형태소 분석
    morphs = kiwi.analyze(text)
    
    # 명사와 형용사만 필터링하여 키워드 리스트 반환
    keywords = [m[0] for m in morphs[0][0] if m[1] in ['NNG', 'NNP', 'VA', 'VV']]  # NNG: 일반명사, NNP: 고유명사, VA: 형용사, VV: 동사
    return ' '.join(keywords)

# "상품정보" 컬럼에서 키워드 추출하여 새로운 "키워드" 컬럼 생성
data['키워드'] = data['상품정보'].apply(extract_keywords)

# 필요한 컬럼만 추출
final_data = data[['브랜드', '상품이름', 'URL', '가격', '리뷰수', '태깅', '키워드']]

# 결과 확인
final_data.head()

final_data.to_excel('kurly.xlsx', index=False)