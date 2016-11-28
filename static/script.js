$(function() {
    function addUserImageToDB() {
        var imageId = $(this).data("image");

        payload = {"image_id": imageId};

        $.post("/favorite_image", payload, function(data) {
           
            var star = $("#image-" + imageId);
           
            star.addClass("star-full glyphicon-star");
            star.removeClass("star-empty glyphicon-star-empty");

            // Add another event listener
            star.on("click", removeUserImageFromDB);
        });
    }


    function removeUserImageFromDB() {
        var imageId = $(this).data("image");

        payload = {"image_id": imageId};

        $.post("/remove_image", payload, function(data) {
            console.log(imageId);
            var star = $("#image-" + imageId);

            star.addClass("star-empty glyphicon-star-empty");
            star.removeClass("star-full glyphicon-star");

            star.on("click", addUserImageToDB);
        });
    }

    function removeImageFromProfile() {
        console.log("Removing closest .image-with-palette")
        $(this).closest('.image-with-palette').remove();

    }

    $(".profile-image").on("click", removeImageFromProfile);
    $(".star-empty").on("click", addUserImageToDB);
    $(".star-full").on("click", removeUserImageFromDB);


    function removeDemoTextFromProfile() {
        console.log("Removing demo text")
        
        $('#profile_demo_text').toggle();

    }

    $(".demo_images span.star-empty").on("click", removeDemoTextFromProfile);

});





