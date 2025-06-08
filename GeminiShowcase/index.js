document.addEventListener('DOMContentLoaded', function() {
  const fileInput = document.getElementById('fileInput');
  const conversationContainer = document.getElementById('conversationContainer');
  
  fileInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = function(e) {
          try {
              const jsonData = JSON.parse(e.target.result);
              renderConversation(jsonData);
          } catch (error) {
              conversationContainer.innerHTML = '<p class="error">解析JSON文件时出错，请确保文件格式正确。</p>';
              console.error('Error parsing JSON:', error);
          }
      };
      reader.readAsText(file);
  });
  
  function renderConversation(data) {
      if (!data || !data.chunkedPrompt || !data.chunkedPrompt.chunks || !Array.isArray(data.chunkedPrompt.chunks)) {
          conversationContainer.innerHTML = '<p class="error">JSON文件格式不符合要求，缺少chunkedPrompt.chunks数组。</p>';
          return;
      }
      
      conversationContainer.innerHTML = '';
      
      data.chunkedPrompt.chunks.forEach((chunk, index) => {
          if (chunk.text) {
              const messageElement = document.createElement('div');
              messageElement.className = 'message';
              
              const textElement = document.createElement('div');
              textElement.className = 'message-text';
              textElement.textContent = chunk.text;
              
              const copyButton = document.createElement('button');
              copyButton.className = 'copy-btn';
              copyButton.textContent = '复制';
              copyButton.addEventListener('click', function() {
                  copyToClipboard(chunk.text);
                  copyButton.textContent = '已复制!';
                  setTimeout(() => {
                      copyButton.textContent = '复制';
                  }, 2000);
              });
              
              messageElement.appendChild(textElement);
              messageElement.appendChild(copyButton);
              conversationContainer.appendChild(messageElement);
          }
      });
  }
  
  function copyToClipboard(text) {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';  // 防止页面滚动
      document.body.appendChild(textarea);
      textarea.select();
      
      try {
          document.execCommand('copy');
      } catch (err) {
          console.error('复制失败:', err);
      }
      
      document.body.removeChild(textarea);
  }
});