// Initialize CKEditor
CKEDITOR.replace('note-description');
const data = document.currentScript.dataset;

// Tags handling
var tagsArray = []
console.log(data.tags)
if (data.tags != "") {
    tagsArray = data.tags.split(",");
    updateTagsContainer();
}

function addTag() {
    var tagInput = $('#tag-input');
    var tagValue = tagInput.val().trim();

    if (tagValue !== '') {
        // Check if the tag already exists
        if (tagsArray.indexOf(tagValue) === -1) {
            // Add tag to the array
            tagsArray.push(tagValue);

            // Update the tags-container
            updateTagsContainer();
            // Clear the input field
            tagInput.val('');
        }
    }
}

function removeTag(tagValue) {
    // Remove tag from the array
    tagsArray = tagsArray.filter(function (tag) {
        return tag !== tagValue;
    });

    // Update the tags-container
    updateTagsContainer();
}

function updateTagsContainer() {
    var tagContainer = $('#tags-container');
    tagContainer.empty();

    for (var i = 0; i < tagsArray.length; i++) {
        var tagElement = $('<div class="badge badge-primary m-1"></div>').text(tagsArray[i]);
        var removeButton = $('<button type="button" class="btn btn-danger btn-sm ml-1">Remove</button>');

        // Event handler for removing the tag
        removeButton.click(createRemoveHandler(tagsArray[i]));

        tagElement.append(removeButton);
        tagContainer.append(tagElement);
    }
    // Update the hidden input field with the serialized tagsArray
    $('#tags-array').val(JSON.stringify(tagsArray));
}

function createRemoveHandler(tagValue) {
    return function () {
        removeTag(tagValue);
    };
}