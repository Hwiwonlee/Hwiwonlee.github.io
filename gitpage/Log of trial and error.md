# 1일차  
## git page 만들기 : 2번의 repository 초기화 후 테마를 적용한 git page만들었다. 
여러 문제들이 있진 않았지만 큰 문제 하나로 대부분의 시간을 소모했다. 더 이른 시점에 문제를 해결할 수 있었지만 구글링 후의 결과들을 꼼꼼히 살피지 못한 것이 화근이었다. 영어 읽기의 숙련도를 더 늘리자.  

### 문제 및 해결
1. Minimal mistake테마를 적용한 gitpage의 home에서 rencet posts가 출력이 안됨 : 해결함   
    1. 해결 방법 : gitpage repository 최상위 디렉토리에 존재하는 index.markdown을 제거함.  
    2. 문제 설명 : Recent posts가 놓인 **home layout**에 게시물이 보이게 해주는 index.html과 같은 이름의 **index.markdown**이 같은 directory에 존재, index.html의 작동을 막았기 때문에 발생하는 문제였다.  
    3. 참고 링크 : [Disabling Recent Posts feature](https://github.com/mmistakes/minimal-mistakes/issues/1740)
  
