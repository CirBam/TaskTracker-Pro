var allTasks =[];

function applyFilterAndSort(){
    let tasks = [...allTasks];
    let filterValue = document.getElementById("filterSelect").value;
    let sortValue = document.getElementById("sortSelect").value;

    if (filterValue != "All"){
        tasks = tasks.filter(task => task.category == filterValue);
    }

    if (sortValue == "Due Date"){
        tasks.sort((a,b) => a.date.localeCompare(b.date));
    }
    else if (sortValue == "Priority"){
        let priorityOrder ={
            "Low":1,
            "Mid":2,
            "High":3,
            "Max":4
        };
        tasks.sort((a,b) => priorityOrder[b.priority] - priorityOrder[a.priority]);
    }
    else if(sortValue == "Title"){
        tasks.sort((a,b) => a.title.localeCompare(b.title));
    }
    listTasks(tasks);
}


function loadTaskList(){

    const currentUserId = localStorage.getItem("user_id");
    fetch(`http://localhost:5000/api/tasks?user_id=${currentUserId}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        allTasks = data.tasks;
        applyFilterAndSort();
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

        if (!confirm("Are you sure you want to delete this task?")){
            return;
        }

        fetch(`http://localhost:5000/api/tasks/${taskID}`, {
            method: "DELETE"
        })
        .then(response => response.json())
        .then(data => {
            alert("Task deleted successfully!");
            loadTaskList();
        })
        .catch(error => {
            console.error(error);
        });
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

var selectedTask = null;
function selectTask(taskID){
    if (selectedTask){
        document.getElementById("task" + selectedTask).className = "";
    }

    document.getElementById("task" + taskID).className = "taskselect";
    selectedTask = taskID;
}

function openSelected(mode){
    if (selectedTask == null){
        alert("Please select a task first.")
        return;
    }
    openView(mode,selectedTask);
}

function edit(){
    const params = new URLSearchParams(window.location.search);
    const taskID = params.get("task_id");
    window.location.href = `edittask.html?task_id=${taskID}`;
}

function deleteTask(){
    const params = new URLSearchParams(window.location.search);
    const taskID = params.get("task_id");

    if (!confirm("Are you sure you want to delete this task?")){
        return;
    }

    fetch(`http://localhost:5000/api/tasks/${taskID}`,{
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        alert("Task deleted successfully!");
        window.location.href = "tasklist.html";
    })
    .catch(error => {
        console.error(error);
    });
}
