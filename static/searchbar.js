'use strict';

function searchResultResponse(response) {
   $('#searchresults').html(response);
}
function updateSelectedResponse(response) {
   $('#selectedStudents').html(response)
   updateMetrics()
}
function updateMetricsResponse(response){
   $('#metricsWrapper').html(response)
   getSearchResults()
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

function updateStudent(url) {
   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'POST',
         url: url,
         success: updateSelectedResponse
      }
   );
}
function updateMetrics() {
   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'GET',
         url: '/updatemetrics',
         success: updateMetricsResponse
      }
   );
}
function getSearchResults() {
   let name = $('#nameID').val();
   let netid = $('#netID').val();
   let year = $('#yearID').val();

   name = encodeURIComponent(name);
   netid = encodeURIComponent(netid);
   year = encodeURIComponent(year);

   let url = `/students?name=${name}&netid=${netid}&year=${year}`;

   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'GET',
         url: url,
         success: searchResultResponse
      }
   );
}

function setup() {
   $('#nameID').on('input', getSearchResults);
   $('#netID').on('input', getSearchResults);
   $('#yearID').on('input', getSearchResults);
}
$('document').ready(setup);