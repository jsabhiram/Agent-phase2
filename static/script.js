
document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const manipulateTextarea = document.getElementById('manipulate-textarea');
    const chatMainContent = document.querySelector('.chat-main-content'); // The scrollable container
    // console.log(chatMessages.innerHTML())
    // Function to add a message to the chat
    function addMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'ai-message');
        messageDiv.innerHTML = `<p>${message}</p>`; // Wrap in <p> for consistent styling
        chatMessages.appendChild(messageDiv);
        // chatMessages.scrollTop = chatMessages.scrollHeight;
        scrollToBottom(); // Scroll to bottom after adding new message
    }

    // Function to scroll chat messages to the bottom
    function scrollToBottom() {
        chatMainContent.scrollTop = chatMainContent.scrollHeight;
    }

    // Auto-grow textarea logic for user-input
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto'; // Reset height
        userInput.style.height = userInput.scrollHeight + 'px'; // Set to scroll height
        // Ensure max-height is respected by CSS
    });

    // Handle send button click
    sendButton.addEventListener('click', async () => {
        const message = userInput.value.trim();
        if (message === '') return;
    
        
        addMessage('user', message);
        userInput.value = ''; // Clear input
        userInput.style.height = 'auto'; // Reset textarea height after sending

        // Add a temporary AI thinking message
        const thinkingMessage = document.createElement('div');
        thinkingMessage.classList.add('ai-message');
        thinkingMessage.id = 'thinking-message';
        thinkingMessage.innerHTML = '<p>AI is thinking...</p>';
        chatMessages.appendChild(thinkingMessage);
        scrollToBottom(); // Scroll to show thinking message

        try {
            const response = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.response || 'Something went wrong on the server.');
            }

            const data = await response.json();

            // Remove thinking message
            if (thinkingMessage.parentNode) {
                thinkingMessage.parentNode.removeChild(thinkingMessage);
            }

            addMessage('ai', data.response); // Add AI response
            // Show sidebar if not already visible

            // Open sidebar logic handled later  -->>
            // const sidebar = document.querySelector('.sidebar');
            // if (!sidebar.classList.contains('show')) {
            //     sidebar.classList.add('show');
            // }

            // Append content to the sidebar (you can customize this)
            const history = document.getElementById('conversation-history');
            const newItem = document.createElement('p');
            newItem.textContent = `Insight: ${data.response || 'No summary returned.'}`;
            history.appendChild(newItem);

            // Optionally, update the manipulate textarea if your AI also outputs logs/steps
            if (data.manipulation_log) { // Assuming your API returns this
                 manipulateTextarea.value = data.manipulation_log;
                 manipulateTextarea.scrollTop = manipulateTextarea.scrollHeight; // Scroll manipulate textarea
            }

        } catch (error) {
            console.error('Error:', error);
            // Remove thinking message and show error
            if (thinkingMessage.parentNode) {
                thinkingMessage.parentNode.removeChild(thinkingMessage);
            }
            // addMessage('ai', `Error: ${error.message || 'Could not get response from AI.'}`);
        }
    });

    // Allow sending message on Enter key press
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) { // Shift+Enter for new line
            event.preventDefault(); // Prevent default Enter (new line) behavior
            sendButton.click(); // Programmatically click the send button
        }
    });

    // Handle invoice upload (basic click event, file handling not implemented here)
    const invoiceUploadLabel = document.querySelector('.image-upload label');
    const invoiceUploadInput = document.getElementById('invoice-upload');
    const invoiceUploadImg = document.querySelector('.image-upload img');

    if (invoiceUploadLabel && invoiceUploadInput && invoiceUploadImg) {
        invoiceUploadImg.addEventListener('click', () => {
            invoiceUploadInput.click(); // Trigger the hidden file input
        });
        // invoiceUploadLabel.addEventListener('click', () => {
            // invoiceUploadInput.click(); // Also trigger on label click
        // });

        invoiceUploadInput.addEventListener('change', (event) => {
            if (event.target.files.length > 0) {
                const fileName = event.target.files[0].name;
                console.log('Selected file:', fileName);
                // In a real app, you'd send this file to your Flask backend
                // addMessage('user', `Uploaded file: ${fileName}`); // Optional: show upload message
            }
        });
    }

    // Initial scroll to bottom in case there's pre-loaded content
    scrollToBottom();
});
//end of dom loading

setInterval(() => {
  console.log("Checking status...Hitting /status");
  fetch('/status')
    .then(res => res.json())
    .then(data => {
      const sidebar = document.getElementsByClassName('sidebar')[0];
      if (sidebar) {
        sidebar.style.display = data.show_sidebar ? 'block' : 'none';
      }
    })
    .catch(err => console.error("Status check failed:", err));
}, 2000); // check every 2 seconds


let data = "";

function handleFeedback() {

    fetch('/feedback')
        .then(res => res.json())
        .then(dat => {
            const elm = document.getElementById('badge');

            if (dat.zone && dat.zone !== "") {
                elm.innerHTML = dat.zone;
                data = dat.zone;
                // elm.style.display = 'block';
            } else {
                elm.style.display = 'none';
                data = "";
            }
        })
        .catch(err => console.error("Feed check failed:", err));
}


