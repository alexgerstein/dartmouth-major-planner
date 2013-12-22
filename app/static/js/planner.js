var MAX_COURSES = 4

function getHoursUl(possible_hours, hour) {
    var hour_text = '<div class="btn-group"><button class="btn dropdown-toggle btn-mini" data-toggle="dropdown"><i class="selected-hour">' + hour + ' </i><span class="caret"></span></button><ul class="dropdown-menu">'
    $.each(possible_hours, function(key, value) {
        if (value != hour) {
            hour_text = hour_text + '<li class="hour"><a>' + value + '</a></li>';
        }
    });

    return hour_text + '</ul></div>'
}

function addCourse(term, hour, possible_hours, course, short_name) {

    var obj = ($(".termsBlock").find(term));

    var hour_text = getHoursUl(possible_hours, hour);

    obj.append('<div class="row-fluid"> <div class="span12"> <li id="' + course + '" class="ui-state-default draggable"> <div class="row-fluid"> <div class="span12">' + short_name + '<span class="buttons">' + hour_text + '<i class="btn btn-danger btn-small hidden-phone"><span class="icon-trash icon-white"></i> <i class="btn btn-info btn-small popover-trigger" data-toggle="popover"><span class="icon-info-sign"></i></span> </div> </div> </li> </div> </div>');

    $('i.btn-danger').click(removeCourse);

    var course_desc = null;

    $.post("/getCourseInfo", 
        {
            course: course,
            term: obj.attr('id')
        }, 
        function(response) {
            var split_id = course.split(" ")
            var course_id = obj.find('li:contains(' + short_name + ')');

            $(course_id.find('.popover-trigger')).popover(  {
                content: response['info'],
                title: 'Course Info',
                html: true,
                placement:function (context, source) {
                    var position = $(source).position();
                    var width = window.innerWidth;

                    if (width < 768) {
                        return "left";
                    }

                    if (position.left > 900) {
                        return "left";
                    }

                    if (position.top < 250){
                        return "bottom";
                    }

                    if (position.top > 600){
                        return "top";
                    }

                    if (position.left < 800) {
                        return "right";
                    }

                    return "left";
                },
                delay: {show:500, hide: 100}
            });
        }
    )
};

function showAvailableSlots(event, ui) {
    var posting = $.post('/findterms', { course: ui.item.attr('id') });

    $(".progress").removeClass("hide");

    posting.done(function (data) {

        $(".progress").addClass("hide");
        
        $.each(data['terms'], function(index, item) {
            term_id = "#" + item;
            if ($(term_id).hasClass('off-term')) {
                $(term_id).addClass('available-off');
            } else {
                $(term_id).addClass('available');
            }
        });

        $.each(data['user-terms'], function(index, item) {
            term_id = "#" + item;
            if ($(term_id).hasClass('off-term')) {
                $(term_id).addClass('available-user-off');
            } else {
                $(term_id).addClass('available-user');
            }
        });
    });
}

function clearAvailableSlots(event, ui) {
    $('.sortable2').each( function(index, item) {
        $(this).removeClass('available');
        $(this).removeClass('available-off');
        $(this).removeClass('available-user');
        $(this).removeClass('available-user-off');
    });
}

function saveCourse(event, ui) {
    


    var selectVal = $('#dept_name').find(":selected").val();

    var text = ui.item.attr('id');

    var term_id = ($( this ).attr("id"));
    var ext_term_id = "#" + term_id;

    if ($(ext_term_id + " li:not(.hour)").length > MAX_COURSES + 1) {
        alert("Maximum courses exceeded for this term.");
        return;
    }

    if ($(this).hasClass('off-term')) {
        alert("You cannot add courses to off terms.");
        return;
    }

    if ($(this).hasClass('available') == false) {
        if (confirm('Are you sure you want to put the course here? According to our records, it might not be offered this term. Please consult the latest registrar listing to verify.') != true) {
            return;
        }
    }


    var posting = $.post('/savecourse', { course: text, term: term_id });

    posting.done(function (data) {
        var senderclass = ui.sender.attr('class');

        if (data['error']) {
        	return;
        }

        if (senderclass.indexOf('sortable2') >= 0) {
            var course_hour = ui.sender.find('li:contains(' + data['name'] + ')').find('.selected-hour').text();
        	var postremove = $.post('/removecourse', { course: text, term: ui.sender.attr('id'), hour: course_hour.split(' ')[0] })

    		$("#" + ui.sender.attr('id') + " li").each(function(index, li) {
    			var course = $(li);
    			if (course.attr('id') == text) {
    				course.parent().remove();
    			};
    		});
        }
        var hours = data['possible_hours'].split("; ");
        
        addCourse(ext_term_id, data['hour'], hours, text, data['name']);

    });
        
}

$(document).on('click', '.dropdown-menu li a', function () {
    var course_item = $(this).parents('.draggable');
    var new_hour = $(this).text();
    var term = $(this).parents('.sortable2').attr('id');
    var course = course_item.attr('id');
    
    var posting = $.post('/swaphour', { course: course, term: term, new_hour: new_hour, hour: course_item.find(".dropdown-toggle").text().split(" ")[0] });

    posting.done(function (data) {

        if (data['error']) {
            return;
        }

        var hoursUl = course_item.find('.btn-group').remove();
        var possibleHourArray = data['possible_hours'].split('; ');

        var newHoursUl = getHoursUl(possibleHourArray, new_hour);

        course_item.find('.buttons').prepend(newHoursUl);

    });

});

function removeCourse(event){
    var term_id = $( this ).parents('ul').attr('id');

    var posting = $.post('/removecourse', { course: $(this).parents("li").attr("id"), term: term_id, hour: $(this).parents("li").find(".dropdown-toggle").text().split(" ")[0] });

    $(this).parents('li').parent().remove();

}

function swap_term(term){

    var term_id = "#" + term;

    // Mark term as off
    if ($(term_id).hasClass('off-term')) {
        $(term_id).removeClass('off-term');
        $(term_id).find('i').text('Off?');
    } else {
        $(term_id).addClass('off-term');
        $(term_id).find('i').text('On?');
    }

    var post_opposite = $.post('/swapterm', { term: term });


    // Remove all courses in term
    $(term_id + " li:not(.pin)").each(function(index, item) {
        var course = $(item);

        course.parent().remove();
    })

}


function showCourses(){
    $('.sortable1').scrollTop(0);
    var dept = $('#dept_name').find(":selected").val();
    var term = $('#term_name').find(":selected").val();
    var hour = $('#hour_name').find(":selected").val();

    var posting = $.post('/getcourses', { dept: dept, term: term, hour: hour });
    

    $(".classesBlock ul.sortable1").empty();
    if (dept != "-1" || term != "-1" || hour != "-1") { 
        $(".classesBlock ul.sortable1").append("<li class='loading'>Loading...</li>");
    }

    posting.done(function (data) {
        $(".classesBlock ul.sortable1").empty();
        $.each(data['courses'], function(index, item) {
            $(".classesBlock ul.sortable1").append("<div='row-fluid'> <div='span12'> <li class='ui-state-default draggable' id='" + item['full_name'] + "' >" + item['full_name'] + "</li> </div> </div>");
        });

    });
}
