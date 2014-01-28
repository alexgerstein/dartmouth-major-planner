var MAX_COURSES = 4

function flash_alert(alert) {
    $(".flash").text("");
    $(".flash").text(alert);

    $( ".flash" ).show();
    $(".flash").removeClass('hide');

    $('.flash').delay(7000).fadeOut(400);
}

function getHoursUl(possible_hours, hour) {
    var hour_text = '<div class="btn-group"><button class="btn dropdown-toggle btn-mini" data-toggle="dropdown"><i class="selected-hour">' + hour + ' </i><span class="caret"></span></button><ul class="dropdown-menu">'
    $.each(possible_hours, function(key, value) {
        if (value != hour) {
            hour_text = hour_text + '<li class="hour"><a>' + value + '</a></li>';
        }
    });

    return hour_text + '</ul></div>'
}

function addCourse(term, hour, possible_hours, offering_id, short_name) {

    var obj = ($(".termsBlock").find(term));

    var hour_text = getHoursUl(possible_hours, hour);

    obj.append('<div class="row-fluid"> <div class="span12"> <li id="' + offering_id + '" class="ui-state-default draggable"> <div class="row-fluid"> <div class="span12">' + short_name + '<span class="buttons">' + hour_text + '<i class="btn btn-danger btn-small hidden-phone"><span class="icon-trash icon-white"></i> <i class="btn btn-info btn-small popover-trigger" data-toggle="popover"><span class="icon-info-sign"></i></span> </div> </div> </li> </div> </div>');

    $('i.btn-danger').click(removeCourse);

    var course_desc = null;

    var posting = $.get("/getCourseInfo",
        {
            offering: offering_id,
            term: obj.attr('id'),
        })

    posting.fail (function (response) {
        flash_alert("There was an error loading the course description. Please try reloading the page.");
        return
    })

    posting.done(function(response) {
            $('#' + offering_id).find('.popover-trigger').popover(  {
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
    var posting;
    var offering = false;
    if (ui.item.parent().parent().parent().hasClass('sortable2')) {
        posting = $.get('/findterms', { offering: ui.item.attr('id') });
    } else {
        posting = $.get('/findterms', { course: ui.item.attr('id') });
    }

    $(".progress").removeClass("hide");

    posting.fail(function (data) {
        $(".progress").addClass("hide");
        flash_alert("We seem to be having some technical difficulties. Please check your internet connection and try again.")
        return
    })

    posting.done(function (data) {

        $(".progress").addClass("hide");

        $.each(data['terms'], function(index, item) {
            term_id = "#" + item[0];
            if ($(term_id).hasClass('off-term')) {
                $(term_id).addClass('available-off');
            } else {
                $(term_id).addClass('available');
            }

            if (item[1] == 1) {
                other = "other"
            } else {
                other = "others"
            }
            $(term_id).prepend('<div class="count">Planned by ' + item[1] + ' ' + other + '</div>');
        });

        $.each(data['user_terms'], function(index, item) {
            term_id = "#" + item[0];
            if ($(term_id).hasClass('off-term')) {
                $(term_id).addClass('available-user-off');
            } else {
                $(term_id).addClass('available-user');
            }

            if (item[1] == 0) {
                other = "other"
            } else {
                other = "others"
            }
            $(term_id).prepend('<div class="count">Planned by ' + item[1] + ' ' + other + '</div>');
        });
    });
}

function clearAvailableSlots(event, ui) {
    $('.sortable2').each( function(index, item) {
        $(this).removeClass('available');
        $(this).removeClass('available-off');
        $(this).removeClass('available-user');
        $(this).removeClass('available-user-off');
        $('.count').remove();
    });
}

function saveCourse(event, ui) {

    var selectVal = $('#dept_name').find(":selected").val();

    var course_id = ui.item.attr('id');

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

    var senderclass = ui.sender.attr('class');

    var posting;
    if (senderclass.indexOf('sortable2') >= 0) {
        posting = $.post('/savecourse', { offering: course_id, term: term_id });
    } else {
        posting = $.post('/savecourse', { course: course_id, term: term_id });
    }

    posting.fail (function (data) {
        flash_alert("There was an error saving the course. Please check your internet connection and try again.");
        return
    })

    posting.done(function (data) {
        var senderclass = ui.sender.attr('class');

        if (data['error']) {
        	return;
        }

        if (senderclass.indexOf('sortable2') >= 0) {
            var course_hour = ui.sender.find('li:contains(' + data['name'] + ')').find('.selected-hour').text();
        	var postremove = $.post('/removecourse', { offering: course_id, term: ui.sender.attr('id'), hour: course_hour.split(' ')[0] })

    		$("#" + ui.sender.attr('id') + " li").each(function(index, li) {
    			var course = $(li);
    			if (course.attr('id') == course_id) {
    				course.parent().remove();
    			};
    		});
        }
        var hours = data['possible_hours'].split("; ");

        addCourse(ext_term_id, data['hour'], hours, data['id'], data['name']);

    });

}

$(document).on('click', '.dropdown-menu li a', function () {
    var course_item = $(this).parents('.draggable');
    var new_hour = $(this).text();
    var term = $(this).parents('.sortable2').attr('id');
    var offering_id = course_item.attr('id');

    var posting = $.post('/swaphour', { offering: offering_id, term: term, new_hour: new_hour, hour: course_item.find(".dropdown-toggle").text().split(" ")[0] });

    posting.fail (function (data) {
        flash_alert("There was an error swapping hours. Please check your internet connection and try again.");
        return
    })

    posting.done(function (data) {

        if (data['error']) {
            return;
        }

        var hoursUl = course_item.find('.btn-group').remove();
        var possibleHourArray = data['possible_hours'].split('; ');

        var newHoursUl = getHoursUl(possibleHourArray, new_hour);

        course_item.find('.buttons').prepend(newHoursUl);

        course_item.attr('id',   data['id']);

    });

});

function removeCourse(event){
    var that = $ (this)
    var term_id = that.parents('ul').attr('id');

    var posting = $.post('/removecourse',
        { offering: $(this).parents("li").attr("id"),
        term: term_id,
        hour: $(this).parents("li").find(".dropdown-toggle").text().split(" ")[0] })

    posting.fail (function (data) {
        flash_alert("We encountered an issue removing that course. Please check your internet connection and try again.");
        return
    })

    posting.done (function (data) {
        that.parents('li').parent().remove();
    })

}

function swap_term(term){

    var term_id = "#" + term;

    if (!$(term_id).hasClass('off-term')) {
        if (!confirm('Are you sure you would like to mark this term as off? This will remove all listed courses for the term.')) {
            return
        }
    }

    var post_opposite = $.post('/swapterm', { term: term });

    post_opposite.fail (function (data) {
        flash_alert("There was an issue with swapping the term. Please check your internet connection and try again.");
        return;
    })

    post_opposite.done( function (data) {
        // Remove all courses in term
        $(term_id + " li").each(function(index, item) {
            var course = $(item);
            course.parent().remove();
        })

        // Mark term as off
        if ($(term_id).hasClass('off-term')) {
            $(term_id).removeClass('off-term');
            $(term_id).siblings('li').find('i').text('Off?');
        } else {
            $(term_id).siblings('li').find('i').text('On?');
            $(term_id).addClass('off-term');
        }
    })
}


function showCourses(){
    $('.sortable1').scrollTop(0);
    var dept = $('#dept_name').find(":selected").val();
    var term = $('#term_name').find(":selected").val();
    var hour = $('#hour_name').find(":selected").val();

    var getcourses = $.get('/getcourses', { dept: dept, term: term, hour: hour });


    $(".classesBlock ul.sortable1").empty();
    if (dept != "-1" || term != "-1" || hour != "-1") {
        $(".classesBlock ul.sortable1").append("<li class='loading'>Loading...</li>");
    }

    getcourses.fail(function (data) {
        $(".classesBlock ul.sortable1").empty();
        flash_alert("Oops! We're having trouble displaying the courses. Please check your internet connection and try again.");
    })

    getcourses.done(function (data) {
        $(".classesBlock ul.sortable1").empty();
        $.each(data['courses'], function(index, item) {
            $(".classesBlock ul.sortable1").append("<div='row-fluid'> <div='span12'> <li class='ui-state-default draggable' id='" + item['id'] + "' >" + item['full_name'] + "</li> </div> </div>");
        });

    });
}
