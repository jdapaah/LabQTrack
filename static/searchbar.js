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

function addStudentHelper(parsed) {
   $('#periodDataWrapper').append(parsed.periodhtml)
   $('#selectedStudents').append(parsed.selectedhtml)
   $('#TODOremove').html(parsed.script) // TODO please fix this is dumb
   $("#selectedStudents").show()
   if (parsed.present) {
      $('#activePresent').append(parsed.activehtml)
   }
   else {
      $('#activeAbsentList').append(parsed.activehtml)
      $('#activeAbsent').show()
   }
}

let request = null;

function addStudent() {
   let netid = $(this).val();
   console.log(netid)
   let start = $('#startInput').val();
   let end = $('#endInput').val()
   netid = encodeURIComponent(netid);
   start = encodeURIComponent(start);
   end = encodeURIComponent(end);
   let url = `/addstudent?pst=${start}&pet=${end}&netid=${netid}`
   if (request != null)
      request.abort();

   request = $.ajax(
      {
         type: 'GET',
         url: url,
         success: function (res) {
            let parsed = JSON.parse(res)
            addStudentHelper(parsed);
            getSearchResults();
         }
      }
   );
}

function removeStudentHelper(netid){
   $(`.${netid}-comp`).remove(); // delete all elements for that class

   if ($(".selected").length == 0)
      $("#selectedStudents").hide();
   else
      $("#selectedStudents").show();

   if ($(".selectedabsent").length == 0)
      $("#activeAbsent").hide();
   else
      $("#activeAbsent").show();
}
function removeStudent() {
   let netid = $(this).val();
   removeStudentHelper(netid)
   getSearchResults()
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
// dom is ready function
$(function () {
   $('.selected').click(removeStudent)
   $("#selectedStudents").hide()
   $("#activeAbsent").hide()
   $('.searchinput').on('input', getSearchResults);
   $('.searchbar-button').click(function (event) {
      let start = $('#startInput').val();
      let end = $('#endInput').val()
      start = encodeURIComponent(start);
      end = encodeURIComponent(end);
      if (request != null)
         request.abort();

         $(".loader").show()
         request = $.ajax(
         {
            type: 'GET',
            url: `/coursestudents?pst=${start}&pet=${end}&sel=${selected()}&course=${encodeURIComponent(event.target.value)}`,
            success: (res) => {
               let parsed = JSON.parse(res);
               for(let netid of parsed.remove){
                  removeStudentHelper(netid)
               }
               for (let piece of parsed.add) {
                  addStudentHelper(piece)
               }   
               $(".loader").hide()
               getSearchResults()
            }
         }
      );
   });
});
