# Reinforcement Learning in R  
Nicolas Pröllochs  
2020-03-02  

이 문서는 R에서 model-free reinforcement를 구현해내는데 도움을 줄 수 있는 **ReinforcementLearning** 패키지의 소개를 위해 작성되었다. 이 문서에 포함된 **ReinforcementLearning** 패키지 사용의 예제는 input data와 정의된 states, actions, rewards로 실행이 가능하다. 예제를 통해 이 패키지가 각 state에서 최고의 action, 즉 최적화된 policy를 찾도록 agent를 강화학습시키는 과정을 배울 수 있을 것이다.  

우리는 **ReinforcementLearning** 패키지가 어떤 부분에서 강점을 가지고 있는지 보여주기 위해 단계별로 진행되는 예제를 두었으며 천천히 따\라가다보면 함수의 사용법과 효과에 대해 익힐 수 있을 것이다. 더 나아가, 강화학습의 핵심이라 할 수 있는 agenet의 학습과 action selection behavior를 customize하는 방법에 대해서도 설명해두었다.  

**ReinforcementLearning** 패키지의 핵심은 아래와 같다.  

- 이미 알려진 transition samples의 fixed set으로부터의 학습으로 최적 policy를 도출  
- 미리 정의된 학습 규칙과 행동 결정 규칙에도 호환  
- model-free 강화학습 과제에 대해 호환될 정도로 높은 수준의 사용자 친화적인 framework을 갖고 있음  

## Introduction  

강화학습은 동적 환경(dynamic environment)에서 trial-and-error의 상호작용을 통해 어떻게 agent에게 최적화된 behavior를 학습시킬 것인가를 다루는 분야이다. 강화학습의 모든 알고리즘들은 agent가 제대로 행동하고 있는가를 나타내는 reward signal과 같은 '제한된' feedback property를 갖고 있다. 강화학습에는 supervied machine learning 방법들과는 다르게 '옳은 행동'에 대한 지침들이 존재하지 않는다. 그러므로 강화학습의 목적과 해결해야할 문제는 제한된 유형의 피드백만 주어진 에이전트의 행동을 개선하는 것이다.

### The reinforcement learning problem
강화학습에서의 의사결정자는 **agent**다. 일련의 관측값을 통해 환경(environment)과 상호 작용하고 시간이 지남에 따라 최대화될 reward를 좇는다. model은 다음 3개의 구성요소를 갖는다. 

1. 상태들의 유한한 경우의 수로 이뤄진 집합(a finite set of environment states) **_S_**  : 상태집합
2. 행동들의 유한한 경우의 수로 이뤄진 집합 (a finite set of agent actions) **_A_**  : 행동집합
3. 강화의 signal인 scalar(즉, 보상 = reward)의 집합 **_R_** : 보상집합

각각의 반복 _i_ 에 따라 agent는 상태집합에 속하는 상태(s<sub>i</sub> ∈ **_S_**)를 관측(혹은 **결정**)하고 상태에 따라 정해진 행동(a<sub>i</sub> ∈ **_A_**(s<sub>i</sub>), 이 때, **_A_**(s<sub>i</sub>)⊆ **_A_** 이며 **_A_**(s<sub>i</sub>)는 상태 s<sub>i</sub>에서 가능한 행동으로 정의된다.)을 하게 된다. 반복의 순환이 끝나면 agent는 행동의 결과인 **보상**(reward)를 받는데 이 또한 보상집합에 속한다. 이후 i+1번째의 반복을 시작해 새로운 상태인 s<sub>i+1</sub>를 갖는다.

### Policy learning
i번째 반복이후의 시점에서 발견한 최적점을 저장해두기 위해, 강화학습에서는 각각의 상태, s<sub>i</sub>에서 가능한 행동 a<sub>i</sub>의 기댓값으로 정의되는 stage-action function **_Q_**(s<sub>i</sub>, a<sub>i</sub>)를 사용한다. 만약 **_Q_**(s<sub>i</sub>, a<sub>i</sub>)를 알고 있다면 max(**_Q_**(s<sub>i</sub>, a<sub>i</sub>))를 이뤄낼 수 있는 상태, s<sub>i</sub>와 행동, a<sub>i</sub>로 구할 수 있는 최적의 policy, **_π_**<sup>＊</sup>(s<sub>i</sub>, a<sub>i</sub>)을 찾을 수 있다. 결과적으로 **Agent**의 학습은 optimal policy function **_π_**<sup>＊</sup>(s<sub>i</sub>, a<sub>i</sub>)를 학습함으로써 expected reward를 극대화시키는 것을 의미한다. 

### Experience replay
**경험 재현**(experience replay)은 강화학습의 agent가 과거의 학습으로부터 학습했던 내용을 기억하고 다시 사용할 수 있게 하는 방법이다. 관측된 상태(혹은 결정된 상태) 전환이 시스템과 상호작용하면서 마치 수집된 새로운 관측인 것처럼 agent에게 반복적으로 재현시킴으로써 convergence 속도를 높이는 것이 기본 개념이다. 그러므로 experience replay는 states, actions 그리고 rewards로 구성된 sample sequence를 dataset으로 필요로 한다. 이러한 data는 직접 상호작용할 필요 없이 실행 중인 시스템에서도 수집될 수 있다. 저장된 training example dataset를 통해 에이전트는 입력 데이터의 모든 상태 전환에 대한 상태 동작 기능과 최적의 정책을 배울 수 있다. 다음 단계에서는 validation이나 새로운 데이터 수집(예를 들어, 현재 정책을 반복적으로 개선하기 위해)을 위해 시스템에 policy를 적용할 수 있다. Experience replay의 주요한 장점은 추가적인 상호작용이 없이 갱신된 상태로부터 information의 역전파(back-propagation)를 허용함으로써 convergence의 속도를 높이는데 있다. 


