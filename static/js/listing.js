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
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.classList.add('w-32', 'h-32', 'object-cover', 'rounded-md', 'mr-2', 'mb-2');
                        photoPreviewContainer.appendChild(img);
                    }
                    reader.readAsDataURL(file);
                }
            }
        });
    }
});
