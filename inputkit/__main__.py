import argparse
import json
from . import load_corpus

p = argparse.ArgumentParser(description="检查本地业务资料的字段、类型和引用")
p.add_argument("directory", nargs="?", default="data")
a = p.parse_args()
tables = load_corpus(a.directory)
print(json.dumps({name: len(rows) for name, rows in tables.items()}, ensure_ascii=False, indent=2))
