import json
from datetime import datetime
from tkinter import messagebox
from getrecord import fetch_by_id

def _get_formatted_data(record_id):
    record = fetch_by_id(record_id)
    if not record:
        messagebox.showerror("エラー", "対象のデータが見つかりません")
        return None, None
    try:
        meta = json.loads(record.get('meta_json', '{}'))
    except (json.JSONDecodeError, TypeError):
        meta = {}
    return record, meta

def _build_lines(record, meta, style):
    rec_type = record.get('type')
    lines = []
    
    # スタイル定義 (太字開始, 太字終了, リスト記号)
    styles = {
        "slack":  ("*", "*", "・"),
        "jira":   ("", "", "・"),
        "notion": ("**", "**", "- ")
    }
    b_s, b_e, l_p = styles.get(style)

    if rec_type == "standup":
        date = meta.get('date') or datetime.now().strftime('%Y-%m-%d')
        lines.append("### 🗓️ 日報" if style == "notion" else f"{b_s}【日報】{b_e}")
        items = [("日付", date), ("昨日やったこと", meta.get('done')), ("今日やること", meta.get('today')), ("困りごと", meta.get('blocker')), ("チケット番号", meta.get('ticket'))]
    
    elif rec_type == "handover":
        lines.append("### 引継ぎ" if style == "notion" else f"{b_s}【引継ぎ】{b_e}")
        items = [("タイトル", record.get('title')), ("背景", meta.get('context')), ("現状", meta.get('current')), ("次アクション", meta.get('next')), ("注意点", meta.get('notes')), ("参考リンク", meta.get('links'))]
    
    elif rec_type == "incident":
        lines.append("### 障害/問い合わせ報告" if style == "notion" else f"{b_s}【障害/問い合わせ報告】{b_e}")
        items = [("現象", meta.get('summary')), ("影響範囲", meta.get('impact')), ("環境", meta.get('env')), ("再現手順", meta.get('repro_steps')), ("確認済みログ", meta.get('logs_checked')), ("仮説", meta.get('hypothesis'))]
    
    else:
        return [f"{b_s}{rec_type}{b_e}", record.get('body', '内容なし')]

    for label, value in items:
        lines.append(f"{l_p}{b_s}{label}:{b_e} {value or 'なし'}")
    
    return lines

def _copy_to_clipboard(root, lines, msg):
    root.clipboard_clear()
    root.clipboard_append("\n".join(lines))
    messagebox.showinfo("完了", msg)

def copy_to_slack(root, record_id):
    res = _get_formatted_data(record_id)
    if res[0]: _copy_to_clipboard(root, _build_lines(res[0], res[1], "slack"), "Slack形式でコピーしました")

def copy_to_jira(root, record_id):
    res = _get_formatted_data(record_id)
    if res[0]: _copy_to_clipboard(root, _build_lines(res[0], res[1], "jira"), "Jira形式でコピーしました")

def copy_to_notion(root, record_id):
    res = _get_formatted_data(record_id)
    if res[0]: _copy_to_clipboard(root, _build_lines(res[0], res[1], "notion"), "Notion形式でコピーしました")