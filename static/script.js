$(function() {
    function addUserImageToDB() {
        var imageId = $(this).data("image");

        payload = {"image_id": imageId};

        $.post("/favorite_image", payload, function(data) {
           
            var heart = $("#image-" + imageId);
           
            heart.addClass("heart-full glyphicon-heart");
            heart.removeClass("heart-empty glyphicon-heart-empty");

            // Add another event listener
            heart.off("click");
            heart.on("click", removeUserImageFromDB);
        });
    }


    function removeUserImageFromDB() {
        var imageId = $(this).data("image");

        payload = {"image_id": imageId};

        $.post("/remove_image", payload, function(data) {
            console.log(imageId);
            var heart = $("#image-" + imageId);

            heart.addClass("heart-empty glyphicon-heart-empty");
            heart.removeClass("heart-full glyphicon-heart");

            heart.off("click");
            heart.on("click", addUserImageToDB);
        });
    }

    function removeImageFromProfile() {
        console.log("Removing closest .image-with-palette")
        $(this).closest('.image-with-palette').remove();
    }

    $(".profile-image").on("click", removeImageFromProfile);
    $(".heart-empty").on("click", addUserImageToDB);
    $(".heart-full").on("click", removeUserImageFromDB);


    function toggleDemoTextOnProfile() {
        console.log("Toggling demo text")
        $('#profile_demo_text').toggle();
    }

    $(".demo_images span.heart-empty").on("click", toggleDemoTextOnProfile);

});





