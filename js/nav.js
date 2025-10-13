$(document).ready(function() {
    // 获取当前页面路径，确定当前激活的菜单项
    var currentPage = window.location.pathname.split('/').pop();
    
    // 根据当前页面设置初始slide位置
    var activeIndex = getActiveMenuIndex(currentPage);
    setSlidePosition(activeIndex);
    
    // 点击事件 - 保存状态到localStorage
    $(".nav ul li a").on("click", function(e) {
        // 如果点击的是子菜单项，不改变slide位置
        if (!$(this).parents(".submenu").length) {
            var index = $(this).parent().index() - 2; // 减去两个slide元素
            // 保存当前激活的菜单索引到localStorage
            localStorage.setItem('activeNavIndex', index);
            localStorage.setItem('activeNavPage', currentPage);
            
            var position = $(this).parent().position();
            var width = $(this).parent().width();
            $(".slide1").css({
                opacity: 1,
                left: position.left,
                width: width
            });
        }
    });
    
    // 鼠标悬停事件
    $(".nav ul li a").on("mouseover", function(e) {
        // 如果悬停的是子菜单项，不触发slide2效果
        if (!$(this).parents(".submenu").length) {
            var position = $(this).parent().position();
            var width = $(this).parent().width();
            $(".slide2").css({
                opacity: 1,
                left: position.left,
                width: width
            }).addClass("squeeze");
        }
    });
    
    // 鼠标移出事件
    $(".nav ul li a").on("mouseout", function(e) {
        // 检查鼠标是否移动到了子菜单上
        if (!$(e.relatedTarget).parents(".submenu").length) {
            $(".slide2").css({ opacity: 0 }).removeClass("squeeze");
        }
    });
    
    // 为了确保子菜单显示时slide效果不消失
    $(".submenu").on("mouseover", function(e) {
        e.stopPropagation();
        // 保持slide2的状态
        $(".slide2").css({ opacity: 1 });
    });
    
    $(".submenu").on("mouseout", function(e) {
        e.stopPropagation();
        // 检查鼠标是否移出了整个菜单项
        if (!$(e.relatedTarget).parents(".has-submenu").length) {
            $(".slide2").css({ opacity: 0 }).removeClass("squeeze");
        }
    });
    
    // 根据页面路径获取激活菜单索引
    function getActiveMenuIndex(page) {
        switch(page) {
            case 'home.html':
                return 0; // 首页对应第一个菜单项
            case 'culture.html':
                return 1; // 陶瓷文化对应第二个菜单项
            case 'community.html':
                return 2; // 社区对应第三个菜单项
            case 'profile.html':
                return 3; // 个人中心对应第四个菜单项
            default:
                return 0; // 默认首页
        }
    }
    
    // 设置slide位置
    function setSlidePosition(index) {
        // 获取对应的菜单项
        var $menuItem = $(".nav ul li").eq(index + 2); // 前两个是slide元素
        
        if ($menuItem.length > 0) {
            var position = $menuItem.position();
            var width = $menuItem.width();
            
            $(".slide1").css({
                opacity: 1,
                left: position.left,
                width: width
            });
        }
    }
});