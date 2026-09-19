package com.example.copilot;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Service;

@Service
public class EnterpriseTools {
 private final Map<String,Map<String,Object>> tickets=new ConcurrentHashMap<>();

 @Tool(description="Look up a customer by customer id. Read-only.")
 public Map<String,Object> getCustomer(String customerId){
  return Map.of("customerId",customerId,"name","Contoso","status","active");
 }

 @Tool(description="Create a support ticket. Priority critical requires approved=true.")
 public Map<String,Object> createTicket(String subject,String priority,boolean approved){
  if("critical".equalsIgnoreCase(priority)&&!approved)
   return Map.of("status","approval_required","reason","critical ticket requires approval");
  String id="T-"+UUID.randomUUID().toString().substring(0,8);
  var t=Map.<String,Object>of("ticketId",id,"subject",subject,"priority",priority,"status","created");
  tickets.put(id,t);return t;
 }

 @Tool(description="Get a support ticket by id. Read-only.")
 public Map<String,Object> getTicket(String ticketId){
  return tickets.getOrDefault(ticketId,Map.of("status","not_found"));
 }
}