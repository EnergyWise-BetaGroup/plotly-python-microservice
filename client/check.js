const url = "http://localhost:3000"
 
const lineMountPoint = document.getElementById("line-mount-point")
const donutMountPoint = document.getElementById("donut-mount-point")
 
// const token = localStorage.getItem("token");
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyZWdpc3RyYXRpb25faWQiOjEsImlhdCI6MTc0MTAxODQzMSwiZXhwIjoxNzQxMDIyMDMxfQ.FUARa1zaVMLMrz6CjLmsjM5oV68ujaQQl0IEmd4kQgg"
 
async function fetchChart(chart ,mountPoint){
    options = {
        headers: {authorization: token}
    }
 
    const response = await fetch(`${url}/stats/${chart}`, options)
    const returnedData = await response.json()
 
    if(returnedData.html) {
        mountPoint.innerHTML = returnedData.html
    } else {
        console.error("Error fetching chart")
    }
 
    var scripts = mountPoint.getElementsByTagName("script");
    for(var i=0; i < scripts.length; i++) {
        eval(scripts[i].innerHTML);
    }
}

 
function fetchAllCharts() {
    fetchChart("line-graph", lineMountPoint)
    fetchChart("donut", donutMountPoint)
}
 
window.addEventListener("DOMContentLoaded", fetchAllCharts)