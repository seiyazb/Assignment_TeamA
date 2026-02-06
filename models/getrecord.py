import pymysql

# データベース接続取得
def get_connection():
    return pymysql.connect(
    host='localhost',
    user='root',
    password='1022',
    database='app_assiggnment',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
    )

# records検索
def fetch_by_id(record_id):
    """IDを基にrecordsテーブルから1件取得する"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM pyapp WHERE id = %s"
            cursor.execute(sql, (record_id,))
            return cursor.fetchone()
