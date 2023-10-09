import os

import fire
import torch
from peft import PeftModel
from transformers import LlamaForCausalLM, LlamaTokenizer, BloomForCausalLM, AutoTokenizer, AutoModelForCausalLM


def export_hf(BASE_MODEL: str = '',
              cache_dir: str = '',
              lora_weights: str = '',
              save_dir: str = '',
              load_in_8bit: bool = False,
              max_shard_size: str = "400MB"):
    # 读取模型
    if 'llama' in BASE_MODEL.lower():
        base_model = LlamaForCausalLM.from_pretrained(BASE_MODEL, cache_dir=cache_dir, load_in_8bit=load_in_8bit,
                                                      torch_dtype=torch.float16, device_map={"": "cpu"}, )
    elif 'bloom' in BASE_MODEL.lower():
        base_model = BloomForCausalLM.from_pretrained(BASE_MODEL, cache_dir=cache_dir, load_in_8bit=load_in_8bit,
                                                      torch_dtype=torch.float16, device_map={"": "cpu"}, )
    else:
        base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, cache_dir=cache_dir, load_in_8bit=load_in_8bit,
                                                          torch_dtype=torch.float16, device_map={"": "cpu"}, )
    lora_model = PeftModel.from_pretrained(base_model, lora_weights, device_map={"": "cpu"},
                                           torch_dtype=torch.float16, )

    # 读取Tokenizer
    if 'llama' in BASE_MODEL.lower():
        tokenizer = LlamaTokenizer.from_pretrained(BASE_MODEL, cache_dir=cache_dir)
    else:
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, cache_dir=cache_dir)

    # 合并参数

    model = lora_model.merge_and_unload()
 
    print(f"Saving the target model to {output_path}")
    model.save_pretrained(os.path.join(save_dir, "hf_ckpt"))
    tokenizer.save_pretrained(os.path.join(save_dir, "hf_ckpt"))
    print('合并完成')

if __name__ == '__main__':
    fire.Fire(export_hf)
