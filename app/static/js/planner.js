var MAX_COURSES = 4

function addCourse(term, course, short_name) {

    var obj = ($(".termsBlock").find(term));

    obj.append('<div class="row-fluid"> <div class="span12"> <li id="' + course + '" class="ui-state-default draggable"> <div class="row-fluid"> <div class="span12">' + short_name + '<i class="btn btn-danger"><span class="icon-trash icon-white"></i> </div> </div> </li> </div> </div>');


    $('i.btn-danger').click(removeCourse);
}

function showAvailableSlots(event, ui) {
    var posting = $.post('/findterms', { course_item: ui.item.attr('id') });

    posting.done(function (data) {
        $.each(data['terms'], function(index, item) {
            term_id = "#" + item['term'];
            if ($(term_id).hasClass('off-term')) {
                $(term_id).addClass('available-off');
            } else {
                $(term_id).addClass('available');
            }
        });
    });
}

function clearAvailableSlots(event, ui) {
    $('.sortable2').each( function(index, item) {
        $(this).removeClass('available');
        $(this).removeClass('available-off');
    });
}

function saveCourse(event, ui) {
    
    var selectVal = $('#dept_name').find(":selected").val();

    var text = ui.item.attr('id');

    var term_id = ($( this ).attr("id"));
    var ext_term_id = "#" + term_id;

    if ($(ext_term_id + " li").length > MAX_COURSES + 1) {
        alert("Maximum courses exceeded for this term.");
        return;
    }

    var posting = $.post('/savecourse', { course_item: text, term: term_id });

    posting.done(function (data) {
        var senderclass = ui.sender.attr('class');

        if (data['error']) {
        	return;
        }

        if (senderclass.indexOf('sortable2') >= 0) {
        	var postremove = $.post('/removecourse', { course: text, term: ui.sender.attr('id')})

    		$("#" + ui.sender.attr('id') + " li").each(function(index, li) {
    			var course = $(li);
    			if (course.attr('id') == text) {
    				course.parent().remove();
    			};
    		});
        }
        
        addCourse(ext_term_id, text, data['name']);

    });
        
}

function removeCourse(event){
    var term_id = $( this ).parents('ul').attr('id');

    var posting = $.post('/removecourse', { course: $(this).parents("li").attr("id"), term: term_id });

    $(this).parents('li').parent().remove();

}

function swap_term(term){

    var term_id = "#" + term;

    // Mark term as off
    if ($(term_id).hasClass('off-term')) {
        $(term_id).removeClass('off-term');
        $(term_id).addClass('droptrue');
        $(term_id).find('i').text('Off?');
    } else {
        $(term_id).addClass('off-term');
        $(term_id).removeClass('droptrue');
        $(term_id).find('i').text('On?');
    }

    var post_opposite = $.post('/swapterm', { term: term });


    // Remove all courses in term
    $(term_id + " li:not(.pin)").each(function(index, item) {
        var course = $(item);

        var posting = $.post('/removecourse', { course: course.attr("id"), term: term });

        course.parent().remove();
    })

}


function showCourses(dept){
    var posting = $.post('/getcourses', { dept: dept });
    
    posting.done(function (data) {
        $(".classesBlock ul.sortable1").empty();
        $.each(data['courses'], function(index, item) {
            $(".classesBlock ul.sortable1").append("<div='row-fluid'> <div='span12'> <li class='ui-state-default draggable' id='" + item['full_name'] + "' >" + item['full_name'] + "</li> </div> </div>");
        });

    });
}
