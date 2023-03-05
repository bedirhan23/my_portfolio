package com.example.thymeleaf;

import com.example.thymeleaf.InputForm;

import java.util.ArrayList;

public class Converter{
    private String unwanted(String txt, String unwantedStr, String funcName) {

        String newTxt = txt.replaceAll(unwantedStr, funcName);
        return newTxt;
    }
    private ArrayList<String> split(String txt, int n, boolean isSame) {
        ArrayList<String> words = new ArrayList<>();
        if(isSame) {
            for(int i = 1; i < txt.length()-1; i += n) {
                String subStr = txt.substring(i, Math.min(txt.length()-1, i+ n));
                words.add(subStr);
            }
        }
        else {
            for(int i = 0; i < txt.length(); i += n) {
                String subStr = txt.substring(i, Math.min(txt.length(), i+ n));
                words.add(subStr);
            }
        }
        return words;
    }
    private boolean check(String text) {
        if(text.charAt(0) == text.charAt(text.length()-1)) {
            return true;
        }
        return false;

    }
    private String concatedWoLimit(String txt, String expByText, String funcName ) {
        String x = unwanted(txt, expByText, funcName);
        return x;

    }
    private String concated(int lmt, String text, String oper, String funcName ) {
        String x = "";
        String firstL = ""+text.charAt(0);

        if(check(text)) {
            ArrayList<String> words = split(text, lmt, true);
            for(int i = 0; i < words.size(); i++) {
                x = x.concat(funcName);
                x = x.concat("(");
                x = x.concat(firstL);
                x = x.concat(words.get(i));
                x = x.concat(firstL);
                x = x.concat(")");
                if(i < words.size()-1) {
                    x = x.concat(oper);
                }
            }
            return x;
        }
        else {
            ArrayList<String> words = split(text, lmt, false);
            for(int j = 0; j < words.size(); j++) {
                x = x.concat(funcName);
                x = x.concat("(");
                x = x.concat(words.get(j));
                x = x.concat(")");
                if(j < words.size()-1) {
                    x = x.concat(oper);
                }
            }
            return x;
        }
    }
    public String convert(InputForm inputForm){
        String text = inputForm.getMainText();
        String comFunc = inputForm.getComFunc();
        String funcName = inputForm.getFuncName();
        String expByText = inputForm.getExpByText();
        int expByLimit = inputForm.getExpByLimit();
        if(expByLimit <= 0) {
            return concatedWoLimit(text, expByText, funcName);
        }
        else {
            return concated(expByLimit, text, comFunc, funcName);
        }
    }
}
