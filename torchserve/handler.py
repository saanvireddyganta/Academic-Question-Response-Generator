import json, torch
from ts.torch_handler.base_handler import BaseHandler
from transformers import AutoTokenizer, AutoModelForCausalLM
class AcademicHandler(BaseHandler):
    def initialize(self, context):
        d=context.system_properties.get("model_dir")
        self.device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tok=AutoTokenizer.from_pretrained(d)
        self.model=AutoModelForCausalLM.from_pretrained(d).to(self.device)
        if self.tok.pad_token_id is None: self.tok.pad_token=self.tok.eos_token
        self.model.eval(); self.initialized=True
    def preprocess(self,data):
        x=data[0]
        if isinstance(x,(bytes,bytearray)): x=x.decode()
        if isinstance(x,str): x=json.loads(x)
        if isinstance(x,dict) and "body" in x:
            x=x["body"]
            if isinstance(x,(bytes,bytearray)): x=x.decode()
            if isinstance(x,str): x=json.loads(x)
        if not isinstance(x,dict): raise ValueError("Request must be a JSON object.")
        p=x.get("prompt"); n=x.get("max_new_tokens",60)
        if not isinstance(p,str) or not p.strip(): raise ValueError("prompt is required.")
        if len(p)>12000: raise ValueError("Question is too long.")
        if not isinstance(n,int) or isinstance(n,bool) or not 20<=n<=150: raise ValueError("max_new_tokens must be 20 to 150.")
        text="Explain this academic topic in simple terms. Topic: "+p.strip()+"\nExplanation:"
        e=self.tok(text,return_tensors="pt",truncation=True,max_length=900)
        return {"ids":e["input_ids"].to(self.device),"mask":e["attention_mask"].to(self.device),"n":n}
    def inference(self,x):
        with torch.inference_mode():
            out=self.model.generate(input_ids=x["ids"],attention_mask=x["mask"],max_new_tokens=x["n"],do_sample=True,temperature=.7,top_p=.9,pad_token_id=self.tok.eos_token_id)
        return self.tok.decode(out[0,x["ids"].shape[1]:],skip_special_tokens=True).strip()
    def postprocess(self,x): return [{"generated_text":x,"model":"distilgpt2"}]
