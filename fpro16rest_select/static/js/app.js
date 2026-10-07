const btnJikwon = document.querySelector("#btnJikwon");
const btnOne = document.querySelector("#btnOne");
const btnBuser = document.querySelector("#btnBuser");
const btnBuserPart = document.querySelector("#btnBuserPart");

const Jikwonno = document.querySelector("#Jikwonno");
const Buserno = document.querySelector("#Buserno");

const msg = document.querySelector("#msg");
const tbody = document.querySelector("#tbody");
const thead = document.querySelector("#thead");

function setMsg(text){
    msg.textContent = text;
}

function clearTable(){
    thead.innerHTML = "";
    tbody.innerHTML = "";
}

function makeTable(rows){
    clearTable();

    if(!rows || rows.length === 0){
        setMsg("자료 없음");
        return;
    }

    let header = "<tr>";
    Object.keys(rows[0]).forEach(key => {
        header += "<th>" + key + "</th>"
    })
    header += "</tr>"
    thead.innerHTML = header;

    rows.forEach(r => { 
        let tr = "<tr>";
        Object.values(r).forEach(v => {
            tr += "<td>" + v + "</td>"
        })
        tr += "</tr>"
        tbody.innerHTML += tr;
    })
}


// 전체 직원
async function loadJikwon(){
    const res = await fetch("/acorn/jikwon");
    const mydata = await res.json();
    makeTable(mydata.data);

    setMsg("전체 직원 조회 완료")
}

btnJikwon.onclick = loadJikwon;   // 괄호 치지말고 함수의 결과를 넘겨줘야 함