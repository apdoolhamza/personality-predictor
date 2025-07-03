 document.addEventListener('DOMContentLoaded', function() {
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-button');
            const chatContainer = document.querySelector('.chat-container');
            const msgcontainer = document.querySelector('.msg-container');
            const typingIndicator = document.getElementById('typing-indicator');
            const quickReplyButtons = document.querySelectorAll('.quick-question');

            // Hide typing indicator initially
            typingIndicator.classList.add('d-none');

            // Function to add a user message to the chat
            function addUserMessage(message) {
                let now = new Date();
                let timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                let messageElement = document.createElement('div');
                messageElement.className = 'd-flex justify-content-end mb-4';
                messageElement.innerHTML = `
                   <div class="d-flex justify-content-end mb-4">
                <div class="flex-grow-1" style="max-width: 80%;">
                    <div class="message-bubble-user p-3 rounded-3 message-enter">
                        <p class="mb-0">${message}</p>
                    </div>
                    <span class="small text-muted mt-1 d-block text-end timestamp">Today, ${timeString}</span>
                </div>
                <div class="message-avatar user-avatar ms-3">
                    <i class="ri-user-line"></i>
                </div>
            </div>
                `;
    
                msgcontainer.insertBefore(messageElement, typingIndicator)
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

               // Function to add a user message to the chat
            function addAIResponse(message) {
 
                // Show typing indicator
                typingIndicator.classList.remove('d-none');
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                // After a delay, hide typing indicator and show AI response
                setTimeout(() => {
                typingIndicator.classList.add('d-none');
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                    let now = new Date();
                    let timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                    let messageElement = document.createElement('div');
                    messageElement.className = 'd-flex justify-content-start mb-4';
                    messageElement.innerHTML = `
                    <div class="d-flex mb-4">
                    <div class="message-avatar ai-avatar me-3">
                        <i class="ri-robot-line"></i>
                    </div>
                    <div class="flex-grow-1" style="max-width: 80%;">
                        <div class="message-bubble-ai p-3 rounded-3 message-enter">
                            <p class="mb-0">${message}</p>
                        </div>
                        <span class="small text-muted mt-1 d-block">${timeString}</span>
                    </div>
                </div>`;
                       
                    msgcontainer.insertBefore(messageElement, typingIndicator)
                    chatContainer.scrollTop = chatContainer.scrollHeight;

                    // Animate progress bars
                    const progressBars = document.querySelectorAll('.progress-bar');
                    progressBars.forEach(bar => {
                        const width = bar.style.width;
                        bar.style.width = '0';
                        setTimeout(() => {
                            bar.style.width = width;
                        }, 100);
                    });
                }, 2000);

            }

            // Raw AI Response
            function response(type, nickname, quote, description, traitsList) {
                return `
                    <div class="message-bubble-ai p-3 rounded-3 message-enter">
                        <p class="mb-3">${type}</p>
                        <p class="mb-3">${nickname}</p>
                        <div class="mb-4">
                        <p id="personality-description" class="text-dark mb-4">${description}</p>
                        <div class="quote text-muted fst-italic">
                            <blockquote id="personality-quote">"${quote}"</blockquote>
                        </div>
                    </div>
                        ${traitsList}
                        <p class="mb-0">To refine my analysis, could you tell me how you typically handle stressful situations? Do you prefer to tackle problems head-on or take time to process before responding?</p>
                    </div>
                `;
            }

            // Fetch Response
            function fetchResponse() {
                 let message = messageInput.value.trim();

                fetch('/predict', {
                    method: 'POST',
                    headers: {
                    'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message_input: message })
                })
                .then(response => response.json())
                .then(data => {

                if (message.length < 50) {
                    addAIResponse("Thanks for sharing! Could you tell me a bit more? The more details you provide, the better I can understand your personality.");
                } else {
                    let traitsList = '';
      
                        for (const [trait, value] of Object.entries(data.traits)) {
                            traitsList += `
                            <div class="mb-4">
                                <div class="d-flex justify-content-between small text-muted mb-1">
                                    <span>${trait}</span>
                                    <span>${value}%</span>
                                </div>
                                <div class="progress" style="height: 6px;">
                                    <div class="progress-bar bg-primary" role="progressbar" style="width: ${value}%"></div>
                                </div>
                            </div>
                            `;
                        }
                        
                    addAIResponse(response(data.type, data.nickname, data.quote, data.description, traitsList));
                }
                    
                });

                addUserMessage(message);
                messageInput.value = '';
            }

            // Send message when button is clicked
            sendButton.addEventListener('click', function() {
                fetchResponse();
            });

            // Send message when Enter key is pressed
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                     fetchResponse();
                }
            });

            // Handle quick reply buttons
            quickReplyButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const message = button.textContent;
                    if (message == "What's MBTI?") {
                    addAIResponse(`
                    <p>MBTI means Myers-Briggs Type Indicator.</p>
                    <p>It’s a system that helps people understand their personality type based on how they think, feel, and behave.</p>
                    <p>It uses four main pairs of traits:</p>
                    I or E - Do you get energy from being alone (Introvert) or around people (Extrovert)?<br>
                    N or S - Do you focus on big ideas (Intuition) or real facts (Sensing)?<br>
                    T or F - Do you decide with logic (Thinking) or feelings (Feeling)?
                    <p>J or P - Do you like plans (Judging) or being flexible (Perceiving)?</p>
                    These combine to form one of 16 personality types like INTJ, ENFP, etc.
                    `);
                    } else if (message == "Your Accuracy Level?") {
                    addAIResponse(`
                    <p>The predictions are based on a machine learning model trained on real personality data</p>
                    <p>Each of the four personality traits is predicted with about 80% accuracy using your writing style</p>
                    <p>But remember:</p>
                    <p>This is not a medical or official personality test. <br>
                    It’s just a smart AI guess based on how you write, Meant to be fun, helpful, and interesting.</p>
                    `);
                    } else if (message == "Dataset Trained On?") {
                    addAIResponse(`
                    <p>This AI was trained on a public dataset made from over 8,000+ people’s writings, where each person’s MBTI type is known.</p>
                    <p>The writings were collected from <a href="https://www.kaggle.com/datasets/datasnaek/mbti-type">Kaggle</a> a popular dataset repository, so the model learned how people with different personality types express themselves through text.</p>
                    `);
                    } else if (message == "Tech Stack Used?") {
                    addAIResponse(`
                    <p>This project was built using:</p>
                    <ul>
                        <li>Python: For the backend and AI</li>
                        <li>scikit-learn: To train and run the models</li>
                        <li>Flask: To make it work as a web app</li>
                        <li>HTML, CSS, Bootstrap, JavaScript: For the user interface</li>
                        <li>joblib: To save and load the models</li>
                    </ul>
                    Everything works together to create a smart, interactive experience.
                    `);
                    }
                    addUserMessage(message);
                });
            });

            // Auto-resize input field based on content
            messageInput.addEventListener('input', function() {
                this.style.height = 'auto';
                const maxHeight = 150; // Maximum height in pixels
                const scrollHeight = this.scrollHeight;
                
                if (scrollHeight <= maxHeight) {
                    this.style.height = scrollHeight + 'px';
                } else {
                    this.style.height = maxHeight + 'px';
                    this.style.overflowY = 'auto';
                }
            });
        });