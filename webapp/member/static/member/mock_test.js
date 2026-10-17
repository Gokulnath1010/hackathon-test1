const questions = [...document.querySelectorAll('.question')];
const progress = document.querySelector('#progress');
const answered = document.querySelector('#answered');
const timer = document.querySelector('#timer');
const quizForm = document.querySelector('#quiz-form');
const timeTaken = document.querySelector('#time-taken');
const timeRemaining = document.querySelector('#time-remaining');
let seconds = 45 * 60;
const startedAt = Date.now();

function updateProgress() {
  const count = questions.filter((question) => question.querySelector('input:checked')).length;
  answered.textContent = count;
  progress.style.width = `${count / questions.length * 100}%`;
}

document.querySelectorAll('input[type="radio"]').forEach((input) => input.addEventListener('change', updateProgress));
document.querySelectorAll('.question-answer-button').forEach((button) => {
  button.addEventListener('click', () => {
    const answer = button.nextElementSibling;
    answer.classList.toggle('is-visible');
    button.innerHTML = answer.classList.contains('is-visible')
      ? 'Hide answer <span>↑</span>'
      : 'View answer <span>↓</span>';
  });
});
if (quizForm) {
  quizForm.addEventListener('submit', () => {
    const elapsed = Math.floor((Date.now() - startedAt) / 1000);
    timeTaken.value = `${String(Math.floor(elapsed / 60)).padStart(2, '0')}:${String(elapsed % 60).padStart(2, '0')}`;
    timeRemaining.value = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
  });
}
if (!document.body.classList.contains('quiz-submitted')) {
  setInterval(() => {
    if (seconds <= 0) return;
    seconds -= 1;
    timer.textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
  }, 1000);
}