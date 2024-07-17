const message = document.querySelector("#message")
const message2 = document.querySelector("#message2")
const fileButton = document.querySelector("#file")
const img = document.querySelector("#img")
const synth = window.speechSynthesis
  

async function classify() {

  //get file data
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  //Call Python function via Flask API
  try {
    const response = await fetch('http://127.0.0.1:5500/classify', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    //collect results
    const result = await response.json();
    console.log(result.data);

    //display results
    message.innerHTML = `Python icon: ${result.data}`;

  } catch (err) {
    console.error('Error calling Python function:', err);
  }
  
}

//adding strings to the site, representing previous pins
//doesn't really do anything rn

let stringList = []; // Array to store the entered strings

function addString() {
    let inputElement = document.getElementById('stringInput');
    let inputValue = inputElement.value.trim(); // Trim any leading/trailing whitespace
    
    if (inputValue !== '') {
      stringList.push(inputValue); // Add the string to the array
        inputElement.value = ''; // Clear the input field
        displayStrings(); // Update the displayed strings
    }
}

function displayStrings() {
    let listElement = document.getElementById('stringList');
    listElement.innerHTML = ''; // Clear previous content

    stringList.forEach(function(string) {
        let listItem = document.createElement('li');
        listItem.textContent = string;
        listElement.appendChild(listItem);
    });
}
