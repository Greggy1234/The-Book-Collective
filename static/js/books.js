// These functions are for the book app
// Button element event listeners
// Once the DOM is loaded, the functions here can then follow
document.addEventListener("DOMContentLoaded", function () {
    let buttons = document.getElementsByTagName("button");
    for (let button of buttons) {
        button.addEventListener("click", function () {
            if (button.id == "edit-review-book-page-button") {
                editReview();
            } else if (button.id == "edit-rating-book-page-button") {
                editRating();
            } else if (button.id == "change-status-button") {
                showStatusButtons();
            }
        });
    }
});

/**
 * This is the function to change the displayed review text into a new form where a user can edit
 */
function editReview() {
    const editReviewButton = document.getElementById("edit-review-book-page-button");
    const preWrittenReview = document.getElementById("pre-edit-review");
    const reviewFormContainer = document.getElementById("hidden-edit-review-form-book-page");
    const deleteReviewButton = document.getElementById("delete-review-book-page-button");
    const reviewTextArea = document.getElementById("id_review");
    const fullUserReviewContainer = document.getElementById("full-user-review");
    let fullUserReview = fullUserReviewContainer.innerText;
    editReviewButton.classList.add("d-none");
    preWrittenReview.classList.add("d-none");
    deleteReviewButton.classList.add("d-none");
    reviewFormContainer.classList.remove("d-none");
    reviewTextArea.innerText = fullUserReview;
}

/**
 * This is the function to change the displayed rating by showing the rating options form again
 */
function editRating() {
    const editRatingButton = document.getElementById("edit-rating-book-page-button");
    const preRating = document.getElementById("pre-edit-rating");
    const ratingFormContainer = document.getElementById("hidden-edit-rating-form-book-page");
    const deleteRatingButton = document.getElementById("delete-rating-book-page-button");
    editRatingButton.classList.add("d-none");
    preRating.classList.add("d-none");
    deleteRatingButton.classList.add("d-none");
    ratingFormContainer.classList.remove("d-none");
}

/**
 * This is the function that shows the different status buttons
 */
function showStatusButtons() {
    const changeStatusButtton = document.getElementById("change-status-button");
    const statusButton = document.getElementById("status-buttons");
    changeStatusButtton.classList.add("d-none");
    statusButton.classList.remove("d-none");
}