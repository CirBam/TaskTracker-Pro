const propertylist = ["title", "date", "priority", "category", "completed"];

function listTasks(jsonList) {
  var tasktable = "<tbody>";
  var taskdata = {
    header: {
      title: "Title",
      date: "Due Date",
      priority: "Priority",
      category: "Category",
      completed: "Status"
    }
  }
  var newdata = JSON.parse(jsonList);
  for (let tasklist in taskdata) {
    tasktable += "<tr>";
      for (let i = 0; i < 5; i++) {
        tasktable += "<td>";
        if (i == 4 && tasklist != "header") {}
        else {
          tasktable += taskdata[tasklist][propertylist[i]];
        }
        tasktable += "</td>";
      }
    tasktable += "</tr>";
  }
  tasktable += "</tbody>"; //closes the table body
  document.getElementById("tasktable").innerHTML = tasktable;//updates the table
}
