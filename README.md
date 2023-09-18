# T2Sql
A simple sever to transfer Text to Sql language by LLM.

## Quick Start
### Requirements
```bash
pip install -r requirements.txt
```

### Set-up Sever
```bash
python set_up.py --model_name_or_path <your_model_path[required]> --host <your_host[optional]> --port <your_port[optional]>
```
The sever will be set-up at `http://127.0.0.1:6006/sqlcoder/`.

### Test
You can test the sever by running [test.py](./test.py).
```bash
python test.py --host <your_host[optional]> --port <your_port[optional]>
```

## fine-tune
We provide method `lora` to fine-tune the LLM. You could fine-tune the model after adding your data. Please note that the data should be alpaca-lora template.
```json
{
  "instruction": "your instruction",
  "input": "your input",
  "output": "your output"
}
```
You can start fine-tune by running [finetune.py](./finetune/finetune.py).
```bash
python ./finetune/finetune.py --data_path <your_data_path> --base_model <your_model_path> --output_dir <your_output_dir>
```
Also you can use [merge_llama_with_lora.py](./finetune/merge_llama_with_lora.py) to get merged weights.
```bash
python ./finetune/merge_llama_wth_lora.py --base_model <your_model_path> --lora_model <your_lora_model_path> --output_type huggingface --output_dir <your_output_dir>
```

## Tips
We recommend using `sqlcoder` as LLM to transfer Text to Sql language.

## Reference
Model weights are based on the original [sqlcoder](https://github.com/defog-ai/sqlcoder).
Thanks to the tutorial of [FastAPI](https://fastapi.tiangolo.com/zh/).
Thanks to [alpaca-lora](https://github.com/tloen/alpaca-lora) and [Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca).
