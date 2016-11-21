
$(function() {
    function addUserImageToDB() {
        var imageId = $(this).data("image");
        payload = {"image_id": imageId};

        $.post("/favorite_image", payload, function(data) {
           
            var star = $("#image-" + imageId);
           
            star.addClass("star-full glyphicon-star");
            star.removeClass("star-empty glyphicon-star-empty");

            star.on("click", removeImage);
        });
    }


    function removeUserImageFromDB() {
        var imageId = $(this).data("image");
        payload = {"image_id": imageId};

        $.post("/remove_image", payload, function(data) {
            var star = $("#image-" + imageId);

            star.addClass("star-empty glyphicon-star-empty");
            star.removeClass("star-full glyphicon-star");

            star.on("click", favoriteImage);
        });
    }

    function removeImageFromPage() {
        $(this).closest('.image-with-palette').remove();

    }

    $(".profile-image").on("click", removeImageFromPage);
    $(".star-empty").on("click", addUserImageToDB);
    $(".star-full").on("click", removeUserImageFromDB);

});