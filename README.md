# T2Sql
A simple sever to transfer Text to Sql language by LLM.

## Quick Start
### Requirements
```bash
pip install -r requirements.txt
```

### Set-up Sever
```bash
python set_up.py --model_name_or_path <your_model_path> --host <your_host> --port <your_port>
```
The sever will be set-up at `http://127.0.0.1:6006/sqlcoder/`

### Test
You can test the sever by running [test.py](./test.py).
```bash
python test.py
```

## Tips
We recommend using `sqlcoder` as LLM to transfer Text to Sql language.

## Reference
All work is based on the original [sqlcoder](https://github.com/defog-ai/sqlcoder).
Thanks to the tutorial of [FastAPI](https://fastapi.tiangolo.com/zh/)
