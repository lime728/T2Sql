import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
import argparse
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


class LlmModel(object):
    def __init__(self, model_name_or_path):
        self.tokenizer, self.model = self.get_tokenizer_model(model_name_or_path)
        self.prompt_file = self.read_file('prompt.md')
        self.metadata_file = self.read_file('metadata.sql')
        self.eos_token_id = self.tokenizer.convert_tokens_to_ids(["```"])[0]
        
    def change_metadata(self, metadata):
        self.metadata_file = metadata
        
    def read_file(self, path):
        with open(path, 'r') as f:
            file = f.read()
        return file
    
    def generate_prompt(self, question):
        prompt = self.prompt_file.format(
            user_question=question, table_metadata_string=self.metadata_file
        )
        return prompt
    
    def get_tokenizer_model(self, model_name):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
            use_cache=True,
        ).to('cuda')
        return tokenizer, model
    
    def run_inference(self, question):
        self.model.eval()
        prompt = self.generate_prompt(question)
        inputs = self.tokenizer(prompt, return_tensors="pt").to('cuda')
        output = self.model.generate(**inputs, 
                                     max_new_tokens=300, 
                                     do_sample=False, 
                                     num_beams=5,
                                     num_return_sequences=1,
                                     eos_token_id=self.eos_token_id,
                                     pad_token_id=self.eos_token_id,
                                    )
        result = self.tokenizer.decode(output[0]).split("```sql")[-1].split("```")[0].split(";")[0].strip() + ";"
        return result
    
    def test_qa():
        while True:
            question = input('Input:')
            if question == 'q':
                break
            print('Output:\n', SqlCoder.run_inference(question))
         
        
class Instruction(BaseModel):
    question: str = ""
    metadata: str = None
        
            
def sever(SqlCoder, host, port):
    app = FastAPI()
    
    app.add_middleware(
        CORSMiddleware,
        # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
        allow_origins=["*"],
        # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
        allow_credentials=False,
        # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
        allow_methods=["*"],
        # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
        # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
        allow_headers=["*"],
        # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
        # expose_headers=["*"]
        # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
        # max_age=1000
    )
    
    @app.post("/sqlcoder/")
    async def postdate(data: Instruction):  # 传入一个People类型的参数people
        item_dict = data.dict()
        metadata = item_dict['metadata']
        question = item_dict['question']
        if metadata:
            SqlCoder.change_metadata(metadata)
        output = SqlCoder.run_inference(question)
        return {"output": output}
    
    uvicorn.run(app=app, host=host, port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name_or_path', '-model_path', help='model name or path')
    parser.add_argument('--host', '-H', help='host to listen', default='127.0.0.1')
    parser.add_argument('--port', '-P', help='port of this service', default=6006)
    args = parser.parse_args()
    SqlCoder = LlmModel(args.model_name_or_path)
    sever(SqlCoder, args.host, args.port)
