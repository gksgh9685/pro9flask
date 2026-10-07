from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import get_connFunc

app = Flask(__name__);

@app.get('/')
def index():
    return render_template("index.html")

# 전체 직원 조회
@app.get('/acorn/jikwon')
def jikwon_list():
    sql = """
        select jikwonno,jikwonname,busername,jikwonjik,jikwonpay,
        year(jikwonibsail) as ibsayear
        from jikwon
        inner join buser on jikwon.busernum=buser.buserno
        order by jikwonno

    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()


    return jsonify({"ok":True, "data":rows})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000);