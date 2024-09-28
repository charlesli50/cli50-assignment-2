// document
//   .getElementById("uploadForm")
//   .addEventListener("submit", async function (event) {
//     event.preventDefault();

//     // console.log("Uploading image...");
//     fetch(`/step_through/1`)
//       .then((response) => response.text())
//       .then((data) => {
//         document.getElementById("frame").innerText = 1;
//       })
//       .catch((error) => console.error("Error:", error));
//   });
// document
//   .getElementById("walk")
//   .addEventListener("Click", async function (event) {
//     event.preventDefault();
//   });

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function step(step) {
  $.getJSON("/step_through/" + step, function (data) {
    $("#graph-container").html(data.graph_html); // Update the graph
  }).fail(function () {
    console.error("Error fetching the next graph data.");
  });
  await sleep(1000);
}

$(document).ready(function () {
  let currentStep = 0; // Track the current step

  $("#walk").on("click", async function () {
    for (i = 0; i < 15; i++) {
      //   await sleep(1000);
      currentStep++; // Move to the next step
      await step(currentStep);
    }
    currentStep = 0;
  });

  $("#gen_new").on("click", function () {
    $.getJSON("/gen_new/", function (data) {
      $("#graph-container").html(data.graph_html); // Update the graph
    }).fail(function () {
      console.error("Error fetching the next graph data.");
    });
  });

  $("#run_to").on("click", function () {
    $.getJSON("/run_to/", function (data) {
      $("#graph-container").html(data.graph_html); // Update the graph
    }).fail(function () {
      console.error("Error fetching the next graph data.");
    });
  });

  $("#reset").on("click", function () {
    $.getJSON("/reset/", function (data) {
      $("#graph-container").html(data.graph_html); // Update the graph
    }).fail(function () {
      console.error("Error fetching the next graph data.");
    });
  });

  //   var graphContainer = document.getElementById("graph-container");
});

// Get the select element by its ID
var selectElement = document.getElementById("mySelect");

// Add an event listener for the 'change' event
selectElement.addEventListener("change", function () {
  // Get the selected option value
  var selectedValue = selectElement.value;

  // Log the selected value to the console (you can also trigger other actions here)
  $.getJSON("/methods/" + selectedValue, function (data) {
    $("#graph-container").html(data.graph_html); // Update the graph
  }).fail(function () {
    console.error("Error fetching the next graph data.");
  });
});

window.onload = function () {
  //   var graphDiv = document
  //     .getElementById("graph-container")
  //     .getElementsByTagName("div")[0];

  $("#graph-container").on("plotly_click", function (eventData) {
    var selectedPoints = [];
    if (!eventData || !eventData.points) {
      point_data = eventData.target.data[0];
      console.log(point_data);
      console.log(point_data.selectedpoints);

      // Send selected points to Flask server
      fetch("/init_points", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ points: point_data.selectedpoints }),
      })
        .then((response) => response.json())
        // .then((data) => $("#graph-container").html(data.graph_html))
        .then((data) => console.log("Data sent to Flask:", data))
        .catch((error) => console.error("Error:", error));
    }
  });
};

function handleInputChange() {
  const inputValue = document.getElementById("text-input").value; // Get the input value
  $.getJSON("/clusters/" + inputValue, function (data) {
    console.log("Data sent to Flask:", data); // Update the graph
  }).fail(function () {
    console.error("Error fetching the next graph data.");
  });
}
