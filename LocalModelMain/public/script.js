const fileInput = document.getElementById('fileInput');
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const uploadedImage = document.getElementById('uploadedImage');
const statusMessage = document.getElementById('status');
const messageDiv = document.getElementById('message');


fileInput.addEventListener('change', uploadImage);

function uploadImage() {
  messageDiv.textContent = 'Image Uploading! Classifying...';
  const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        classify(formData);
    }
    else {
        messageDiv.textContent = "no file";
    }
}

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
        classify(formData);
        uploadedImage.src = URL.createObjectURL(blob);
        uploadedImage.style.display = 'block';
        messageDiv.textContent = 'Photo captured! Classifying...';
    });
}


async function classify(formData) {

  //Call Python function via Flask API
  try {
    const response = await fetch('https://10.1.7.160:5500/classify', {
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