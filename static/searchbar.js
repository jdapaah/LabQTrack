'use strict';

// read button values to get students that have been selected
//TODO cookies?
function selected() {
   let selectedList = [];
   $('.selected').each(function (_, element) {
      selectedList.push(element.value)
   })
   const selected = selectedList.join()
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
let parsed = null;

function updateSelected(baseurl, netid) {
   let sel = selected();
   sel = encodeURIComponent(sel);
   let url = baseurl + `?sel=${sel}&netid=${netid}`
   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'GET',
         url: url,
         success: (res) => {
            $('#selectedStudents').html(res)
            updateMetrics()
         }
      }
   );
}
function updateMetrics() {
   if (request != null)
      request.abort();
   let sel = selected();
   let start = $('#startInput').val();
   let end = $('#endInput').val()
   start = encodeURIComponent(start);
   end = encodeURIComponent(end);
   sel = encodeURIComponent(sel);
   request = $.ajax(
      {
         type: 'GET',
         url: `/updatemetrics?pst=${start}&pet=${end}&sel=${sel}`,
         success: (res) => {
            parsed = JSON.parse(res)
            $('#activeWrapper').html(parsed.activehtml)
            $('#periodDataWrapper').html(parsed.periodbody)
            getSearchResults()
         }
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

   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'GET',
         url: `/students?name=${name}&netid=${netid}&year=${year}&sel=${sel}`,
         success: (res) => {
            $('#searchresults').html(res);
         }
      }
   );
}

function setup() {
   $('#nameID').on('input', getSearchResults);
   $('#netID').on('input', getSearchResults);
   $('#yearID').on('input', getSearchResults);
   $('#all126').click(() => {
      if (request != null)
         request.abort();

      request = $.ajax(
         {
            type: 'GET',
            url: '/coursestudents?course=126',
            success: (res) => {
               $('#selectedStudents').html(res)
               updateMetrics()
            }
         }
      );
   })
   $('#all2xx').click(() => {
      if (request != null)
         request.abort();

      request = $.ajax(
         {
            type: 'GET',
            url: '/coursestudents?course=2xx',
            success: (res) => {
               $('#selectedStudents').html(res)
               updateMetrics()
            }
         }
      );
   })
}
$('document').ready(setup);
