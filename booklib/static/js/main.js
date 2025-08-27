$(document).ready(function() {
  $('#myTable').DataTable({
  "pagingType": "full_numbers", // Тип постраничной навигации
  "pageLength": 20, // Количество записей на странице
  });
});