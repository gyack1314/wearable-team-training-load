from __future__ import annotations

import csv
from datetime import date, datetime
import json
import math
from pathlib import Path


def convert(value, column):
    if value == "":
        if column["nullable"]:
            return None
        raise ValueError("必填字段为空 " + column["name"])
    kind = column["type"]
    if kind == "int":
        return int(value)
    if kind == "float":
        number = float(value)
        if not math.isfinite(number):
            raise ValueError("数值必须有限")
        return number
    if kind == "date":
        return date.fromisoformat(value)
    if kind == "datetime":
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            raise ValueError("时间戳缺少时区")
        return parsed
    if kind == "str":
        return value
    raise ValueError("未知字段类型 " + kind)


def read_table(path, definition):
    columns = definition["columns"]
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != [column["name"] for column in columns]:
            raise ValueError("列名或列顺序不符合资料契约 " + str(path))
        result = []
        seen = set()
        for raw in reader:
            if None in raw or any(value is None for value in raw.values()):
                raise ValueError("记录字段数不正确 " + str(path))
            row = {column["name"]: convert(raw[column["name"]], column) for column in columns}
            key = row[definition["primary_key"]]
            if key in seen:
                raise ValueError("重复物理记录键 " + str(key))
            seen.add(key)
            result.append(row)
    return result


def load_corpus(directory):
    directory = Path(directory)
    schema = json.loads((directory / "schema.json").read_text(encoding="utf-8"))
    tables = {name: read_table(directory / (name + ".csv"), table) for name, table in schema["tables"].items()}
    for name, table in schema["tables"].items():
        for column, target in table.get("references", {}).items():
            target_table, target_column = target.split(".")
            keys = {row[target_column] for row in tables[target_table]}
            if any(row[column] is not None and row[column] not in keys for row in tables[name]):
                raise ValueError("资料引用不存在 " + name + "." + column)
    json.loads((directory / "terms.json").read_text(encoding="utf-8"))
    return tables
