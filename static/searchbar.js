'use strict';

// read button values to get students that have been selected
//TODO cookies?
function selected() {
   let selectedList = [];
   $('.selected').each(function (_, element) {
      selectedList.push(element.value)
   })
   const selected = selectedList.join()
   return encodeURIComponent(selected)
}

function addStudent() {
   let baseurl = '/addstudent'
   let netid = $(this).val();
   netid = encodeURIComponent(netid);
   let sel = selected();
   let url = baseurl + `?sel=${sel}&netid=${netid}`
   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'GET',
         url: url,
         success: (res) => {
            $('#selectedStudents').html(res)
            updateMetrics(true)
         }
      }
   );
}
function removeStudent() {
   let netid = $(this).val();
   $(`.${netid}-comp`).remove(); // delete all elements for that class
   if($(".selected").length == 0){
      $("#selstudheader").remove();
   }
   getSearchResults()
}

let request = null;

function updateMetrics(updateAll) {
   if (request != null)
      request.abort();
   
   let baseurl, updateMetricsSuccess;

   if(updateAll) { // update all metrics
      baseurl = '/updatemetrics';
      updateMetricsSuccess = (res) =>{
            let parsed = JSON.parse(res)
            $('#activeWrapper').html(parsed.activehtml)
            $('#periodDataWrapper').html(parsed.periodbody)
            getSearchResults();
            $(".loader").hide();
      };
   }
   else { // only update the period metric
      baseurl = '/updateperiod';
      updateMetricsSuccess = (res)=>{
         $('#periodDataWrapper').html(res)
         getSearchResults();
         $(".loader").hide();
      };
 }
   let start = $('#startInput').val();
   let end = $('#endInput').val()
   start = encodeURIComponent(start);
   end = encodeURIComponent(end);
   $(".loader").show()
   request = $.ajax(
      {
         type: 'GET',
         url: baseurl+`?pst=${start}&pet=${end}&sel=${selected()}`,
         success: (res) => updateMetricsSuccess(res)
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

   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'GET',
         url: `/students?name=${name}&netid=${netid}&year=${year}&sel=${selected()}`,
         success: (res) => {
            $('#searchresults').html(res);
         }
      }
   );
}

function setup() {
   $('.searchinput').on('input', getSearchResults);
   $('#all126').click(() => {
      if (request != null)
         request.abort();

      request = $.ajax(
         {
            type: 'GET',
            url: '/coursestudents?course=126',
            success: (res) => {
               $('#selectedStudents').html(res)
               updateMetrics(true)
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
               updateMetrics(true)
            }
         }
      );
   })
   $('#allclear').click(() => {
      if (request != null)
         request.abort();

      request = $.ajax(
         {
            type: 'GET',
            url: '/coursestudents?course=none',
            success: (res) => {
               $('#selectedStudents').html(res)
               updateMetrics(true)
            }
         }
      );
   })
}
$('document').ready(setup);
