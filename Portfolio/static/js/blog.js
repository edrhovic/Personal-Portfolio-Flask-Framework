const imageModal = document.getElementById('imageModal');
        imageModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const imageSrc = button.getAttribute('data-bs-img');
            const imageTitle = button.getAttribute('data-bs-title');
            const modalImage = document.getElementById('modalImage');
            modalImage.src = imageSrc;
            document.getElementById('imageModalLabel').textContent = imageTitle;
        });


