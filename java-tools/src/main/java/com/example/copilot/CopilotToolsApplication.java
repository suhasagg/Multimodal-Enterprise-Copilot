package com.example.copilot;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
@SpringBootApplication
public class CopilotToolsApplication {
 public static void main(String[] args){SpringApplication.run(CopilotToolsApplication.class,args);}
 @Bean ToolCallbackProvider tools(EnterpriseTools t){
  return MethodToolCallbackProvider.builder().toolObjects(t).build();
 }
}