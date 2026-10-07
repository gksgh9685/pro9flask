const code = document.querySelector("#code");
const sang = document.querySelector("#sang");
const su = document.querySelector("#su");
const dan = document.querySelector("#dan");
const msg = document.querySelector("#msg");
const tbody = document.querySelector("#tbody");

function setMsg(text) { msg.textContent = text; }
function clearForm() {
    [code, sang, su, dan].forEach(input => { input.value = ""; });
    code.focus();
}
async function api(url, options = {}) {
    const res = await fetch(url, options);
    const data = await res.json();
    if (!res.ok || !data.ok) throw new Error(data.msg || "요청 실패");
    return data;
}
async function loadAll(showMessage = true) {
    const data = await api("/api/sangdata");
    tbody.replaceChildren();
    data.datas.forEach(row => {
        const tr = document.createElement("tr");
        [row.code, row.sang, row.su, row.dan].forEach(value => {
            const td = document.createElement("td");
            td.textContent = value;
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    if (showMessage) setMsg("조회 완료");
}
async function saveData(method) {
    const productCode = code.value.trim();
    if (!/^\d+$/.test(productCode) || !sang.value.trim() ||
        !/^\d+$/.test(su.value.trim()) || !/^\d+$/.test(dan.value.trim())) {
        setMsg("코드, 수량, 단가는 0 이상의 정수이며 상품명은 필수입니다.");
        return;
    }
    const data = {sang: sang.value.trim(), su: su.value.trim(), dan: dan.value.trim()};
    if (method === "POST") data.code = productCode;
    await api("/api/sangdata" + (method === "PUT" ? "/" + productCode : ""), {
        method, headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)
    });
    clearForm();
    await loadAll(false);
    setMsg(method === "POST" ? "추가 완료" : "수정 완료");
}
async function deleteData() {
    if (!/^\d+$/.test(code.value.trim())) {
        setMsg("삭제할 상품 코드를 숫자로 입력하세요.");
        code.focus();
        return;
    }
    const data = await api("/api/sangdata/" + code.value.trim(), {method: "DELETE"});
    clearForm();
    await loadAll(false);
    setMsg(data.msg);
}
function run(action) {
    return async () => {
        try { await action(); }
        catch (err) { setMsg("오류: " + err.message); }
    };
}
window.addEventListener("load", run(() => loadAll()));
document.querySelector("#btnAdd").onclick = run(() => saveData("POST"));
document.querySelector("#btnUpdate").onclick = run(() => saveData("PUT"));
document.querySelector("#btnDelete").onclick = run(deleteData);
