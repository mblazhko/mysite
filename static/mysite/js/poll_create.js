function addQuestion() {
      const questionsDiv = document.getElementById("questions");

      const question = document.createElement("div");
      question.classList.add("card-body", "border", "mb-2")

      const questionContainer = document.createElement("div");
      questionContainer.classList.add("d-flex", "align-items-center");

      const questionInput = document.createElement("input");
      questionInput.type = "text";
      questionInput.name = "questions";
      questionInput.required = true;
      questionInput.placeholder = "Question";
      questionInput.className = "form-control";
      questionContainer.appendChild(questionInput);

      const removeQuestionButton = document.createElement("button");
      removeQuestionButton.type = "button";
      removeQuestionButton.textContent = "-";
      removeQuestionButton.classList.add("btn", "btn-outline-danger", "ml-2");
      removeQuestionButton.addEventListener("click", function() {
          questionsDiv.removeChild(question);
      });
      questionContainer.appendChild(removeQuestionButton);

      const addOptionButton = document.createElement("button");
      addOptionButton.type = "button";
      addOptionButton.textContent = "Add an option";
      addOptionButton.classList.add("btn", "btn-outline-dark", "ml-2", "my-1");
      addOptionButton.addEventListener("click", function() {
          const questionText = questionInput.value;
          addOption(question, questionText);
      });

      question.appendChild(questionContainer);
      question.appendChild(addOptionButton);

      questionsDiv.appendChild(question);
}

  function addOption(questionsDiv, questionText) {
      const optionInput = document.createElement("input");
      optionInput.type = "text";
      optionInput.name = `options_${questionText}`;
      optionInput.required = true;
      optionInput.placeholder = "Option";
      optionInput.classList.add("form-control", "form-control-sm", "list-group-item",);

      const optionDiv = document.createElement("div");
      optionDiv.classList.add("card-body", "d-flex", "align-items-center", "p-0", "mx-2")

      const removeOptionButton = document.createElement("button");
      removeOptionButton.type = "button";
      removeOptionButton.textContent = "-";
      removeOptionButton.classList.add("btn", "btn-outline-danger",)
      removeOptionButton.addEventListener("click", function() {
        optionDiv.removeChild(optionInput);
        optionDiv.removeChild(removeOptionButton);
      });

      optionDiv.appendChild(optionInput);
      optionDiv.appendChild(removeOptionButton);

      questionsDiv.appendChild(optionDiv);
      }

document.getElementById("pollForm").addEventListener("submit", function(event) {
    const questions = document.querySelectorAll("[name='questions']");
    let valid = true;

    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(errorMessage => {
        errorMessage.remove();
    });

    if (questions.length === 0) {
        valid = false;
        const errorMsg = document.createElement('div');
        errorMsg.className = 'error-message text-danger text-sm';
        errorMsg.innerText = 'Please add at least one question';
        document.getElementById('questions').appendChild(errorMsg);
    }

    questions.forEach(question => {
        const questionText = question.value;
        const options = document.querySelectorAll(`[name='options_${questionText}']`);

        if (options.length < 2) {
            valid = false;
            const errorMsg = document.createElement('div');
            errorMsg.className = 'error-message text-danger text-sm';
            errorMsg.innerText = 'Please add at least two options for each question';
            document.getElementById('questions').appendChild(errorMsg);
        }
    });

    if (!valid) {
        event.preventDefault();
    }
});