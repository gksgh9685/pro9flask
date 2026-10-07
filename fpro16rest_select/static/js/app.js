const btnJikwon = document.querySelector('#btnJikwon');
const btnOne = document.querySelector('#btnOne');
const btnBuser = document.querySelector('#btnBuser');
const btnBuserPart = document.querySelector('#btnBuserPart');

const jikwonno = document.querySelector('#jikwonno');
const buserno = document.querySelector('#buserno');


const msg = document.querySelector('#msg');
const thead = document.querySelector('#thead');
const tbody = document.querySelector('#tbody');

function setMsg(text){
    msg.textContent = text;
}

function clearTable(){
    thead.innerHTML ='';
    tbody.innerHTML ='';
}

function makeTable(rows){
    clearTable();

    if(!rows || rows.length === 0){
        setMsg('자료 없음');
        return;
    }

    let header ='<tr>';
    Object.keys(rows[0]).forEach(key => {
        header += '<th>' + key + '<th>';
    });
    header += '<tr>';
    thead.innerHTML = header;

    rows.forEach(r => {
        let tr = '<tr>';
        Object.values(r).forEach(key => {
            tr += '<td>' + key + '<td>';
        });
        tr += '</tr>';
        tbody.innerHTML += tr;
    });
}