#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define str_size 1000

char str[str_size];
char prepositions[] = "inIntoToatAtofOfforForfromFrom";
int counter = 0, word = 1, sec_counter = 0, preposition = 1, sentence = 1, i = 0, k = 0, h = 0, sayivarmi = 0, kacincisayi = 0;
int degerler[]={0, 2, 2, 2, 4, 2, 6, 2, 8, 2, 10, 2, 12, 2, 14, 2, 16, 3, 19, 3, 22, 4, 26, 4};
int sayilar[50];
char gecicisayiarray[50];
FILE *belge;
char karakter[50];

int stringkontrol(int ilkchar, int uzunluk, int kontrol){
	i = 0;
	while(i < uzunluk){
		if(str[kontrol+i] != prepositions[ilkchar+i]){
			return 0;
		}
		i++;
	}
	return 1;
}

void kontrolzamani(int b){
	k = 0;
	while(k < 24){
		if (stringkontrol(degerler[k], degerler[k+1], b) != 0){
			if( str[b+degerler[k+1]] == ' ' || str[b+degerler[k+1]]  == '\n' || str[b+degerler[k+1]] == '\t' || str[b+degerler[k+1]] == '\0' || str[b+degerler[k+1]] == '.'){
				preposition++;
			}
		}
		k = k + 2;
	}
}

int main(void){

    printf("Please enter a text file: ");
    scanf("%s",karakter);
    belge = fopen(karakter,"r");
    fgets(str, str_size ,belge);
    puts(str);
    fclose(belge);
    while (str[counter] !=  '\0')
    {
        if( str[counter] == ' ' || str[counter]  == '\n' || str[counter] == '\t'){
            word++;
        }
        else if( str[counter] == '.'){
        	sentence++;
		}
        counter ++;
    }
    while (str[sec_counter] != '\0')
    {
    	while(((int) str[sec_counter]) >= 48 && ((int) str[sec_counter]) <= 57){
			gecicisayiarray[sayivarmi] = str[sec_counter];
			sayivarmi++;
			sec_counter++;
		}
		if(sayivarmi != 0){
	    	sayilar[kacincisayi] = atoi(gecicisayiarray);
			kacincisayi++;
			sayivarmi = 0;	
		}
    	if(sec_counter == 0){
    		kontrolzamani(sec_counter);
		}
		else if(sec_counter > 0){
    		if( str[sec_counter] == ' ' || str[sec_counter]  == '\n' || str[sec_counter] == '\t'){
				kontrolzamani(sec_counter+1);
        	}
    	}
        sec_counter ++;
    }
    
    printf("Total number of words in the sentences: %d\n", word-1);  
    printf("Total number of sentences in the text: %d\n", sentence-1);
	printf("Total number of prepositions in the sentences: %d\n ", preposition-1);
	printf("Numbers: ");
	while(h < kacincisayi){
		printf("%d ", sayilar[h]);
		h++;
	}
}