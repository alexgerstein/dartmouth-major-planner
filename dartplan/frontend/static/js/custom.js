// JavaScript Document for FlatDuplex Landingpage

$(document).ready(function(){
	
	$('.scroll').click(function(){
		var mark = $(this).attr('id');
		var position = $('.'+mark).offset().top;
		$('html, body').animate({scrollTop:position - 90}, 'slow');
		return false;
		});
	
	// Header Slider
	$('.flexslider.notebookslider').flexslider({
		controlNav: true,
		directionNav: false
	});
	
	// Info Slider
	$('.flexslider.infoslider').flexslider({
		controlNav: false,
		animation: "slide",
		slideshowSpeed: 20000,
	});
	
	// Testimonials Slider
	$('.flexslider.testimonialslider').flexslider({
		controlNav: false,
		directionNav: false
	});
	
	// Gallery Slider
	$('.flexslider.galleryslider').flexslider({
		controlNav: true,
		animation: "slide",
		slideshow: false,
		directionNav: true
	});
	
	// Gallery Lightbox
	$('.gallery-img').magnificPopup({
		delegate: 'a', // child items selector, by clicking on it popup will open
		type: 'image'
	});
	
	
	// Hover Actions
	$('.hover').css('opacity', '1');
	  $('.hover').hover(
	    function () {
	       $(this).stop().animate({ opacity: 0.7 }, 'slow');
	    },
	    function () {  
	       $(this).stop().animate({ opacity: 1 }, 'slow');
	  });
	  
	  // About Profile Hover
	  $('.profile').hover(
			  function(){
				  $(this).find('.profile-image').addClass('profile-image-hover');
				  $(this).find('.profile-border-arrow').addClass('profile-border-arrow-hover');
			  },
			  function(){
				  $(this).find('.profile-image').removeClass('profile-image-hover');
				  $(this).find('.profile-border-arrow').removeClass('profile-border-arrow-hover');
			  }
		
	  );
	  
	  // Pricing Table Hover
	  $('.column').hover(
			  function(){
				  $(this).addClass('column-hover');
			  },
			  function(){
				  $(this).removeClass('column-hover');
			  }
		
	  );
	  
	  // Gallery Overlay
	  $('.gallery-img a').hover(
			  function(){
				  $(this).find('.img-overlay').animate({'top': '0'}, 'fast');
			  },
			  function(){
				  $(this).find('.img-overlay').animate({'top': '100%'}, 'fast');
			  }
		
	  );
	  
	  // Scroll Top Button
	  $('.scroll-top').click(function(){
		  $("html, body").animate({ scrollTop: 0 }, 'slow');
		  return false;
	  });

});