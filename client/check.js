const mountPoint = document.getElementById("mount-point")

const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWdpc3RyYXRpb25faWQiOjEsImlhdCI6MTc0MTAxMzgxNywiZXhwIjoxNzQxMDE3NDE3fQ.PqdVrH-yHeiUWQcQ_UtW0ISGvVoUEbG003zBe_rI1Wg"

function mountChart(htmlData) {
    mountPoint.innerHTML = htmlData
}

async function fetchChart(){
    options = {
        headers: {authorization: token}
    }

    const response = await fetch("http://localhost:3000/stats/", options)
    const returnedData = await response.json()

    mountChart(returnedData.html)

    var scripts = mountPoint.getElementsByTagName("script");
    for(var i=0; i < scripts.length; i++) {
        eval(scripts[i].innerHTML);
    }
}

window.addEventListener("DOMContentLoaded", fetchChart)