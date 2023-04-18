$(".menu>li").mouseover(function(){
    $(this).children(".submenu").stop().slideDown();
});

$(".menu>li").mouseleave(function(){
    $(this).children(".submenu").stop().slideUp();
});

//이미지 슬라이드
var now = 0 //시작이미지
var imgs = 2; //이미지 개수

function slide(){
    if(now == imgs){
        now=0;
    }
    else{
        now++;
    }

    $(".slide>img").eq(now-1).css({"margin-top":"300px"});
    $(".slide>img").eq(now).css({"margin-top":"0px"});
}

setInterval(function(){slide();},2000);