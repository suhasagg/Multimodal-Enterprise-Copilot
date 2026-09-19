package com.example.copilot;
import java.io.IOException;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.util.MimeType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/multimodal")
public class MultimodalController {
 private final ChatClient chat;
 public MultimodalController(ChatClient.Builder builder){this.chat=builder.build();}

 @PostMapping(value="/image",consumes=MediaType.MULTIPART_FORM_DATA_VALUE)
 public String image(@RequestParam String question,@RequestPart MultipartFile image) throws IOException {
  MimeType type=MimeType.valueOf(image.getContentType()==null?"image/png":image.getContentType());
  var resource=new ByteArrayResource(image.getBytes());
  return chat.prompt().user(u->u.text(question).media(type,resource)).call().content();
 }
}