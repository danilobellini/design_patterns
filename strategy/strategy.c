#include <stdio.h>

typedef int (*BinaryOpPtr)(int, int);

typedef struct{
  BinaryOpPtr func;
  char symbol;
} Strategy;

int sum(int a, int b){ return a + b; }
int sub(int a, int b){ return a - b; }
int mul(int a, int b){ return a * b; }

int apply(Strategy st, int a, int b){
  return st.func(a, b);
}

Strategy strategies[] = {{sum, '+'}, {sub, '-'}, {mul, '*'}};

int main(){
  Strategy st;
  int idx;
  for(idx = 0; idx < 3; idx++){
    st = strategies[idx];
    printf("2 %c 3 = %d\n", st.symbol, apply(st, 2, 3));
    printf("7 %c 5 = %d\n", st.symbol, apply(st, 7, 5));
  }
  return 0;
}

