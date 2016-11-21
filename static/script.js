var myThis

function favoriteImage() {
    var imageId = $(this).data("image");

    payload = {"image_id": imageId};

    $.post("/favorite_image", payload, function(data) {
        console.log(imageId);
        var button = $("#image-" + imageId)


        button.addClass("remove-image-btn");
        button.addClass("glyphicon-star");
        button.removeClass("favorite-image-btn");
        button.removeClass("glyphicon-star-empty");
        button.off("click");
        // Add '/remove-favorite' listener




    });
}


$(".favorite-image-btn").on("click", favoriteImage);


// 

// function(data) is the success function
// Then toggle star classes in f(x)
