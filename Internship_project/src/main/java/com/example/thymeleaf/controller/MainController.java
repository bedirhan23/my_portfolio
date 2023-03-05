package com.example.thymeleaf.controller;

import com.example.thymeleaf.Converter;
import com.example.thymeleaf.InputForm;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class MainController {

    Converter c = new Converter();

    @GetMapping("/inputForm")
    public String showForm(Model model) {
        InputForm inputForm = new InputForm();
        model.addAttribute("inputText", inputForm);
        return "inputForm";
    }

    @PostMapping("/service/textprocess")
    public String submitForm(@ModelAttribute InputForm inputForm, Model model){
        String output = c.convert(inputForm);
        inputForm.setOutput(output);
        model.addAttribute("inputText", inputForm);
        return "service/textprocess";
    }
}
