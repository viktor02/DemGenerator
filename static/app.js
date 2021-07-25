const selectElement = document.querySelector('#select');

selectElement.addEventListener('change', (event) => {
    var selected = selectElement.options[selectElement.selectedIndex].value;
    // If user choice Quote
    if (selected === "2") {
        // Hide 'add watermark' checkbox
        document.getElementById("selectDiv").style.visibility = "hidden";
        // Change text
        document.getElementById("captureLabel").innerText = 'Text'
        document.getElementById("subtextLabel").innerText = 'Quote Author'
    } else {
        // Revert back
        // Visible checkbox
        document.getElementById("selectDiv").style.visibility = "visible";

        // Change text
        document.getElementById("captureLabel").innerText = 'Caption'
        document.getElementById("subtextLabel").innerText = 'Text under caption'
    }
});