document.getElementById('download-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    // Get input values
    const videoUrl = document.getElementById('video-url').value;
    const choice = document.getElementById('choice').value;
    
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = "Downloading... Please wait...";
  
    // Create the data object to send
    const data = {
      video_url: videoUrl,
      choice: choice
    };
  
    // Send data to the backend (Vercel function)
    fetch('/api/download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
      } else {
        resultDiv.innerHTML = `<p style="color: green;">${data.message}</p>`;
      }
    })
    .catch(error => {
      resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    });
  });
  