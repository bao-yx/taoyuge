(function($) {
    $.fn.timeline = function() {
        var selectors = {
            id: $(this),
            item:$(this).find(".item"),
            activeClass: "item--active",
            img: ".img"
        };
        selectors.item.eq(0).addClass(selectors.activeClass);
        selectors.id.css(
            "background-image",
             'url(' + selectors.item.first().find(selectors.img).attr("src") + ')'
        );
        var itemLength = selectors.item.length;
        var windowHeight = $(window).height();
        
        // 初始激活检查
        updateActiveItem();
        
        $(window).scroll(function() {
            updateActiveItem();
        });
        
        function updateActiveItem() {
            var pos = $(window).scrollTop();
            var viewportMiddle = pos + windowHeight / 2;
            var closestItem = null;
            var minDistance = Infinity;
            
            selectors.item.each(function(i) {
                var min = $(this).offset().top;
                var itemHeight = $(this).height();
                var itemMiddle = min + itemHeight / 2;
                var distance = Math.abs(viewportMiddle - itemMiddle);
                
                // 找到距离视口中间最近的项目
                if (distance < minDistance) {
                    minDistance = distance;
                    closestItem = $(this);
                }
            });
            
            // 激活距离最近的项目
            if (closestItem && minDistance < windowHeight) {
                selectors.item.removeClass(selectors.activeClass);
                closestItem.addClass(selectors.activeClass);
                selectors.id.css(
                    "background-image",
                    'url(' + closestItem.find(selectors.img).attr("src") + ')'
                );
            }
        }
        
        // 窗口大小变化时重新计算
        $(window).resize(function() {
            windowHeight = $(window).height();
        });
    };
})(jQuery);

// 确保DOM加载完成后再执行
$(document).ready(function() {
    $('#history').timeline();
});