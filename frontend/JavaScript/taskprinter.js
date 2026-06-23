function listTasks(jsonList) {
  let tasktable = "<tbody>";

  // Rebuild the header row so it doesn't get wiped out when we update innerHTML
  tasktable += `
    <tr>
      <th>Title</th>
      <th>Due Date</th>
      <th>Priority</th>
      <th>Category</th>
      <th>Status</th>
      <th>Actions>/th>
    </tr>
  `;

  // Parse the JSON string into a JavaScript array (if it isn't parsed already)
  let tasks = typeof jsonList === "string" ? JSON.parse(jsonList) : jsonList;

  // Iterate over the actual tasks array, not the hardcoded header data
  tasks.forEach(task => {
    tasktable += `<tr id="task${task.task_id} onclick="selectTask(${task.task_id})">`;

    // Inject the properties directly into table data cells
    tasktable += `<td>${task.title}</td>`;
    tasktable += `<td>${task.date}</td>`;
    tasktable += `<td>${task.priority}</td>`;
    tasktable += `<td>${task.category}</td>`;

    // Format the boolean completion status into readable text
    let statusText = task.completed ? "Completed" : "Pending";
    tasktable += `<td>${statusText}</td>`;

    tasktable += "</tr>";
  });

  tasktable += "</tbody>";

  // Update the table in the DOM
  document.getElementById("tasktable").innerHTML = tasktable;
}

var selectedTask = null;

function selectTask(newid) {
  if (selectedTask) {
    document.getElementById(selectedTask).className = "";
  }
  document.getElementById(newid).className = "taskselect";
  selectedTask = newid;
}

function openView(mode) {
  switch (mode) {
    case 0://view
      let targetUrl = "viewtask.html?taskid=" + selectedTask;
      window.location.href(targetUrl);
			break;
		case 1://edit
			let targetUrl = "edittask.html?taskid=" + selectedTask;
			window.location.href(targetUrl);
			break;
		case 2://delete
			var check = confirm("Are you sure you want to delete this task?");
			if (check) {
				//enter delete command here.
			}
			break;
		default:
      alert("Something went wrong. Please try again.");
  }
}
