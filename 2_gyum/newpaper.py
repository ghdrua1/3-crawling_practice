#!/usr/bin/env python
# coding: utf-8

# # 신문기사 데이터 추출 및 CSV 저장
# 이 노트북에서는 GDELT API를 사용하여 특정 키워드에 맞는 신문기사를 추출하고, Newspaper3k 라이브러리를 사용해 각 기사의 본문을 파싱한 후, 이를 CSV 파일로 저장하는 방법을 설명합니다.

# ### 1. 필요한 라이브러리 설치 및 임포트
# 
# 이 단계에서는 필요한 라이브러리들을 설치합니다. gdeltdoc는 GDELT API를 사용하여 기사를 검색할 때 필요하고, newspaper3k는 각 기사에서 본문을 추출할 때 사용됩니다. 또한, pandas 라이브러리를 사용해 데이터를 쉽게 다룰 수 있습니다.

# In[ ]:


get_ipython().system('pip install gdeltdoc')
get_ipython().system('pip install newspaper3k==0.2.8')
get_ipython().system('pip install lxml_html_clean')
get_ipython().system('pip install pandas')


# ### 2. 라이브러리 임포트
# 필요한 라이브러리를 코드에 임포트합니다. 

# In[2]:


from gdeltdoc import GdeltDoc, Filters
from newspaper import Article
import pandas as pd


# ### 3. GDELT API 필터 설정
# 
# GDELT API를 사용하여 원하는 기사를 추출하기 위한 필터를 설정합니다. Filters 클래스를 사용하여 날짜, 키워드, 도메인 등 다양한 조건을 지정할 수 있습니다.

# In[3]:


f = Filters(
    keyword = "Microsoft",  # 키워드: Microsoft 관련 기사만 추출
    start_date = "2024-05-01",  # 시작 날짜
    end_date = "2024-05-25",  # 종료 날짜
    num_records=10,  # 가져올 기사의 수
    domain ="nytimes.com",  # 특정 도메인(여기서는 NYTimes)
    country="US",  # 국가 설정 (US)
)


# ### 4. GDELT 데이터 검색
# 
# 설정한 필터에 맞는 기사를 GDELT API를 통해 검색하여 결과를 pandas DataFrame으로 변환합니다.

# In[ ]:


# GDELT 객체 생성
gd = GdeltDoc()

# 필터에 맞는 기사 검색
articles = gd.article_search(f)

# 기사의 URL과 제목을 포함한 DataFrame 생성
articles_data = []
for index, row in articles.iterrows():
    url = row['url']
    title = row['title']
    
    # Newspaper3k 라이브러리를 사용하여 기사 본문 추출
    article = Article(url)
    article.download()
    article.parse()
    text = article.text  # 기사 본문
    
    # DataFrame에 추가
    articles_data.append({
        "title": title,
        "url": url,
        "text": text
    })

# DataFrame 생성
articles_df = pd.DataFrame(articles_data)

# 결과 출력
articles_df.head()  # 첫 5개의 기사 출력


# ### 5. CSV 파일로 저장
# 
# 최종적으로 추출한 기사 데이터를 pandas DataFrame으로 저장한 후, 이를 CSV 파일로 저장합니다.

# In[5]:


# CSV 파일로 저장
articles_df.to_csv('articles_data.csv', index=False)

