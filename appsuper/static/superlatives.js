function addSuperlative(id, ownedByMe, name, num) {
    console.log(id);
    newRow = $('<div/>').attr('id', id).addClass('superlative');

    if (ownedByMe) {
	nameElem = $('<input/>').attr('type', 'text').addClass('name').val(name).change(
	    function() {sendSuperlative(id);}
	    );
    } else {
	nameElem = $('<span/>').attr('class', 'name').addClass('name').text(name);
    }    
    nameElem.appendTo(newRow);
    
    if (ownedByMe) {
	numElem = $('<input/>').attr('type', 'number').attr('min', 1).addClass('num')
	    .attr('value', num).change(
	    function() {
		idsel = '#' + id;
		console.log(id);
		answers = $(idsel).find('input.answer');
		console.log($(idsel).find('input.num').val());
		ninps = parseInt($(idsel).find('input.num').val());
		if (answers.length > ninps) {
		    answers[answers.length-1].remove();
		} else if (answers.length < ninps){
		    $(idsel).append($('<input/>').addClass('index-' + answers.length).addClass('answer')).change(
			    createSendSelection(id, answers.length)
		    );
		}
		sendSuperlative(id);
	    }
	);	
	numElem.appendTo(newRow);
    }

    for (var ii = 0; ii < num; ii++) {
	answerElem = $('<input/>').addClass('index-' + ii).addClass('answer');
	console.log(ii);
	answerElem.appendTo(newRow).change(	    
	    createSendSelection(id, ii))
    }   
    if (ownedByMe) {
	deleteElem = $('<span/>').addClass('deletebutton').text('x')
	    .click(function() {
	    $.post('/superlatives/deleteSuperlative/', {id:id},
		   function(d) {
		       if (d == 'deleted') {
			   $('#'+id).remove();
		       } else {
			   alert('Sorry, you can\'t delete a superlative that other people have filled in');
		       }
		   })
	});
	deleteElem.appendTo(newRow);
    }
    
    newRow.appendTo($('#superlatives'));
}

function populateSelections() {
    selections.forEach(
	function(sel) {
	    console.log(sel);
	    $('#' + sel['id']).find('.index-'+sel['index']).val(sel['selection']);
	}
    )
}

function addNewSuperlative() {
    $.post('/superlatives/newSuperlative/',
	   function(d) {
	       d = JSON.parse(d)
	       addSuperlative(d['id'], true, "", 1);
	   });
}
function createSendSelection(id, index) {
    return function() { sendSelection(id, index); };
}

function sendSelection(id, index) {
    idsel = '#' + id;
    console.log(idsel, index);
    var answer = $(idsel).find('.index-' + index).val();
    console.log(answer);
    $.post('/superlatives/updateSelection/',
	   {id:id, index:index, answer:answer});
}
function sendSuperlative(id) {
    idsel = '#' + id;
    var name = $(idsel).find('.name').val();
    var num = parseInt($(idsel).find('.num').val());
    $.post('/superlatives/updateSuperlative/',
	   {id:id, name:name, num:num});
}

function createExistingSuperlatives() {
    $(superlatives).each(function() {
	var sl = $(this)[0];
	addSuperlative(sl.id, sl.ownedByMe, sl.name, sl.numfields);
    })
}

function loadvars() {
    $.getJSON('/superlatives/superlatives/',
	      function(d) {
		  superlatives = d;
		  console.log(superlatives);
		  createExistingSuperlatives();
		  $.getJSON('/superlatives/selections/',
			    function(d) {
				selections = d;
				populateSelections()
			    })
	      })
}

$('document').ready(loadvars);
