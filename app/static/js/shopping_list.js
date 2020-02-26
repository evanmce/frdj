async function removeItem(item_id) {
    let response = await fetch(`/shopping_list?item_id=${item_id}`, {
        method: "PUT"
    });
    let element = document.getElementById(`item_id${item_id}`);
    element.parentNode.removeChild(element);
}

window.addEventListener("DOMContentLoaded", function() {
    console.log("on load event");
    let result = document.getElementsByTagName("form");
    result[0].addEventListener("submit", async function(event) {
        console.log("event listener");
        event.preventDefault();
        let request_data = new FormData(event.target);
        let request = new XMLHttpRequest();
        request.open("POST", "/shopping_list");
        request.send(request_data);

        request.onreadystatechange = async function() {
            if (request.readyState === XMLHttpRequest.DONE) {
                if (request.status === 200) {
                    console.log(request.response);
                    let data = JSON.parse(request.response);
                    console.log(data);
                    let element = document.createElement("a");
                    element.id = data["item_id"];
                    element.setAttribute("href","#");
                    element.setAttribute("type","checkbox");
                    element.setAttribute("class","list-group-item list-group-item clearfix align-center");
                    element.innerHTML =
                    `${data["item_name"]}
                    <span class="pull-right">
                        <button type="button" class="btn btn-sm btn-success">
                            <i class="fas fa-check"></i>
                        </button>
                        <button type="button" class="btn btn-sm btn-warning">
                            <i class="fas fa-pen"></i>
                        </button>
                        <button type="button" class="btn btn-sm btn-danger" onclick="removeItem(${data["item_id"]})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </span>`;
                    document.getElementById("shopping_list_container").appendChild(element);
                }
            }
        }       
    });
});