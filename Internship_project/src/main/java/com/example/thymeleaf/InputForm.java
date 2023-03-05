package com.example.thymeleaf;

import java.util.Objects;

public class InputForm {
    private String mainText;
    private String comFunc;
    private String funcName;
    private String expByText;
    private Integer expByLimit;

    private String output;

    public String getMainText() {
        return mainText;
    }

    public void setMainText(String mainText) {
        this.mainText = mainText;
    }

    public String getComFunc() {
        return comFunc;
    }

    public void setComFunc(String comFunc) {
        this.comFunc = comFunc;
    }

    public String getFuncName() {
        return funcName;
    }

    public void setFuncName(String funcName) {
        this.funcName = funcName;
    }

    public String getExpByText() {
        return expByText;
    }

    public void setExpByText(String expByText) {
        this.expByText = expByText;
    }

    public Integer getExpByLimit() {
        return Objects.requireNonNullElse(expByLimit, 0);
    }

    public void setExpByLimit(Integer expByLimit) {
        this.expByLimit = expByLimit;
    }

    public String getOutput() {
        return output;
    }

    public void setOutput(String output) {
        this.output = output;
    }
}
