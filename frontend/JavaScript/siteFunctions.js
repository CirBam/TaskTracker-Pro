// 3. Logout function for the navbar
function logout() {
  localStorage.clear(); // Wipe the saved user data
  window.location.href = "login.html"; // Send back to login
}

function loadDashboard(){
  const username = localStorage.getItem("username");
  document.getElementById("greeting").innerHTML = "Welcome, " + username;
  const currentUserID = localStorage.getItem("user_id");

  fetch(`http://localhost:5000/api/tasks?user_id=${currentUserID}`)
  .then(response => response.json())
  .then(data => {
    let tasks = data.tasks;

    loadSummary(tasks);

    loadUpcoming(tasks);
  })
  .catch(error => {
    console.error(error);
  });
}

function loadSummary(tasks){
  let activeCount = 0;
  let completedCount = 0;
  let urgentCount = 0;

  tasks.forEach(task => {
    if (task.completed){
      completedCount++;
    }
    else{
      activeCount++;
    }

    if(task.priority == "Max"){
      urgentCount++;
    }
  });
  document.getElementById("active").innerHTML = "Active Tasks: " + activeCount;

  document.getElementById("complete").innerHTML = "Completed Tasks: " + completedCount;

  document.getElementById("urgent").innerHTML = "Urgent Tasks: " + urgentCount;
}

function loadUpcoming(tasks){
  let tasklist = document.getElementById("tasklist");
  let datelist = document.getElementById("datelist");

  tasklist.innerHTML = "";
  datelist.innerHTML = "";

  tasks.sort((a,b) => a.date.localeCompare(b.date));
  let count = 0;
  tasks.forEach(task => {
    if (!task.completed && count < 5){
      tasklist.innerHTML +=
        `<li>${task.title}</li>`;
      
      datelist.innerHTML +=
        `<li>${task.date}</li>`;
      count++
    }
  })
}
