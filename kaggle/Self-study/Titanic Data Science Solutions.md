https://www.kaggle.com/startupsci/titanic-data-science-solutions/notebook#Titanic-Data-Science-Solutions

### 들어가기 전에
본 글은 1) kaggle에 익숙해지기 위해 2) Python이 실제로 어떻게 사용되는지 알기 위해 3) 영어 공부 및 글쓰기 능력 강화 등의 목적으로 작성되었다. 
kaggle에 올라와있는 '좋은' notebook을 대상으로 했으며 이번 글은 Titanic Data Science Solutions의 번역과 내용 이해를 위한 comment로 이뤄져 있다.
나의 이해가 제 1 목적이므로 원문의 구성과 조금 달라질 수 있다. 얼마나 계속될지는 모르겠지만 최대한 하는데까지 해보자. 

# Titanic Data Science Solutions
## 1. Introduction

본 글은 책, Data Science Solutions<sup>[[1]](#footnote_1)</sup>의 한 부분이다. 
본 글은 kaggle과 같은 사이트에서 볼 수 있는 data science 경연이나 문제들을 해결할 수 있는 일반적인 업무 흐름에 따라 작성되었다.

kaggle에는 data science로 해결할 수 있는 수 많은 과제들이 문제를 해결하기 위해 제출된 더 많은 수의 훌륭한 보고서들이 있다.
그러나 대부분의 보고서는 전문가가 전문가를 위해 쓴 글이기 때문에 '어떻게 해결방법이 고안되었는가'를 설명할 때 일부를 생략하기도 한다. 
물론 주요 독자인 data science의 전문가는 문제가 되지 않지만 이 글을 보고 있을 입문자들에겐 올바른 이해를 위해 생략된 일부가 꼭 필요할 것이다.
본 글의 목적은 해결 방법이 어떻게 고안되었는지를 명확히 보여주는 것이다. 따라서 단계별로 진행되는 업무흐름을 명시할 것이고 문제 해결 방법 제시를 위해 진행되는 모든 의사결정과 이유를 각 단계마다 명확히 보일 것이다. 

### 1.1 Workflow stages
data science 경연에서 제출할 보고서를 작성할 때, 아래의 7개의 흐름을 따라가는 것을 제안한다. 

1. 질문이나 문제를 정의할 것
1. training data와 testing data를 명시할 것
1. data 전처리(Wrangle, prepare, cleanse)
1. data를 분석, 탐색하거나 패턴을 확인할 것
1. 문제 해결을 위한 모델을 세우고 모델을 통해 예측할 것
1. 시각화를 비롯한 결과 제시를 통해 문제 해결 과정을 보일 것
1. 결과를 제출할 것

위의 과정은 일반적으로 따라갈 수 있는 흐름이지만 모든 일이 그렇듯, 예외가 발생할 수 있다. 아래의 경우가 일반적인 흐름을 따르지 않는, 이례적인 사례들이다.

- 여러 개의 과정을 섞어서 진행하는 경우. 시각화를 이용해 data를 분석하는 경우.
- 위의 과정에서 명시된 것보다 더 이른 단계에서 분석을 시작하는 경우. 전처리 이전과 이후에 data를 분석하는 경우. 
- 전체 과정에서 한 단계를 여러번 반복하는 경우. 시각화 단계가 여러번 반복되는 경우.
- 한 단계를 모두 제외시키는 경우. 경연 결과에서 해당 단계를 보이지 않아도 된다고 판단한 경우.







<a name="footnote_1">[1]</a> Data Science Solutions의 저자와 notebook Titanic Data Science Solutions의 저자가 같다
