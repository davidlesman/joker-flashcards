function interceptClickEvent(e) {
  var target = e.target || e.srcElement;
  // check if linked was clicked
  if (target.getAttribute('id') === 'group') {
    // reset cards
    const cards = document.querySelector('#list');
    cards.innerHTML = '';

    // get info
    const group = target.getAttribute('value');
    const csrftoken = document.querySelector(
      '[name=csrfmiddlewaretoken]'
    ).value;

    fetch('/cards/', {
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken },
      body: JSON.stringify({
        group: group,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // loop and create cards
        Object.keys(data).forEach((key) => {
          console.log(key);
          createFlashCard(data[key]);
        });
      });

    //tell the browser not to respond to the link click
    e.preventDefault();
  }
}

function createFlashCard(card) {
  const cards = document.querySelector('#list');
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

//listen for link click events at the document level
if (document.addEventListener) {
  document.addEventListener('click', interceptClickEvent);
} else if (document.attachEvent) {
  document.attachEvent('onclick', interceptClickEvent);
}
