from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
from db import get_connFunc

app = Flask(__name__);


def validate_product(data, include_code=False):
    if not isinstance(data, dict):
        raise ValueError("올바른 JSON 객체를 전달하세요.")
    sang = data.get("sang")
    if not isinstance(sang, str) or not sang.strip():
        raise ValueError("상품명은 필수입니다.")
    numbers = []
    for key in (["code", "su", "dan"] if include_code else ["su", "dan"]):
        value = data.get(key)
        if isinstance(value, bool) or not str(value).isascii() or not str(value).isdecimal():
            raise ValueError(f"{key}는 0 이상의 정수여야 합니다.")
        numbers.append(int(value))
    if include_code:
        return numbers[0], sang.strip(), numbers[1], numbers[2]
    return sang.strip(), numbers[0], numbers[1]


@app.errorhandler(pymysql.MySQLError)
def database_error(err):
    app.logger.error("Database request failed: %s", err)
    return jsonify({"ok": False, "msg": "DB 요청에 실패했습니다."}), 500


@app.get("/")
def index():
    return render_template("index.html")

"""
상품 CRUD라면 보통 이렇게 구성
GET    /api/sangdata       전체조회
GET    /api/sangdata/1     1번 상품 조회
POST   /api/sangdata       상품 추가
PUT    /api/sangdata/1     1번 상품 수정
DELETE /api/sangdata/1     1번 상품 삭제
"""

# 전체 자료 읽기
@app.get("/api/sangdata")
def list_sangdata():
    sql = "select code,sang,su,dan from sangdata order by code asc"

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return jsonify({"ok":True, "datas":rows})

# 새 상품 추가(insert)
@app.post("/api/sangdata")
def create_sangdata():
    data = request.get_json(silent=True)
    try:
        code, sang, su, dan = validate_product(data, include_code=True)
    except ValueError as err:
        return jsonify({"ok": False, "msg": str(err)}), 400
    isql = "insert into sangdata(code,sang,su,dan) values(%s,%s,%s,%s)"

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(isql, (code,sang,su,dan))

    return jsonify({"ok":True})

# 상품 수정
@app.put("/api/sangdata/<int:code>")
def update_sangdata(code):
    data = request.get_json(silent=True)
    try:
        sang, su, dan = validate_product(data)
    except ValueError as err:
        return jsonify({"ok": False, "msg": str(err)}), 400
    usql = "update sangdata set sang=%s,su=%s,dan=%s where code=%s"

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute("select code from sangdata where code=%s", (code,))
            if cur.fetchone() is None:
                return jsonify({"ok": False, "msg": "해당 자료 없음"}), 404
            cur.execute(usql, (sang,su,dan,code))

    return jsonify({"ok":True})


# 상품 삭제
@app.delete("/api/sangdata/<int:code>")
def delete_sangdata(code):
    try:
        dsql = "delete from sangdata where code=%s"

        with get_connFunc() as conn:
            with conn.cursor() as cur:
                cur.execute(dsql, (code,))
                if cur.rowcount == 0:
                    return jsonify({"ok":False, "msg":"해당 자료 없음"})

        return jsonify({"ok":True, "msg":"삭제 완료"})
    except Exception as err:
        return jsonify({"ok":False, "msg":str(err)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);
