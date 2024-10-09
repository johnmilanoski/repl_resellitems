document.addEventListener('DOMContentLoaded', function() {
    const addCustomFieldButton = document.getElementById('add-custom-field');
    const customFieldsContainer = document.getElementById('custom-fields-container');

    if (addCustomFieldButton && customFieldsContainer) {
        addCustomFieldButton.addEventListener('click', function() {
            const newField = document.createElement('div');
            newField.classList.add('custom-field', 'mb-4');
            newField.innerHTML = `
                <input type="text" name="custom_fields-${customFieldsContainer.children.length}-name" placeholder="Field Name" class="w-full px-3 py-2 border rounded-md">
                <input type="text" name="custom_fields-${customFieldsContainer.children.length}-value" placeholder="Field Value" class="w-full px-3 py-2 border rounded-md mt-2">
            `;
            customFieldsContainer.appendChild(newField);
        });
    }

    const photoInput = document.getElementById('photo-input');
    const photoPreviewContainer = document.getElementById('photo-preview-container');

    if (photoInput && photoPreviewContainer) {
        photoInput.addEventListener('change', function(event) {
            photoPreviewContainer.innerHTML = '';
            const files = event.target.files;
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const div = document.createElement('div');
                        div.className = 'relative mr-2 mb-2';
                        div.innerHTML = `
                            <img src="${e.target.result}" class="w-32 h-32 object-cover rounded-md">
                            <button type="button" class="absolute top-0 right-0 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center" onclick="removePhoto(this)">×</button>
                        `;
                        photoPreviewContainer.appendChild(div);
                    }
                    reader.readAsDataURL(file);
                }
            }
        });
    }
});

function removePhoto(button) {
    const photoDiv = button.closest('div');
    photoDiv.remove();
    updateFileInput();
}

function updateFileInput() {
    const photoInput = document.getElementById('photo-input');
    const photoPreviewContainer = document.getElementById('photo-preview-container');
    const dataTransfer = new DataTransfer();
    const files = photoPreviewContainer.querySelectorAll('img');
    files.forEach((file, index) => {
        const blob = dataURLtoBlob(file.src);
        dataTransfer.items.add(new File([blob], `photo_${index}.jpg`, { type: 'image/jpeg' }));
    });
    photoInput.files = dataTransfer.files;
}

function dataURLtoBlob(dataURL) {
    const arr = dataURL.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
}
