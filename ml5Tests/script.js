const fileInput = document.getElementById('fileInput');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const uploadedImage = document.getElementById('uploadedImage');
const statusMessage = document.getElementById('status');
const messageDiv = document.getElementById('message');

function uploadImage() {
  messageDiv.textContent = 'Image Uploading! Classifying...';
  const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        classify(formData);
    }
}
2
function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.style.display = 'block';
            captureButton.style.display = 'block';
        })
        .catch(error => {
            console.error('Error accessing camera: ', error);
            messageDiv.textContent = 'Error accessing camera';
        });
    uploadedImage.src = '';
    uploadedImage.style.display = 'none';  
    messageDiv.textContent = "take a photo!"  
}

function capturePhoto() {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    video.style.display = 'none';
    captureButton.style.display = 'none';
    video.srcObject.getTracks().forEach(track => track.stop());
    
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('file', blob, 'photo.png');
        classify2(formData);
        uploadedImage.src = URL.createObjectURL(blob);
        uploadedImage.style.display = 'block';
        messageDiv.textContent = 'Photo captured! Classifying...';
    });
}

fileInput.addEventListener('change', uploadImage);

async function classify2(formData) {

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
    message.innerHTML = `${result.data}`;

  } catch (err) {
    console.error('Error calling Python function:', err);
  }
  
}


//ffffffffffffffffffffffffffffff

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
    message.innerHTML = `${result.data}`;

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

document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('fileInput');
  const uploadedImage = document.getElementById('uploadedImage');
  
  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
      const objectURL = URL.createObjectURL(file);
      uploadedImage.src = objectURL;
      uploadedImage.style.display = 'block';
    } else {
      uploadedImage.src = '';
      uploadedImage.style.display = 'none';
    }
  });
});