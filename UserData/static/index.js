const textElement = document.getElementById('typing');
        const text = "Store your important notes, update, and access them anywhere you want.";
        let index = 0;
      
        function typeText() {
          if (index < text.length) {
            textElement.textContent += text.charAt(index);
            index++;
            setTimeout(typeText, 50); // Adjust the typing speed by changing the timeout value (e.g., 50ms)
          }
        }
      
        // Start the typing effect when the page loads
        window.onload = typeText;