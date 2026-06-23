
const currentUserId = localStorage.getItem("user_id");
fetch(`http://localhost:5000/api/tasks?user_id=${currentUserId}`)
.then(response => response.json())
.then(data => {
    console.log(data);
    listTasks(data.tasks);
})
.catch(error => {
    console.error(error);
});

function openView2(mode, taskID){
    if (mode == 0){
        window.location.href = `viewtask.html?task_id=${taskID}`;
function loadTaskList(){

    const currentUserId = localStorage.getItem("user_id");
    fetch(`http://localhost:5000/api/tasks?user_id=${currentUserId}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        listTasks(data.tasks);
    })
    .catch(error => {
        console.error(error);
    });
}
    function openView(mode, taskID){
        if (mode == 0){
            window.location.href = `viewtask.html?task_id=${taskID}`;

        }
        else if (mode == 1){
            window.location.href = `edittask.html?task_id=${taskID}`;
        }
        else if (mode == 2){
            alert("Delete task " + taskID);
        }
    }

function loadTask(){
    const params = new URLSearchParams(window.location.search);
    const taskId = params.get("task_id");

    fetch(`http://localhost:5000/api/tasks/${taskId}`)
    .then(response => response.json())
    .then(task => {
        document.getElementById("title").innerHTML = task.title;
        document.getElementById("desc").innerHTML = task.description;
        document.getElementById("date").innerHTML = task.date;
        document.getElementById("category").innerHTML = task.category;
        document.getElementById("priority").innerHTML = task.priority;

        if (task.completed){
            document.getElementById("complete").innerHTML = "Completed";
        }
        else{
            document.getElementById("complete").innerHTML = "Pending";
        }
    })
    .catch(error => {
        console.error(error);
    })
}

function finished(){
    const params = new URLSearchParams(window.location.search);
    const taskId = params.get("task_id");

    fetch(`http://localhost:5000/api/tasks/${taskId}/complete`, {
        method: "PUT"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadTask();
    })
    .catch(error => {
        console.error(error)
    });
}
