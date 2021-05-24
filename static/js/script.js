$(document).ready(function () {

    //MOUSE ENTER FOR POSTS
    $(".outer").mouseenter(function () {

        $($(this).find('section:first')).animate({opacity: "0.1"}, 100);

    });


    //MOUSE LEAVE FOR POSTS
    $(".outer").mouseleave(function () {

        $($(this).find('section:first')).animate({opacity: "1"}, 100);

    });


    //MOUSE ENTER FOR ANCHORS
    $(".nav").mouseenter(function () {

        $(this).animate({backgroundColor: "#ffffff", color: "#2d2d2d"}, 100);

    });
    //MOUSE LEAVE FOR ANCHORS
    $(".nav").mouseleave(function () {

        $(this).animate({backgroundColor: "#2d2d2d", color: "#ffffff"}, 100);

    });

    //MOUSE ENTER FOR ANCHORS
    $(".nava").mouseenter(function () {

        $(this).animate({backgroundColor: "#ffffff", color: "#2d2d2d"}, 100);

    });
    //MOUSE LEAVE FOR ANCHORS
    $(".nava").mouseleave(function () {

        $(this).animate({backgroundColor: "#2d2d2d", color: "#ffffff"}, 100);

    });
});

function showMessage(msg) {
    alert(msg);
};
	
	
	

	


	
