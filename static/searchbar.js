'use strict';

function searchResultResponse(response) {
   $('#searchresults').html(response);
}
function updateSelectedResponse(response) {
   $('#selectedStudents').html(response)
   updateMetrics()
}
function updateMetricsResponse(response) {
   $('#metricsWrapper').html(response)
   getSearchResults()
}

// read button values to get students that have been selected
//TODO cookies?
function selected() {
   let selectedList = [];
   $('.selected').each(function (_, element) {
      selectedList.push(element.value)
   })
   const selected = selectedList.join()
   console.log(selected)
   return selected
}

function addStudent() {
   let baseurl = '/addstudent'
   let netid = $(this).val();
   netid = encodeURIComponent(netid);
   updateSelected(baseurl, netid);
}
function removeStudent() {
   let baseurl = '/removestudent';
   let netid = $(this).val();
   netid = encodeURIComponent(netid);
   updateSelected(baseurl, netid);
}

let request = null;

function updateSelected(baseurl, netid) {
   console.log(baseurl)
   let sel = selected();
   sel = encodeURIComponent(sel);
   let url = baseurl + `?sel=${sel}&netid=${netid}`
   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'GET',
         url: url,
         success: updateSelectedResponse
      }
   );
}
function updateMetrics() {
   if (request != null)
      request.abort();
   let sel = selected();
   sel = encodeURIComponent(sel);
   request = $.ajax(
      {
         type: 'GET',
         url: `/updatemetrics?sel=${sel}`,
         success: updateMetricsResponse
      }
   );
}
function getSearchResults() {
   let name = $('#nameID').val();
   let netid = $('#netID').val();
   let year = $('#yearID').val();

   // what to search by
   name = encodeURIComponent(name);
   netid = encodeURIComponent(netid);
   year = encodeURIComponent(year);
   // what to filter out
   const sel = encodeURIComponent(selected());

   let url = `/students?name=${name}&netid=${netid}&year=${year}&sel=${sel}`;

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
