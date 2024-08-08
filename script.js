const fileInput = document.getElementById('fileInput');
const uploadedImage = document.getElementById('uploadedImage');
const messageDiv = document.getElementById('message');

fileInput.addEventListener('change', classifyWithOpenAI);

async function classifyWithOpenAI() {
  
  messageDiv.textContent = 'Classifying with OpenAI...';

  function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
  }

  const objectId = getQueryParam('objectId');
  const workspace = getQueryParam('workspace');
  const workspaceId = getQueryParam('workspaceId');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);
  formData.append('objectId', objectId);
  formData.append('workspace', workspace);
  formData.append('workspaceId', workspaceId);
  
  //Call Python function via Flask API
  try {
    const response = await fetch('https://pinhelper.tryformation.com/classifyWithOpenAI', {
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
    message.innerHTML = result.data;
  } catch (err) {
    console.error('Error calling Python function:', err);
  }
}

//show image when uploaded
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


