package com.example.copilot;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
class EnterpriseToolsTest {
 @Test void criticalNeedsApproval(){
  var r=new EnterpriseTools().createTicket("outage","critical",false);
  assertEquals("approval_required",r.get("status"));
 }
}