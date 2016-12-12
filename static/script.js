$(function() {

    function addUserImageToDB() {
        var imageId = $(this).data("image");

        payload = {"image_id": imageId};

        $.post("/add_user_image", payload, function(data) {         
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

        $.post("/remove_user_image", payload, function(data) {
            console.log(imageId);
            var heart = $("#image-" + imageId);

            heart.addClass("heart-empty glyphicon-heart-empty");
            heart.removeClass("heart-full glyphicon-heart");

            heart.off("click");
            heart.on("click", addUserImageToDB);
        });
    }

    $(".heart-empty").on("click", addUserImageToDB);
    $(".heart-full").on("click", removeUserImageFromDB);




    function removeImageFromBrowser() {
        console.log("Removing closest .image-with-palette")
        $(this).closest('.image-with-palette').remove();
    }

    $(".profile-image").on("click", removeImageFromBrowser);
    





    function removeGalleryImageFromDB() {
        var imageId = $(this).data("image");
        payload = {"image_id": imageId};

        $.post("/remove_gallery_image", payload, function(data) {
            console.log("Sent request to remove from gallery: " + imageId);
            alert("Deleted gallery image " + imageId);
        });
    }

    $(".remove-gallery-image").on("click", removeGalleryImageFromDB);
    $(".remove-gallery-image").on("click", removeImageFromBrowser);






    function removeAllRecordsOfImage() {
        var imageId = $(this).data("image");
        payload = {"image_id": imageId};

        $.post("/remove_all_image_records", payload, function(data) {
            console.log(imageId);
            alert("Deleted record " + imageId);
        });
    }

    $(".remove-all-image-records").on("click", removeAllRecordsOfImage);
    $(".remove-all-image-records").on("click", removeImageFromBrowser);



    function toggleDemoTextOnProfile() {
        console.log("Toggling demo text")
        $('#profile_demo_text').toggle();
    }

    $(".demo_images span.heart-empty").on("click", toggleDemoTextOnProfile);

});





