(function($) {
    $.fn.timeline = function(options) {
        var settings = $.extend({
            activeRange: 1/4
        }, options);

        var selectors = {
            id: $(this),
            item: $(this).find(".item"),
            activeClass: "item--active",
            img: ".img"
        };

        selectors.item.eq(0).addClass(selectors.activeClass);
        selectors.id.css(
            "background-image",
            'url(' + selectors.item.first().find(selectors.img).attr("src") + ')'
        );

        var windowHeight = $(window).height();
        var activeRangePixel = windowHeight * settings.activeRange;

        updateActiveItem();

        $(window).on('scroll resize', updateActiveItem);

        function updateActiveItem() {
            var scrollTop = $(window).scrollTop();
            var viewportTop = scrollTop;
            var viewportBottom = scrollTop + windowHeight;
            var closestItem = null;
            var minDistance = Infinity;

            selectors.item.each(function() {
                var $item = $(this);
                var itemTop = $item.offset().top;
                var itemBottom = itemTop + $item.height();

                var itemMiddle = itemTop + $item.height() / 2;


                if (itemBottom >= viewportTop + activeRangePixel && itemTop <= viewportBottom - activeRangePixel) {

                    var distance = Math.abs(itemTop - viewportTop);


                    if (distance < minDistance) {
                        minDistance = distance;
                        closestItem = $item;
                    }
                }
            });


            if (closestItem) {
                selectors.item.removeClass(selectors.activeClass);
                closestItem.addClass(selectors.activeClass);
                selectors.id.css(
                    "background-image",
                    'url(' + closestItem.find(selectors.img).attr("src") + ')'
                );
            } else {

                selectors.item.removeClass(selectors.activeClass);
                selectors.item.eq(0).addClass(selectors.activeClass);
                selectors.id.css(
                    "background-image",
                    'url(' + selectors.item.first().find(selectors.img).attr("src") + ')'
                );
            }
        }
    };
})(jQuery);

$(document).ready(function() {
    $('#history').timeline({ activeRange: 0.1 });
});