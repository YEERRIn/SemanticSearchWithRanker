# SemanticSearchWithRanker
<b> 개요 </b><br>
이 프로젝트는 [마켓컬리](https://www.kurly.com/)의 상품 데이터를 입력 받아 TF-IDF, BM25, BGE-M3 + FAISS 3가지의 검색 모델을 혼합하는 구현이다. 구현한 하이브리드 서치를 기반으로 점수 반환를 반환해 사용자가 입력한 쿼리와 가장 유사한 상품을 찾는 검색엔진을 제공한다.
<br>
<br>
프로젝트 진행 날짜: 2024.11 ~ 2025.02<br>

## 문제정의
 전통적인 검색 엔진은 주로 키워드에 의존하기에 사람들이 검색을 할 때 같은 것을 표현하기 위해 서로 다른 단어나 구문을 사용하는 경우, 불완전하거나 관련성이 없는 검색 결과를 초래하기도 한다. 시맨틱 검색은 단순히 입력한 단어들의 의미뿐만 아니라, 그 뒤에 숨겨진 의도까지 파악할 수 있다. 하지만 시맨틱 검색만을 사용했을 경우 사용자가 모호하거나 불완전한 질의와 같이 명확히 표현하지 않은 경우 관련성이 낮거나 부정확한 결과를 반환할 가능성이 있다.<br>
 위와 같은 문제점을 해결하기 위해 하이브리드 서치를 통해 키워드 검색의 정확성과 시맨틱 검색의 문맥 이해를 동시에 활용하면서, 각각의 한계를 극복하여 더 정확하고 관련성 높은 검색 결과를 제공할 수 있다. <br>
 또한 이용자들은 기존의 매스미디어에 공신력을 부여했던 것처럼, 검색엔진이 제시하는 정보의 순위를 신뢰한다. 랭커는 초기 검색 결과의 순서를 최적화하는 필수적인 도구로, 사용자에게 표시되는 최종 결과의 정확도와 관련성을 향상 시킬 수 있다.

## 프레임워크
<img width="766" alt="KakaoTalk_20250315_192827759" src="https://github.com/user-attachments/assets/8aad1ab1-84e7-4b15-956e-b23e7656ba83" />

<br>

## 개념정리
## Embedding 
- <b> 텍스트 데이터를  숫자로 이루어진 벡터로 변환하는 과정</b> <br>
- 임베딩을 통해 생성된 벡터 표현을 기반으로 텍스트 데이터를 벡터 공간 내에서 수학적으로 다룸 → 텍스트 간의 유사성 계산 및 텍스트 데이터를 기반으로 하는 다양한 머신러닝 및 자연어 처리 작업 수행 <br>
- 임베딩 과정을 텍스트의 의미적인 정보를 보존하도록 설계되며, 벡터 공간에서 가까이 위치한 텍스트 조각들은 의미적으로 유사한 것으로 간주됨 

### BGE-M3
- 중국 AI 연구소인 BAAI에서 만든 Embedding Model
- Information Retrieval에서 사용되는 Embedding Model의 한계를 극복하기 위해 다음과 같은 특징을 가짐<br>
  - <b>Multi-Linguality</b> : 100개 이상의 언어 지원
  - <b>Multi-Functionality</b>: 3가지 Retrieval 방식 제공
  - <b>Multi-Granularity</b>: 짧고, 긴 문장(최대 8192 토큰)에서도 잘 동작 <br>
- 실제 실험 결과 한국어에서도 좋은 성능을 보임

## Vector Database 
- 벡터를 고차원 포인트포 저장하고 검색하는 기능을 제공하는 데이터베이스
  - n차원 공간에서 가장 가까운 이웃을 효율적이고 빠르게 조회할 수 있는 추가적 기능을 제공
    - 일반적으로 K-NN 인덱스로 구동되며 HNSW 및 IVF와 같은 알고리즘으로 구축
- 임베딩 모델을 통해 생성된 벡터를 벡터 데이터베이스에 인덱싱함으로서 데이터베이스 내에서 인접한 벡터를 쿼리, 유사한 데이터를 반환

### FAISS
- Facebook에서 개발한 고차원 벡터 계산용 라이브러리. 밀집 벡터의 유사도 검색과 클러스터링에 사용

<b> FAISS 선택 이유 </b>
- NNS(Nearest Neighbor Search) 기능 제공 외에도 GPU 지원을 통한 빠른 데이터 처리 능력과 다양한 인덱스를 지원하여 데이터 크기 및 요구에 맞는 최적화된 검색을 제공한다는 점에서 FAISS 선택

<b>FAISS Vector Index</b> <br>
- IndexFlatL2 ✅
  - 모든 벡터를 순차적으로 비교하는 단순한 인덱스
  - L2 거리를 이용하여 벡터 간의 거리 계산
- IndexIVFFlat
  - 인버스 파일 시스템(IVF)와 Flat 구조를 결합한 인덱스
  - 벡터를 여러 클러스터로 나누고, 각 클러스터 내에서 검색을 수행
- IndexIvFPQ
  - VF와 제품 양자화를 결합한 인덱스
  - 벡터를 압축하여 메모리 사용량을 줄이고, 검색 속도를 높이기 위해 IVF 구조 사용
- IndexHNSW
  - 계층적 탐색이 가능한 소규모 세계(HNSW) 그래프를 사용한 인덱스
  - 그래프 기반 검색 방법, 큰 데이터셋에서도 빠른 검색 성능을 제공
- IndexLSH
  - Locality Sensitive Hashing (LSH)를 사용한 인덱스
  - 특정 거리 매트릭에 기반한 근사 검색을 빠르게 수행
 
→  규모가 크지 않다는 점을 고려하여 가장 기본이 되는 IndexFlatL2 인덱스를 사용 

## Rerank
- RAG의 정확도는 관련 정보의 컨텍스트 내 존재 유무가 아닌 순서로 결정 → 즉, 관련 정보가 컨텍스트 내 상위권에 위치하고 있을 때 좋은 답변을 얻을 수 있음
- 정보의 순서를 조정하기 위해 Rernak를 사용
  - 검색에서 한차례 선별된 정보 리스트에서 상위 K개의 문서에 한정하여 순위를 재조정
  - reranker 모델을 사용하여 최종적으로 질의에 대해 가장 의미 있는 내용을 담고 있는 문서를 보다 상위로 올리는 것을 목표로 함
 <br>
 
## 사용 방법

1. git clone
```
git clone https://github.com/YEERRIn/SemanticSearchWithRanker
```

2. query 입력
```
query = '간식으로 먹을 수 있는 든든한 샌드위치 추천해줘' 
```
<br>

## 팀원 소개
|[송다은](https://github.com/daeun6)|[문미란](https://github.com/alfks)|[신예린](https://github.com/YEERRIn)|[정은지](https://github.com/bbobburi)|
| :---: | :---: | :---: | :---: |
|<img width="100" src="https://github.com/GDSC-SWU/2023-AI-ML-study/assets/81478444/21400679-dcc3-4731-9638-d8f717e0bc84"/>|<img width="100" src="https://avatars.githubusercontent.com/u/117802772?v=4"/>|<img width="100" src="https://avatars.githubusercontent.com/u/109721289?v=4"/>|<img width="100" src="https://avatars.githubusercontent.com/u/93800329?v=4"/>|
