#include <stdio.h>

#define str_size 1000

char str[str_size];
FILE *belge;
int counter = 0, sayivarmi = 0, kacincisayi = 0, satir = 0, sutun = 0, i = 0, j = 0,gecicisatir = 0, gecicisutun = 0;
char gecicisayiarray[50];
int **matris;

int main(void){
    while(i < str_size){
    	str[i] = -1;
		i++;
	}
	i=0;
	belge = fopen("matrix.txt","r");
	while(i == 0){
		str[j] = fgetc(belge);
		if(str[j] == -1){
			i = 1;
		}
		j++;
	}
    i = 0;
    j = 0; 
    fclose(belge);
    while (str[counter] !=  -1){
		while(((int) str[counter]) >= 48 && ((int) str[counter]) <= 57){
			gecicisayiarray[sayivarmi] = str[counter];
			sayivarmi++;
			counter++;
		}
		if(sayivarmi != 0){
		   	if(kacincisayi == 0){
		   		satir = atoi(gecicisayiarray);
				kacincisayi++;
				sayivarmi = 0;
			}
			else if(kacincisayi == 1){
				sutun = atoi(gecicisayiarray);
				kacincisayi++;
				sayivarmi = 0;
				matris = (int **)malloc(satir * sizeof(int *));
			    while (i < satir){
			         matris[i] = (int *)malloc(sutun * sizeof(int)); 
					i++;
				}
				i=0;
				while (i <  satir){
			      	while (j < sutun){
			         	matris[i][j] = 0;
			        	j++;;
					}
					j=0;
			        i++;
			    }
			    i=0;
			    j=0;
			}
			else{
				if(kacincisayi % 3 == 0){
					gecicisutun = atoi(gecicisayiarray);
				}
				else if(kacincisayi % 3 == 1){
					matris[gecicisatir][gecicisutun] = atoi(gecicisayiarray);
					printf("row: %d\ncol: %d, val: %d\n", gecicisatir, gecicisutun, matris[gecicisatir][gecicisutun]);
					gecicisatir = 0;
					gecicisutun = 0;
				}
				else {
					gecicisatir = atoi(gecicisayiarray);
				}
				kacincisayi++;
				sayivarmi=0;
			}
			while(i<50){
				gecicisayiarray[i] = ' ';
				i++;
			}
			i=0;
		}
        counter ++;
    }
	counter = 0;
    return 0;
} 