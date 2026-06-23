
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