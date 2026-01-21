// These functions are for the reviewapp
// Button element event listeners
// Once the DOM is loaded, the functions here can then follow
document.addEventListener("DOMContentLoaded", function () {
    let reviewTextElement = document.getElementById("review-text-review-page");
    let reviewText = reviewTextElement.innerText;
    let buttons = document.getElementsByTagName("button");
    for (let button of buttons) {
        button.addEventListener("click", function () {
            if (button.id == "edit-review-review-page-button") {
                editReview(reviewText);
            } else if (button.id == "edit-rating-review-page-button") {
                editRating();
            }
        });
    }
});

/**
 * This is the function to change the displayed review text into a new form where a user can edit
 */
function editReview(reviewText) {
    const reviewRating = document.getElementById("review-rating-review-page");
    const reviewEditDeleteButtons = document.getElementById("review-edit-delete-review-page");
    const ratingEditDeleteButtons = document.getElementById("rating-edit-delete-review-page");
    const reviewFormContainer = document.getElementById("hidden-edit-review-form-review-page");
    const reviewTextArea = document.getElementById("id_review");
    reviewTextArea.innerText = reviewText;    
    reviewRating.classList.add("d-none");
    reviewEditDeleteButtons.classList.remove("d-flex");
    ratingEditDeleteButtons.classList.remove("d-flex");
    reviewEditDeleteButtons.classList.add("d-none");
    ratingEditDeleteButtons.classList.add("d-none");
    reviewFormContainer.classList.remove("d-none");    
}

/**
 * This is the function to change the displayed rating by showing the rating options form again
 */
function editRating() {
    const reviewRating = document.getElementById("review-rating-review-page");
    const reviewEditDeleteButtons = document.getElementById("review-edit-delete-review-page");
    const ratingEditDeleteButtons = document.getElementById("rating-edit-delete-review-page");
    const ratingFormContainer = document.getElementById("hidden-edit-rating-form-review-page");
    reviewRating.classList.add("d-none");
    reviewEditDeleteButtons.classList.remove("d-flex");
    ratingEditDeleteButtons.classList.remove("d-flex");
    reviewEditDeleteButtons.classList.add("d-none");
    ratingEditDeleteButtons.classList.add("d-none");
    ratingFormContainer.classList.remove("d-none"); 
}