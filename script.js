const form = document.getElementById('spam-form');
const outputBox = document.getElementById('result-box');
const outputLabel = document.getElementById('result-label');
const outputScore = document.getElementById('result-confidence');
const submitBtn = document.getElementById('check-btn');

if (form) {
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = document.getElementById('message').value.trim();
    if (!message) return;

    submitBtn.textContent = "Processing...";
    submitBtn.disabled = true;

    try {
      const response = await fetch('/predict', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await response.json();

      // Support both "result" and "prediction" key from app.py
      const prediction = data.result || data.prediction;
      const confidence = data.confidence || data.spam_probability;

      outputBox.style.display = "block";
      outputBox.className = (prediction === "SPAM" || prediction === "Spam") ? "spam" : "ham";

      outputLabel.textContent = prediction;
      outputScore.textContent = `Confidence: ${confidence}%`;

    } catch (error) {
      alert("Server error. Try again.");
    } finally {
      submitBtn.textContent = "Analyze Message";
      submitBtn.disabled = false;
    }
  });
}