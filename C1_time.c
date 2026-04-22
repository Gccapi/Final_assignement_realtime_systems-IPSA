#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int multi(int x,int y){
	
	return (int)x*y;
	}

int main(){
	srand(time(NULL));
	int long long a;
	for (int i =0; i<20000000; i++){ 	
		int x = rand() %10000000 +100000 ;
		int y = rand() %10000000 +100000 ;
		a = multi(x,y);
	}
	
	
	return 0; 	
	}
