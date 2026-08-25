const form = document.getElementById("analyzeForm");
const loader = document.getElementById("loader");
const resultDiv = document.getElementById("result");
const resultContent = document.getElementById("resultContent");
const submitBtn = document.getElementById("submitBtn");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);

  loader.classList.remove("hidden");
  resultDiv.classList.add("hidden");
  submitBtn.disabled = true;

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (data.error) {
      resultContent.textContent = "Error: " + data.error;
    } else {
      resultContent.textContent = data.result;
    }

    resultDiv.classList.remove("hidden");
  } catch (err) {
    resultContent.textContent = "Something went wrong: " + err.message;
    resultDiv.classList.remove("hidden");
  } finally {
    loader.classList.add("hidden");
    submitBtn.disabled = false;
  }
});
