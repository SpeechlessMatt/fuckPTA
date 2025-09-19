// :s0
#include <iostream>
#include <string>
using namespace std;
// :s0

// :s1
#define COND 'a'
#define INPUT_INDEX 10
#define EFFECTIVE_LEN_MAX 10
#define EFFECTIVE_LEN 10
// :s1

// :f1
int le_logic_unit(string text, int effective[], int effective_len){
    for (int i = 0; i < effective_len; i++){
        int j = effective[i];
        if (text[j] > COND){
            return 0;
        }
    }
    return 1;
}
// :f1

// :f2
int get_len_unit(string text, int effective[], int effective_len){
    if (effective[0] <= text.length() && text.length() < effective[0] + effective_len)
        return 1;
    return 0;
}
// :f2

// :m
int main(){
    string inp;
    for (int i = 0; i < INPUT_INDEX; i++){
        cin>>inp;
    }
    int effective_list[EFFECTIVE_LEN_MAX] = {0};
    if (le_logic_unit(inp, effective_list, EFFECTIVE_LEN) == 1){
        return 1;
    }else{
        return 0;
    }
}
// :m

// :m2
int main(){
    string inp;
    for (int i = 0; i < INPUT_INDEX; i++){
        cin>>inp;
    }
    int effective_list[EFFECTIVE_LEN_MAX] = {0};
    if (get_len_unit(inp, effective_list, EFFECTIVE_LEN) == 1){
        return 1;
    }else{
        return 0;
    }
}
// :m2
