#!/usr/bin/env python3
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).parent / "todos.json"


def load_todos():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save_todos(todos):
    DATA_FILE.write_text(json.dumps(todos, ensure_ascii=False, indent=2))


def add(title):
    todos = load_todos()
    next_id = max((t["id"] for t in todos), default=0) + 1
    todos.append({"id": next_id, "title": title, "done": False})
    save_todos(todos)
    print(f"追加しました: [{next_id}] {title}")


def list_todos():
    todos = load_todos()
    if not todos:
        print("タスクがありません")
        return
    for t in todos:
        mark = "x" if t["done"] else " "
        print(f"[{mark}] {t['id']}. {t['title']}")


def done(id_):
    todos = load_todos()
    for t in todos:
        if t["id"] == id_:
            t["done"] = True
            save_todos(todos)
            print(f"完了しました: {t['title']}")
            return
    print(f"ID {id_} が見つかりません")


def delete(id_):
    todos = load_todos()
    new_todos = [t for t in todos if t["id"] != id_]
    if len(new_todos) == len(todos):
        print(f"ID {id_} が見つかりません")
        return
    save_todos(new_todos)
    print(f"削除しました: ID {id_}")


def usage():
    print("使い方:")
    print("  python todo.py add <タスク名>   タスクを追加")
    print("  python todo.py list             タスク一覧を表示")
    print("  python todo.py done <ID>        タスクを完了にする")
    print("  python todo.py delete <ID>      タスクを削除")


def main():
    args = sys.argv[1:]
    if not args:
        usage()
        return

    cmd = args[0]

    if cmd == "add":
        if len(args) < 2:
            print("エラー: タスク名を指定してください")
        else:
            add(" ".join(args[1:]))
    elif cmd == "list":
        list_todos()
    elif cmd == "done":
        if len(args) < 2:
            print("エラー: IDを指定してください")
        else:
            done(int(args[1]))
    elif cmd == "delete":
        if len(args) < 2:
            print("エラー: IDを指定してください")
        else:
            delete(int(args[1]))
    else:
        print(f"不明なコマンド: {cmd}")
        usage()


if __name__ == "__main__":
    main()
