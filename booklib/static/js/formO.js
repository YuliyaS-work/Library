// Функция для обновления всех списков книг, исключая выбранные
function updateBookOptions() {
    const allSelects = document.querySelectorAll('.book-select');
    const selectedValues = Array.from(allSelects)
        .map(s => s.value)
        .filter(v => v !== '');

    allSelects.forEach(function(select) {
        const currentValue = select.value;
        // Временный массив опций
        const options = Array.from(select.options);
        // Проверяем, есть ли уже опция "--Выберите книгу--"
        const placeholderOption = select.querySelector('option[value=""]');

        // Если нет, добавляем её
        if (!placeholderOption) {
            select.innerHTML = '<option value="">--Выберите книгу--</option>';
        } else {
            // Очищаем все, кроме этой опции
            select.innerHTML = '';
            select.appendChild(placeholderOption);
        }
        options.forEach(function(option) {
            if (option.value === '' || option.value === currentValue) {
                // добавляем текущий выбранный или пустой
                select.appendChild(option);
            } else if (!selectedValues.includes(option.value)) {
                // добавляем только если не выбран в другом списке
                select.appendChild(option);
            }
        });
    });
}

const prices = {};

// Обновляем обработчики для всех селектов
document.querySelectorAll('.book-select').forEach(function(select) {
    select.addEventListener('change', function() {
        const selectedBookId = this.value;
        const index = this.id.split('_')[1];
        const subSelect = document.getElementById(`bookobj_${index}`);

        if (selectedBookId) {
            fetch(`${getBookObjUrl}?book_id=${selectedBookId}`)
                .then(response => response.json())
                .then(data => {
                    subSelect.innerHTML = '';
                    if (data.length > 0) {
                        data.forEach(function(sub) {
                            const option = document.createElement('option');
                            option.value = sub.registr_number;
                            option.textContent = sub.registr_number;
                            option.setAttribute('data-price', sub.price_per_day);
                            subSelect.appendChild(option);
                        });
                        subSelect.disabled = false;

                        // по умолчанию выбираем первый
                        const firstOption = subSelect.options[0];
                        if (firstOption) {
                            subSelect.value = firstOption.value;
                            const pricePerDay = parseFloat(firstOption.getAttribute('data-price'));
                            prices[index] = pricePerDay;
                            updateCost();
                        }
                    } else {
                        const option = document.createElement('option');
                        option.textContent = '--Нет подклассов--';
                        option.value = '';
                        subSelect.appendChild(option);
                        subSelect.disabled = true;
                        delete prices[index];
                        updateCost();
                    }
                });
        } else {
            // если ничего не выбрано
            subSelect.innerHTML = '<option value="">--номер--</option>';
            subSelect.disabled = false;
            delete prices[index];
            updateCost();
        }

        // Обновляем список книг, чтобы исключить выбранные
        updateBookOptions();
    });
});


function updateCost() {
    let sumPricesPerDay = 0;
    let quantityBooks = Object.keys(prices).length;

    for (const key in prices) {
        sumPricesPerDay += prices[key];
    }
    let discount = 1;
    if (quantityBooks <= 2) {
        discount = 1;
    } else if (quantityBooks >=3 && quantityBooks <=4) {
        discount = 0.9;
    } else if (quantityBooks >=5) {
        discount=0.85;
    }

    const days=30;
    const totalCost=Math.round(sumPricesPerDay * days * discount *100)/100;
    document.getElementById('pre_cost').value=totalCost.toFixed(2);
    document.getElementById('quantity_books').value=quantityBooks;
}
