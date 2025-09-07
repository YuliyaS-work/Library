document.addEventListener('DOMContentLoaded', () => {
  const selects = Array.from(document.querySelectorAll('.book-select'));

  // Сохраним все варианты для каждого селекта (чтобы не терять их)
  const allOptions = selects.map(select => {
    return Array.from(select.options).map(option => ({
      value: option.value,
      text: option.text,
    }));
  });

  function updateSelects() {
    // Собираем выбранные значения в предыдущих селектах
    const selectedValues = [];

    selects.forEach((select, index) => {
      const currentValue = select.value;

      // Формируем список значений, которые нельзя показывать в этом селекте
      // Это все выбранные значения в предыдущих селектах
      const disabledValues = selectedValues.slice();

      // Обновляем опции селекта
      select.innerHTML = ''; // очистить

      // Добавляем опции из сохранённого списка, исключая disabledValues
      allOptions[index].forEach(opt => {
        // option с пустым value всегда показываем (placeholder)
        if (opt.value === '' || !disabledValues.includes(opt.value)) {
          const option = document.createElement('option');
          option.value = opt.value;
          option.text = opt.text;
          select.appendChild(option);
        }
      });

      // Восстанавливаем выбранное значение, если оно осталось в списке
      if (currentValue && !disabledValues.includes(currentValue)) {
        select.value = currentValue;
      } else {
        // Если выбранное значение теперь недоступно — сбрасываем выбор
        select.value = '';
      }

      // Добавляем текущ выбор в список выбранных для следующих селектов
      if (select.value) {
        selectedValues.push(select.value);
      }
    });
  }

  // Навешиваем обработчики на все селекты
  selects.forEach(select => {
    select.addEventListener('change', updateSelects);
  });


});

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
        // Инициализация
        updateSelects();
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
    document.getElementById('discount').value=discount;

}
