
function test(data) {
    datas = data['recommends'];
    let div = document.getElementById('recommended');
    div.innerHTML = '';

    datas.forEach(function (item) {

        let card = document.createElement('div');
        card.className = 'card';
        card.style.marginBottom = '5px';

        let cardBody = document.createElement('div');
        cardBody.className = 'card-body';
        cardBody.innerText = item['text'];
        cardBody.onclick = function () {
            document.getElementsByClassName('ql-editor')[0].innerHTML += item['text'];
        };
        card.appendChild(cardBody);

        div.appendChild(card);
    });
}

function isKeyPressed(event) {
    if (event.keyCode == 9) {
        let text = document.getElementsByClassName('ql-editor')[0];
        fetch('/recommendation', {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                content: text.innerHTML
            })
        }).then(response => response.json())
            .then(data => test(data));
    }
}