function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let person = document.getElementById('person_data');

person.addEventListener('change', give_info);

function give_info() {
    const personId = this.value;
    const infoBlock = document.getElementById('person_info');

    if (!personId) {
        infoBlock.innerHTML = '';
        return;
    }

    fetch(getDataUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: `person_data=${encodeURIComponent(personId)}`
    })
     .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        let htmlContent = '';

        if (data.date_of_birth) {
            htmlContent += `<p>День рождения: ${data.date_of_birth}</p>`;
        }
        if (data.address) {
            htmlContent += `<p>Адрес: ${data.address}</p>`;
        }
        if (data.mail) {
            htmlContent += `<p>Email: ${data.mail}</p>`;
        }
        if (data.quantity_books) {
            htmlContent += `<p>Количество книг: ${data.quantity_books}</p>`;
        } else {htmlContent += "<p>Количество книг:  0 </p>";}
        if (data.debt) {
            htmlContent += `<p>Задолженность: ${data.debt} BYN</p>`;
        }


        if(data.orders){
            data.orders.forEach((order, i) => {
            htmlContent += `<p>Выдача: номер ${order.order_id}</p>`;
            order.books.forEach((book, j) => {
            htmlContent += `<p>Книга: ${book}</p>`;
                });
            });
        }

        infoBlock.innerHTML = htmlContent;
    })
    .catch(() => {
        infoBlock.innerHTML = 'Ошибка загрузки данных.';
    });
}