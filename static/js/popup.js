/*
 * Popup window handling
 */
function show_popup(title, url) {
    /* Fade out screen */
    var $mask = $("#noc-popup-mask");
    var ww = $(window).width();
    var wh = $(window).height();
    
    $mask.css({
        "width": ww,
        "height": $(document).height()
    });
    $mask.show();
    $mask.fadeIn(500);
    $mask.fadeTo("slow", 0.8);
    
    /* Show popup window */
    var $popup = $("#noc-popup-window");
    
    var margin = 50;
    $popup.css({
        "left": margin,
        "top": margin,
        "width": ww - 2 * margin,
        "height": wh - 2 * margin
    });

    var $title = $("#noc-popup-header-title");
    $title.text(title);
    /* @todo: FIX */
    $title.css({"left": ($popup.width() - $title.width()) / 2});
    
    $popup.show();
    /* Load URL */
    var $body = $("#noc-popup-body");
    
    $body.load(url);
    /* Return false to cancel link jumping */
    return false;
}

function hide_popup() {
    var $mask = $("#noc-popup-mask");
    $("#noc-popup-header-title").text("");
    $("#noc-popup-window").hide();
    $mask.fadeIn(500);
    $mask.fadeTo("show", 0);
    $mask.hide();
    $("#noc-popup-body").html("");
    
    return false;
}
