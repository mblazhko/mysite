document.getElementById('pollForm').addEventListener('submit', function(event) {
    const questions = document.querySelectorAll('[name^="choice_"]');
      let valid = true;

      questions.forEach(function(question) {
        const name = question.getAttribute('name');
        const checked = document.querySelector('[name="' + name + '"]:checked');

        const questionId = name.split('_')[1];

        const questionElement = document.getElementById('question_' + questionId);

        if (!checked) {
            valid = false;
            if (!questionElement.querySelector('.error-message')) {
                const errorMsg = document.createElement('h6');
                errorMsg.className = 'error-message text-danger text-sm';
                errorMsg.innerText = 'Please make your choice';
                questionElement.appendChild(errorMsg);
            }
        } else {
            if (questionElement.querySelector('.error-message')) {
                questionElement.querySelector('.error-message').remove();
            }
        }
    });

    if (!valid) {
        event.preventDefault();
    }
});