# Goal : Find and select paper subject 

> **SUMMARY NOTE**  
> &nbsp;&nbsp;&nbsp;&nbsp;meta analysis, network meta analysis가 cancer 혹은 disease 분야에서 어떻게 사용되는지 확인하기 위해 여러 논문을 골랐고 읽은 것들 중에 몇 편을 추려 기록했다. 보면서 이론적인 접근보다는 data를 이용한 실습 혹은 연구적인 측면이 강하다는 생각이 들었다. I-square가 0.5가 넘어가도 의미있다고 하거나 result에 대한 추가적인 error test를 하지 않는 부분들 때문이었다.  
> &nbsp;&nbsp;&nbsp;&nbsp;추후 해야할 것은 1) 어떤 주제로 2) 어떤 방법을 사용할 것인지 정하는 것이고 더불어 3) DII에 대한 간단한 조사해보고 정의와 도출 및 쓰임에 대해 알아봐야할 것이다. 


## 01.03
## 1. Dose-reponse meta-analysis of coffee consumption and risk of colorectal adenoma
### Abstract 
&nbsp;&nbsp;&nbsp;&nbsp;coffee 섭취와 colorectal adenoma 발병 사이의 논쟁은 꽤 역사가 깊다. 본 연구에서는 coffee 섭취와 colorectal adenoma 발병 사이의 관계를 밝히기 위해 meta-analysis를 이용, 과거에 진행된 연구결과를 통합해 coffee와 colorectal adenoma 발병 사이의 관계를 추론해보고자 한다. Pubmed, Medline, Embase를 이용해 coffee와 CRA의 키워드로 검색해본 결과 18년 9월 1일 전까지 총 6444개의 논문을 찾았고 선별과정을 통해 8개의 meta-analysis 대상 논문을 선정했다. 8개의 논문에 실린 결과를 바탕으로 meta-analysis의 여러 방법론(response-dose with random effect model, response-dose with fixed effect model, subgroup analysis)을 사용했다. 진행한 meta-analysis에서 outcome value로는 대중적으로 사용되는 odds ratio(OR)를 사용했다. meta-analysis를 통한 분석 결과, coffee 섭취 증가는 CRA의 발병 위험을 감소시킨다는 결론을 얻었다. 그러나 meta-analysis로 통합시킨 연구 사이에 여러 차이가 있기 때문에 여전히 신중히 생각해볼 문제다. (Wang, Y., et al., 2019)
### Statistical method  
- Meta-analysis   
    1. Respose-dose model 
        1. fiexed effect model : general approach
        1. random effect model : 남녀를 합쳐 진행한 최초 meta-analysis, heterogeneity 여부를 확인하고자 한 것 같음. 
    2. Subgroup analysis : 연구 방법인 cohort, case-control group으로 나눠 분석
### Notes
1. Dose-reponse를 이용한 arregation이 가능함.
2. I-square가 0.5 중반이 되는데 의미있는 연구 혹은 accept 되는 연구라는게 신기함. 
3. case-control, cohort 등 연구 방법에 따른 subgroup analysis를 수행했다. 
4. disease 분야에서 meta-analysis를 사용하는 예시를 보았다. 
-------------------------------------------------------------------------------
## 2. Chemoprevention of colorectal cancer in individuals with previous colorectal neoplasia: systematic review and network meta-analysis
### Abstract
&nbsp;&nbsp;&nbsp;&nbsp;이미 존재하는 advanced metachronous neoplasia를 예방하기 위한 약물의 효과와 안정성에 대한 연구 결과를 network meta analysis로 종합해 어떤 약물이 효과적이고 안전한지 알아보도록 하겠다. (Dulai, PS., et al., 2016)
### Statistical method  
- Network meta-analysis   
    1. Bayesian approach
    2. SUCRA : ranking method for showing dominate thing
### Notes
1. Dose-reponse를 이용한 arregation이 가능함.
    1. 보통 사용하는 meta, NMA model을 Dose-reponse model라고 부르나봄. 난 fixed, random effect model로만 불렀었는데. 
2. 지금까지 본 NMA 논문이 그렇듯 이것도 comparison and find dominating thing이 목적임.  
3. cancer 분야에서 network meta-analysis를 사용하는 예시를 보았다. 
-------------------------------------------------------------------------------
## 3. Meta-analysis of the Association Between Dietary Inflammatory Index(DII) and Cancer Outcomes
### Abstract
&nbsp;&nbsp;&nbsp;&nbsp;높은 수준의 Dietary Inflammatory Index(이하 DII)가 암의 발병과 사망 위험을 증가시킬 수 있다는 가설은 많은 연구로 사실 여부가 증명되고 있다. 비교적 최근에는 암의 종류와 암의 발병 및 사망을 세세히 구분하여 더욱 심층적인 연구가 이뤄지고 있으며 이미 유의미한 결과들이 논문으로 출판되었다. 본 논문에서는 지금까지 나온 DII와 암의 발병 및 사망의 관계를 밝힌 연구들을 meta-analysis로 통합하여 DII와 암의 발병 및 사망 위험 사이의 관련성을 다시 한 번 확인하고자 한다. meta-analysis의 대상이 된 연구들은 PubMed, Scopus, Embase 등과 같은 online database에 1980년부터 2016년 10월까지 저장된 논문들에서 여러 단계를 거쳐 선택된 24편의 논문에 실린 결과들이다. meta-analysis 결과, 높은 수준의 DII가 암의 발병 및 사망 위험에 영향을 미친다는 것을 확인하였고 암 종을 구분해 시행한 meta-analysis에서도 같은 결과를 확인할 수 있었다. (Fowler, ME., Akinyemiju, TF. 2017)
### Statistical method  
-  Meta-analysis
    1. Random effect model 
### Notes
1. 단순한 meta-analysis 결과를 정리한 논문이다. 다만 24편의 논문에 실린 연구 결과를 정리하는 것이 조금 어려웠을 듯. 
2. DII의 정의와 도출에 대해 공부할 필요가 생겼다.  
3. 앞선 논문을 보면서도 느끼는 건데, meta-analysis의 대상이 되는 연구들의 design이 최대한 비슷해야 한다는 가정(Similarity assumption)이 존재하는데도 case-control, cohort, RCT 등의 다른 연구 방법으로 나온 결과들을 종합해 overall result를 만들어내는 게 신기하다. 더 신기한 건 그래도 유의하게 나온다는 사실. 
4. 어차피 유의하게 나오는 거 차라리 "Dose-reponse meta-analysis of coffee consumption and risk of colorectal adenoma"에서 처럼 subgroup analysis를 추가해보는 건 어땠을까 싶다. 그러면 좀 더 괜찮은 통계분석 구조가 됐을 것 같은데. 
5. publication bias와 같은, result가 갖고 있는 error에 대한 inference가 없다는 것도 눈에 띈다. 구조가 탄탄하지는 않은 것 같다. 
-------------------------------------------------------------------------------
## 4. Meta-analysis of the association between the Dietary Inflammatory Index(DII) and breast cancer risk 
### Abstract
&nbsp;&nbsp;&nbsp;&nbsp;DII와 암 발병에 대한 관련성 연구는 활발히 진행되고 있는 연구 분야 중 하나이다. 본 논문에서는 여러 암 종 중, 유방암의 발병과 DII 사이의 연구들을 meta-analysis로 종합해 연구 결과의 유의성을 다시 한번 확인하고자 한다. 2017년 9월 12일까지 Pubmed, EMBASE, Cochrane database에 등록된 논문들 중 7개의 논문을 최종 선택한 후 연구 결과를 meta-analysis로 분석 및 종합해 결과를 확인했다. 분석 결과 높은 수준의 DII를 가진 여성이 그렇지 않은 여성보다 유방암 발생 가능성이 더 높았다. 층화 분석 결과 폐경기의 여성, case-control design의 연구, Asia지역과 Europe지역 등이 다른 categories보다 DII score를 높게 갖는 경우일 때 유방암 발병률이 더 높았다. hormonal receptor의 positive, negative 사이의 비교에서도 positive group이 negative 그룹보다 유방암 발병률이 더 높았다. 본 논문의 한계는 높은 수준의 DII와 유방암과의 관계만을 확인한 것에 있다. 중간 수준의 DII와 유방암과의 관계를 확인한 것은 아니므로 관련 부분에 대한 추가연구가 필요할 것이다. (Wang, L., et al., 2018)
### Statistical method  
-  Meta-analysis
    1. Random effect model 
    2. Meta-regression and subgroup analysis
    3. Funnel plot 
### Notes
1. 유방암의 발병만을 대상으로한 meta-analysis여서 그런지 대상 연구의 개수가 좀 적은 것 같다. 
2. 단순히 random effect model 후 Q, I-square만 확인한 것이 아니라 다른 분석도 병행해서 수행한 것이 눈에 띈다. 
-------------------------------------------------------------------------------
