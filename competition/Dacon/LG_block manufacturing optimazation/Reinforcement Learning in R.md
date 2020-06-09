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

## Setup of the ReinforcementLearning package  
생략

## Usage  
**ReinforcementLearning** 패키지의 주된 기능들을 예제를 통해 알아보자.  

### Data preparation  
**ReinforcementLearning** 패키지에는 Q-learning이나 경험 재현과 같은 강화학습의 매커니즘들을 활용할 수 있는 함수들이 정의되어 있다. 즉, 상태, 행동, 보상 등의 sample sequences로 이뤄진 과거 경험을 토대로 최적의 policy를 학습시킬 수 있다. 다시 말해. 다음과 같은 state-transition tuple (s<sub>i</sub>, a<sub>i</sub>, r<sub>i+1</sub>, s<sub>i+1</sub>)로 각 학습 예제들이 구성되어 있다는 것이다. 
  1. s<sub>i</sub>는 현재의 environment state.  
  2. a<sub>i</sub>는 현재의 state에서 선택된 action.  
  3. r<sub>i+1</sub>는 현재의 state에서 다음의 state로 넘어가면서 곧바로 생성되는 reward.  
  4. s<sub>i+1</sub>는 한 단계 이후의 environment state.  
강화학습을 위한 학습 예제들은 (1) 외부 source를 통해 구성되거나 (2) environment의 behavior에 의해 정의된 function을 실행함으로써 구성된다. 이 두가지 방법에 의해, 앞서 보았던 tuple, (s<sub>i</sub>, a<sub>i</sub>, r<sub>i+1</sub>, s<sub>i+1</sub>)이 구성되어야 한다. 위의 두 가지 방법에 대한 차이는 다음 절에서 설명하도록 하겠다.

### Learning from pre-defined observations  
이 접근방식은 입력 데이터가 미리 결정되어 있거나 과거의 행동을 복제하는 agent를 교육하고자 할 때 유용하다. 이 경우 과거 관측치가 있는 표 형식의 데이터 구조를 패키지에 삽입하기만 하면 된다. sensor data와 같은 external source에서 state-transition tuples을 수집하여 environment과의 추가적인 상호작용을 제거하여 agent를 학습시키고자 할 때 사용할 수 있다.  

다음의 예시는 무작위로 샘플링된 tic-tac-toe 게임의 게임 상태를 포함하는 데이터 집합의 처음 5개의 관찰 결과를 보여준다. 데이터 집합에서 첫 번째 열은 현재의 보드 상태를 나타낸다. 두 번째 열은 이 상태에서 플레이어 X의 관측된 동작을 나타내고 세 번째 열은 동작을 수행한 후의 결과 상태를 나타낸다. 네 번째 열에는 선수 X에 대한 결과 보상이 명시되어 있다. 이 데이터 집합은 에이전트 학습을 위한 입력 자료로 충분하다.
```r
data("tictactoe")
head(tictactoe, 5)
```

### Dynamic learning from an interactive environment function
미리 정의된 dataset이 없거나 불규칙적인, 어쩌면 극단적일 수도 있는 경우를 학습시키고 싶다면 behavior of the environment를 모방한 함수를 정의해 모의 dataset을 만들어낸 후, 이 dataset으로 학습시키는 방법이 있다. state-action pair를 parameter로 갖는 environment function의 예시이다. 함수에 적절한 값을 넣어 실행시키면 **다음 상태**와 **보상**를 얻을 수 있을 것이다. R을 활용해 센서 등 외부 데이터 소스에 접속하고 일반적인 인터페이스를 통해 함수를 정의하고 실행할 수도 있다. 그러한 함수의 구조는 다음과 같다. 
```r
environment <- function(state, action) {
  ...
  return(list("NextState" = newState,
              "Reward" = reward))
}
```
environment function를 정의한 후에야 random sequences를 얻을 수 있다. 이 때의 parameter는 표본의 갯수(**_N_**), environment function, 상태집합(**_S_**), 행동집합(**_A_**)이다. 이로써 state transition tuples, (s<sub>i</sub>, a<sub>i</sub>, r<sub>i+1</sub>, s<sub>i+1</sub>) _for i = 1,...,N_ 의 결과값을 얻을 수 있다. 다음의 코드는 설정된 environment function으로부터 어떻게 state transition tuples를 생성해내는지에 대한 예시다. 
```r
# Define state and action sets
states <- c("s1", "s2", "s3", "s4")
actions <- c("up", "down", "left", "right")

env <- gridworldEnvironment

# Sample N = 1000 random sequences from the environment
data <- sampleExperience(N = 1000, 
                         env = env, 
                         states = states, 
                         actions = actions)
```