setInterval(() => {
    // const elm = document.getElementById('badge');

    // temporarily show interval text
    // elm.innerHTML = "JS Interval";

        // now trigger feedback update (async fetch will update DOM)
    handleFeedback();
}, 3000);



function lim() {
  const sidebar = document.getElementsByClassName('sidebar')[0];
  if (!sidebar) return;

  const element = document.createElement('p');
  element.innerHTML = '<input type="text" placeholder="Enter the deviation in percentage" />';
  sidebar.appendChild(element);
}

    async function uploadFile() {
    uploaded();
    const input = document.getElementById('invoice-upload');
    const file = input.files[0];
    if(file == null){
        return 1;
    }
    // window.alert("Called uploadFile with file:"+ file);
    // target=document.getElementById('badge');                                              //marked for review
    // target.style.display = 'none';

    // side=document.getElementsByClassName('sidebar');
    // side.classList.add('active');

    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/upload', {
      method: 'POST',
      body: formData
    });
    
    // tar=document.getElementById('badge');
    // tar.textContent="Processing...";
    const result = await response.json();
    displayReport(result);
    // setTimeout(() => {
    //      tar.textContent="Upload your file";
    // },25000)
  }

  function updateFileName() {
    const fileInput = document.getElementById('invoice-upload');
    const fileLabel = document.getElementById('file-label');
    
    if (fileInput.files.length > 0) {
        fileLabel.textContent = fileInput.files[0].name;
    } else {
        fileLabel.textContent = 'Upload Invoice';
    }
}

function uploaded(){
    const fileLabel = document.getElementById('file-label');
    fileLabel.textContent = '';
}
var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value+"%"; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value+"%";
}

 function displayReport(sata) {
            const reportContainer = document.createElement('div');
           
            const chatMessages = document.getElementById('chat-messages');
            
            // Convert markdown to HTML (simple version - for production consider a markdown library)
            let reportHtml = sata.report
                .replace(/## (.*)/g, '<h2 style="color: white;">$1</h2>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*   /g, '<li style="color: white;">')
                .replace(/\n/g, '<br>');
            
        reportContainer.classList.add('ai-message');
        reportContainer.innerHTML = reportHtml; // Wrap in <p> for consistent styling
        chatMessages.appendChild(reportContainer);

        chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
  
function send() {
    console.log("Send button clicked");
    const sliderValue = document.getElementsByClassName('slider')[0].value;
    console.log("Slider value:", sliderValue);
    
    // Show loading state
    const confirmButton = document.querySelector('.confirm');
    const originalText = confirmButton.value;
    confirmButton.value = 'Saving...';
    confirmButton.disabled = true;
    
    // Send slider value to Flask backend
    fetch('/user_input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'slider_value': parseFloat(sliderValue)
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        if (data.status === 'success') {
            console.log('Slider value sent successfully:', data.slider_value);
            
            // Show success feedback
            confirmButton.value = 'Saved!';
            confirmButton.style.backgroundColor = '#28a745';
            
            // Reset button after 2 seconds
            setTimeout(() => {
                confirmButton.value = originalText;
                confirmButton.disabled = false;
                confirmButton.style.backgroundColor = '';
            }, 2000);
            
            // Optional: Show success message in chat
            showMessage('Price hike tolerance set to ' + sliderValue + '%', 'success');
            
        } else {
            console.error('Error from server:', data.error);
            showMessage('Failed to save setting: ' + data.error, 'error');
            resetButton();
        }
    })
    .catch(error => {
        console.error('Network error:', error);
        showMessage('Network error occurred', 'error');
        resetButton();
    });
    
    function resetButton() {
        confirmButton.value = originalText;
        confirmButton.disabled = false;
        confirmButton.style.backgroundColor = '';
    }
}

function closeWarning() {
      document.getElementById('warning').style.display = 'none';
    }   

///comme

// document.addEventListener('DOMContentLoaded', function() {
    // const chatMessages = document.getElementById('chat-messages');
    // const userInput = document.getElementById('user-input');
    // const sendButton = document.getElementById('send-button');
    // 
    // function addMessage(sender, message) {
        // const messageDiv = document.createElement('div');
        // messageDiv.className = `message ${sender}`;
        // messageDiv.textContent = message;
        // chatMessages.appendChild(messageDiv);
        // chatMessages.scrollTop = chatMessages.scrollHeight;
    // }
    // 
    // async function sendMessage() {
        // const message = userInput.value.trim();
        // if (!message) return;
        // 
        // addMessage('user', message);
        // userInput.value = '';
        // 
        // try {
            // const response = await fetch('/api/query', {
                // method: 'POST',
                // headers: {
                    // 'Content-Type': 'application/json',
                // },
                // body: JSON.stringify({ message: message })
            // });
            // 
            // const data = await response.json();
            // if (data.status === 'success') {
                // addMessage('agent', data.response);
            // } else {
                // addMessage('system', 'Error processing your request');
            // }
        // } catch (error) {
            // console.error('Error:', error);
            // addMessage('system', 'Failed to connect to the AI agent');
        // }
    // }
    // 
    // sendButton.addEventListener('click', sendMessage);
    // userInput.addEventListener('keypress', function(e) {
        // if (e.key === 'Enter') {
            // sendMessage();
        // }
    // });
// });
// 
// 
// 