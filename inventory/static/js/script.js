// $(function(){
//   $('#list_items_table').createTablePagination({
//     rowPerPage: 2,
//     paginationColor: '#6f7ad7',
//     fontColor: '#555555',
//     paginationStyle: 'borderless', // or 'bordered'
//     transitionDuration: 500,
//     jumpPage:true,
//   });
// });

// $(function(){
//   $('#items_history').createTablePagination({
//     rowPerPage: 4,
//     paginationColor: '#6f7ad7',
//     fontColor: '#555555',
//     paginationStyle: 'borderless', // or 'bordered'
//     transitionDuration: 500,
//     jumpPage:true,
//     startingRow: 1
//   });
// });

// paginator({
//   table: document.getElementById("items_history").getElementsByTagName("table")[0],
//   box: document.getElementById("box"),
// });
// paginator({
//   get_rows: function () {
//       return document.getElementById("list").getElementsByTagName("li");
//   },
//   box: document.getElementById("list_index")
// });


$(document).ready(function () {
  $('#items_history').paging({
    limit:5,
  });
});