### Learning phase
### General setup
**ReinforcementLearning()** 에는 강화학습의 핵심 기능들이 모두 포함되어 있어, 이전 절에서 다뤘던 input dataset를 사용하면 agent에게 강화학습을 시킬 수 있다. **ReinforcementLearning()** 은 다음의 parameter를 갖는다. (1) 각 행을 state transition tuples, (s<sub>i</sub>, a<sub>i</sub>, r<sub>i+1</sub>, s<sub>i+1</sub>)로 갖는 data frame을 data argument로 갖는다. (2) 사용자는 data 내의 tuple elements에 열 이름을 지정해야 한다. 다음의 pseudocode는 외부 소스에서 온 pre-defined data를 사용한 예제이다. pseudocode를 보면 parameter, s, a, r, s_new가 어떤 argument를 갖는지 확인 할 수 있다.
```r
# Load dataset
data("tictactoe")

# Perform reinforcement learning
model <- ReinforcementLearning(data = tictactoe, 
                               s = "State", 
                               a = "Action", 
                               r = "Reward", 
                               s_new = "NextState", 
                               iter = 1)
```
### Parameter configuration
agent의 learning behavior를 사용자 정의 및 조정하기 위해 에 몇 가지 parameter를 사용할 수 있다.
  - alpha는 learning rate로 0부터 1의 값을 갖는다. **0**은 Q value를 업데이트하지 않음을 의미하고 이는 곧 학습되는 게 없음을 의미한다. 0.9와 같은 높은 수준의 값을 설정하면 주마간산식으로 학습하게 되어 정확도가 매우 떨어진다. [매우 좋은 시각화 예제](http://www.benfrederickson.com/numerical-optimization/)  
  - gamma는 Discount factor로 0부터 1의 값을 갖는다. 미래에 얻게 될 보상의 중요성을 결정하는 값으로, 0으로 설정하면 agent는 현재의 보상을 좇는 매우 근시안적인 학습을 하게 되고 1으로 설정하면 agent는 과정의 보상을 제쳐두고 최후의 보상만을 생각하는 학습을 하게 된다.  
  - epsilon은 Exploration parameter로 0부터 1의 값을 갖는다. ε-greedy action selection의 exploration mechanism를 정의하는 값이다. ε-greedy action selection의 exploration mechanism를 사용한다면, agent는 확률 ε에 기반한 행동 선택으로 environment를 탐사한다. 또는, 확률 1−ε을 갖는 optimal action을 선택함으로써 agent가 current knowledge를 활용할 수 있도록 한다. epsilon은 이미 존재하는 policy에 새로운 경험을 샘플링할 때만 사용된다.  
  - iter는 training dataset를 이용해 agent를 학습시키는 횟수의 반복을 의미한다. 0보다 큰 숫자로 정의되어야 하며 1로 정의한다면, 각각의 state transition tuple는 agent에게 한번씩만 학습된다. training data의 크기에 따라 결정하는 것을 권장하며, 큰 수로 정의한다면 convergence는 향상시킬지 몰라도 꽤 긴 시간이 필요하게 될 것이다.  
learning parameters인 alpha, gamma, epsilon는 ReinforcementLearning()에는 부수적인 요소지만 ReinforcementLearning()에 control object를 추가할 것이라면 control object에 정의해놓아야 할 필수적인 값들이다. 
```r
# Define control object
control <- list(alpha = 0.1, gamma = 0.1, epsilon = 0.1)

# Pass learning parameters to reinforcement learning function
model <- ReinforcementLearning(data, iter = 10, control = control)
```

### Diagnostics
학습과정의 결과는 state-action table과 각 상태에 따른 최선의 행동으로 정의된 최적 policy로 구성되어 있다. computePolicy(model)로 최적 policy를 출력할 수 있으며 print(model)로 state-action table, 즉, 각각의 state-action pair의 Q-value를 볼 수 있다. 더 나아가 summary(model)를 이용하면 model의 자세한 내용과 요약 통계량도 확인할 수 있다. 
```r
# Print policy
computePolicy(model)

# Print state-action table
print(model)

# Print summary statistics
summary(model)
```
