function openModal(imageSrc) {
    var modalImage = document.getElementById('modalImage');
    modalImage.src = imageSrc;
    document.getElementById('imageModal').style.display = 'block';
}

// Function to close the modal
function closeModal() {
    document.getElementById('imageModal').style.display = 'none';
}