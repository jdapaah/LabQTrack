'use strict';

function updatePeriodResponse(response){
   $('#periodBody').html
}
function addStudent() {
   // TODO
   let netid = $(this).val()
   let url = `/addstudent?netid=${netid}`
   updateStudent(url);
}
function removeStudent() {
   // TODO
   let netid = $(this).val()
   let url = `/removestudent?netid=${netid}`
   updateStudent(url);
}


let request = null;

function updatePeriod() {
   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'POST',
         url: `updateperiod?start=${}&end=${}`,
         success: updatePeriodResponse
      }
   );
}

function setup() {
   $('#startInput').on('input', getSearchResults);
   $('#endInput').on('input', getSearchResults);
}
$('document').ready(setup);