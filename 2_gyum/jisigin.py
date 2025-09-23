#!/usr/bin/env python
# coding: utf-8

# # 네이버 지식인 페이지 정적 크롤링
# 정적 크롤링을 통해 네이버 지식인 페이지에서 데이터를 추출하는 방법을 학습합니다.

# ### 1. 필요한 라이브러리 설치 및 임포트
# 먼저, 웹 크롤링을 위해 필요한 라이브러리들을 설치하고 임포트합니다.
# 
# - bs4: BeautifulSoup 라이브러리는 HTML/XML 페이지를 파싱하여 데이터를 쉽게 추출할 수 있게 도와줍니다.
# - requests: HTTP 요청을 보내 웹 페이지의 HTML을 받아오는 라이브러리입니다.
# - pandas: 데이터를 표 형태로 처리하고, 엑셀 파일로 저장하는 데 사용됩니다.
# - openpyxl: pandas가 엑셀 파일을 처리할 수 있도록 도와주는 라이브러리입니다.

# In[1]:


get_ipython().system('pip install bs4')
get_ipython().system('pip install requests')
get_ipython().system('pip install pandas')
get_ipython().system('pip install openpyxl')


# ### 2. HTML 페이지 불러오기 및 파싱
# 이제 웹 페이지를 불러와서 HTML을 파싱하여 필요한 데이터를 추출하는 작업을 시작합니다.
# 
# - requests.get(url): 지정한 URL에 HTTP GET 요청을 보냅니다.
# - BeautifulSoup(html, 'html.parser'): 응답 받은 HTML을 BeautifulSoup을 사용해 파싱합니다.

# In[1]:


from bs4 import BeautifulSoup
import requests

# 네이버 지식인 삼성전자 검색 페이지 URL
url = "https://kin.naver.com/search/list.naver?query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90"
response = requests.get(url)  # 요청 보내기
html = response.text  # 응답 받은 HTML 문서
soup = BeautifulSoup(html,'html.parser')  # BeautifulSoup으로 파싱
soup


# ### 3. 특정 HTML 요소 선택
# 크롤링할 HTML 요소를 선택하기 위해 CSS 선택자를 사용하여 데이터를 추출합니다.
# 
# - soup.select_one(): CSS 선택자를 사용하여 첫 번째 일치하는 요소를 선택합니다.
# - tree: 선택된 HTML 요소(첫 번째 질문)에 대한 정보를 담고 있습니다.

# In[7]:


# 첫 번째 질문 요소 선택
tree = soup.select_one('.basic1 > li > dl')
tree  # 첫 번째 질문의 HTML 구조를 출력하여 확인


# ### 4. 정보 추출: 제목, 링크, 날짜, 카테고리, 답변수
# 선택한 HTML 요소에서 원하는 데이터를 추출합니다.
# 
# - title_tag.text: title_tag 요소에서 텍스트(제목)를 추출합니다.
# - title_tag.attrs['href']: title_tag 요소에서 링크를 추출합니다.
# - date_tag.text, category_tag.text: 각각 작성일과 카테고리를 추출합니다.
# - hit_tag.text.split(): 답변수를 추출하고 불필요한 문자를 제거합니다.

# In[18]:


# 제목과 링크 추출
title_tag = tree.select_one("._nclicks\\:kin\\.txt._searchListTitleAnchor")
title = title_tag.text
link = title_tag.attrs['href'] 
print(title, link)


# In[ ]:


# 날짜 추출
date_tag = tree.select_one(".txt_inline")
date = date_tag.text
print(date)


# In[32]:


# 카테고리 추출
category_tag = tree.select_one(".txt_g1._nclicks\\:kin\\.cat2")
category = category_tag.text
print(category)


# In[9]:


# 조회수 추출
hit_tag = tree.select_one('.hit')
texts = hit_tag.text
hit = texts.split()[1]
print(hit)


# ### 5. 한 페이지에서 모든 질문 정보 추출
# 한 페이지에 여러 질문이 있을 때, 모든 질문의 정보를 추출합니다.
# 
# - soup.select(): 여러 개의 요소를 선택하여 리스트로 반환합니다.
# - 각 질문에 대해 for 루프를 돌며 제목, 링크, 날짜, 카테고리, 조회수를 추출합니다.

# In[38]:


# 여러 질문 정보 추출
trees = soup.select(".basic1 > li > dl")
for tree in trees:
    title = tree.select_one("._nclicks\\:kin\\.txt").text
    link = tree.select_one("._nclicks\\:kin\\.txt").attrs['href']
    date = tree.select_one(".txt_inline").text
    category = tree.select_one("._nclicks\\:kin\\.cat2").text
    hit = tree.select_one(".hit").text.split()[1]
    
    # 출력
    print(title, link, date, category, hit)


# ### 6. 여러 페이지 크롤링
# 페이지를 변경하면서 여러 페이지의 데이터를 크롤링합니다.
# 
# - for page_num in range(1, 4): 1페이지부터 3페이지까지 순차적으로 크롤링합니다.
# - 각 페이지에서 데이터를 추출하여 data 리스트에 추가하고, 이를 pandas DataFrame으로 변환하여 엑셀 파일로 저장합니다.

# In[43]:


# 여러 페이지에서 정보 추출
data = []
for page_num in range(1, 4):  # 1~3페이지 크롤링
    url = f"https://kin.naver.com/search/list.naver?query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&page={page_num}"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    trees = soup.select(".basic1 > li > dl")
    
    for tree in trees:
        ################
        title = tree.select_one("._nclicks\\:kin\\.txt").text
        link = tree.select_one("._nclicks\\:kin\\.txt").attrs['href']
        date = tree.select_one(".txt_inline").text
        category = tree.select_one("._nclicks\\:kin\\.cat2").text
        hit = tree.select_one(".hit").text.split()[1]
        # 데이터를 리스트에 추가
        data.append([title, link, date, category, hit])

# DataFrame으로 변환
import pandas as pd
df = pd.DataFrame(data,columns=['title','link','date','category','hit'])

df


# ### 7. 결과 저장
# 위의 크롤링한 데이터를 엑셀 파일로 저장합니다.
# 
# - df.to_excel(): 추출한 데이터를 엑셀 파일로 저장합니다. index=False를 설정하여 인덱스를 제외하고 저장합니다.

# In[44]:


# pandas를 사용해 엑셀로 저장

df.to_excel('jisigin.xlsx',index=False)


# In[ ]:




