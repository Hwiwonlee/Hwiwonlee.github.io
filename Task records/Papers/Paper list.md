12.30
## 1. Identification of salivary metabolomic biomarkers for oral cancer screeing  
### Summary 
&nbsp;&nbsp;&nbsp;&nbsp;Saliva와 tumor tissue의 metabolomic analysis로 non-invasive oral cancer screeing의 방법을 발굴하는 것이 목적이며 2개의 potential biomarker를 찾았고 이를 이용한 Mutiple logistic model을 제안했다.(2016, Ishikawka, et al.)  
### Statistical method  
- Mann-Whitney test(saliva, with FDR correction)  
- Wilcoxon matched pairs signed rank test(tissue, FDR correction)  
- Mann-Whitney test and chi-square test(other parameters)  
- Multiple Logistic Model  
    1. tissue에서 유의한 metabolites 선택
    2. saliva에서 유의하며 fold change of averaged concecntration의 identical trend를 갖는 metabolite 선택
    3. SVM-FS와 stepwise FS로 variable selection
    4. model에 대한 CV 시행  
- ROC, AUC
-------------------------------------------------------------------------------
## 2. Effect of timing of collection of salivary metabolomic biomarkers on oral cancer detection
### Summary
&nbsp;&nbsp;&nbsp;&nbsp;Saliva의 수집시점을 3개로 구분(아침식사 후 1.5시간, 3시간, 저녁식사 후 12시간), 구강암 환자의 saliva를 수집했고 하나의 수집 시점(식사 후 1.5시간 이후)에서 건강한 사람의 saliva를 수집해 metabolite의 검출을 시행했다. 검출 결과 시점에 따라 metabolite의 concentration이 달랐고 저녁식사 후 12시간 후의 saliva의 concentration이 가장 높았다. 구강암 환자의 모든 수집 시점의 saliva와 과 건강한 사람의 saliva에서 공통적으로 나온 6개의 metabolites와 저자의 이전 연구에서 potential biomarker로 정의한 2개의 metabolite에 대해 ROC, AUC를 계산해 각 metabolite들의 discrimination ability를 보였다.(2017, Ishikawka, et al.)  
### Statistical method
- Mann-Whitney test(saliva, with FDR correction)  
- ROC, AUC  
--------------------------------------------------------------------------------
## 3. Metabolomic NMR fingerprinting to Identify and Predict Suvival of Patients with Metastatic Colorectal Cancer
### Summary
&npsp;&npsp;&npsp;&npsp;H-NMR(proton nuclear magnetic resonance)를 이용, mRCR(metastatic colorectal cancer) 환자와 control group을 비교해 metabolites에 근거한 mCRC 예측 model을 만들었다.(2012, Ivano Bertini, et al.)  

### Statistical method  
- PLS : Reduct dimesionality  
- SVM : Classification  
- Canonical correlation analysis  
- CV : model assessment  
- non-para Kruskal-Wallis test : The relative concentrations of each metabolite were calculated by integrating the signals in the spectra  
- Fisher exact test & Kruskal-Wallis : Groupwise test with categorical variable or continous variable  
----------------------------------------------------------------------------------
## 4. The early diagnosis and monitoring of squamous cell carcinoma via saliva metabolomics  
### Summary  
&nbsp;&nbsp;&nbsp;&nbsp;OSCC를 조기진단할 수 있다면 환자의 생존률 증가를 이뤄낼 수 있을 것이다. 본 연구는 mass spectrometry 및 statistical analysis를 통해 대조군과 실험군 사이 유의한 차이가 있는 5개의 potential metabolites를 찾아내었다. potential metabolites를 이용한 multiple logistic regression의 ROC, AUC를 계산해본 결과 AUC=0.997, sen = 100%, spec = 96.7%의 높은 성능을 보여 제안한 모델을 이용한다면 OSCC의 조기진단 성공확률을 높일 수 있을 것이다.(2014, Qihui Wang, et al.)  
### Statiscal method  
- PCA : No significance  
- OPLS-DA, S-plot, VIP(Variable Importance in Projection) : Dimension reduction and variable selection  
- Mann-Whitney U test  
- ROC & AUC : After additional mass spectrometrical analysis, To show that assessment of each of selected metabolites  
----------------------------------------------------------------------------------
## 5. [Review]Saliva Metabolomics Opens Door to Biomarker Discovery, Disease Diagnosis, and Treatment  
### Summary  
&nbsp;&nbsp;&nbsp;&nbsp;Saliva Metabolomics를 분석함으로써 구강암, 유방암, 췌장암과 치주질환에 영향을 미치는 것으로 보이는 57개의 metabolites를 찾아냈다. 이 연구와 향후 더욱 많은 연구들이 진행되면 다른 종류의 암에 영향을 미치는 biomarker를 더욱 알아낼 수 있을 것이며 이로써 암 진단과 치료에 긍정적인 영향을 기대해볼 수 있을 것이다.(2012, A Zhang, et al.)  

### Statistical method  
- Used in paper statistical method is None. because this is review paper. However, the AUC used in the cited paper was introduced.  
----------------------------------------------------------------------------------
## 6. [Review]Bioanalytical methods for metabolomic profiling: detection of head and neck cancer, including oral cancer
### Summary  
&nbsp;&nbsp;&nbsp;&nbsp;Research method of metabolomics는 크게 mass spectrometry(MS)와 nuclear magnetic resonance(NMR)를 이용한 metabolites의 검출과 검출된 metabolites를 이용하는 statistical analysis로 나뉜다. 본 문에서는 MS와 NMR의 장단점에 대해 알아보고 주로 사용되는 statistical method를 간단히 설명하겠다. (2015, Nirbhay S.Jain, et al.)   

### Statistical method  
- Supervied learning : PLS-DA, SIMCA(Soft Independent Modeling of Class Analogies), OCS(Orthogonal Signal Correction), OPLS-DA
- Unsupervied learning : PCA, HCA(Hierarchical Cluster Analysis), KNN
----------------------------------------------------------------------------------

12.31
## 8. Capillary electrophoresis mass spectrometry-based saliva metabolomics identified oral, breast and pancreatic cancer-specific profiles
### Summary  
&nbsp;&nbsp;&nbsp;&nbsp;3개의 암종(oral, breast, pancreatic)과 치주질환(periodontal disease) 환자와 Heathy control group 사이, saliva의 metabolites를 MS 및 statistical analysis로 분석해 principal metabolites와 biomarkers를 찾아냈다.  

### Statistical method  
- PCA  
- PLS-DA
- MLR
- CV
- Mann-Whitney test
- Steel-Dwas test
