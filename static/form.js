// init for cards
var cardsJSON;
var userPrompt;

// hide save button and progress bar
var save = document.querySelector('#save-form');
var progress = document.querySelector('#progress');
save.style.display = 'none';
progress.style.display = 'none';

// Creation button
document.querySelector('#chat-form').onsubmit = function () {
  // Reset old cards
  document.querySelector('#flashcards').innerHTML = '';

  // Get values
  const form = document.querySelector('#chat-form');
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const userInput = document.querySelector('#chat-input');

  // Reset chat to loading
  progress.style.display = 'block';
  form.style.display = 'none';

  // Send input
  fetch('/create/', {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    body: JSON.stringify({
      userInput: userInput.value,
    }),
  })
    // Receive cards in JSON form
    .then((response) => response.json())
    .then((data) => {
      data.flashcards.forEach((element) => {
        createFlashCard(element);
        // Hide progress and redisplay form
        progress.style.display = 'none';
        form.style.display = 'block';
        // Set save flag visible
        save.style.display = 'block';
        // Save data in 'global' element
        cardsJSON = data;
        userPrompt = userInput.value;
      });
    });

  return false;
};

// Save button
save.onsubmit = function () {
  // reset cards
  document.querySelector('#flashcards').innerHTML = '';
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // hide form
  save.style.display = 'none';
  progress.style.display = 'block';

  // send JSON
  fetch('/save/', {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    body: JSON.stringify({
      userPrompt: userPrompt,
      cards: cardsJSON,
    }),
  }) // Receive response in JSON form
    .then((response) => response.json())
    .then((data) => {
      // hide save button
      progress.style.display = 'none';
    });
  return false;
};

function createFlashCard(card) {
  const cards = document.querySelector('#flashcards');
  // init
  var object = document.createElement('details');
  var summary = document.createElement('summary');
  var content = document.createElement('p');

  // add response
  summary.innerHTML = card.front;
  content.innerHTML = card.back;

  // clean up element
  object.append(summary);
  object.append(content);
  cards.append(object);
}
