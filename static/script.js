console.log('scripts are successfully loaded'); // Debugging

// Activate Lucide icons
lucide.createIcons();

// Select DOM elements
const preview = document.getElementById('previewImage');
const imageInput = document.getElementById('image');  // ✅ corrected here
const resultText = document.getElementById('result');

// Display image preview when a file is selected
imageInput.addEventListener('change', () => {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview.src = e.target.result;
            preview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

// Upload image and get prediction result
async function uploadImage() {
    const file = imageInput.files[0];
    if (!file) {
        resultText.innerText = '🚫 Please select an image.';
        return;
    }

    resultText.innerText = '⏳ Predicting...';

    const formData = new FormData();
    formData.append('image', file);

    try {
        const res = await fetch('/predict', {
            method: 'POST',
            body: formData,
        });

        const data = await res.json();

        if (data.error) {
            resultText.innerText = `❌ Error: ${data.error}`;
        } else if (data.image) {
            const resultImage = document.getElementById('result-image');
            if (resultImage) {
                resultImage.src = "data:image/png;base64," + data.image;
                resultImage.style.display = "block";
            }
            resultText.innerText = '';
        } else {
            resultText.innerText = '⚠️ Unexpected response.';
        }
    } catch (err) {
        console.error('Error:', err);
        resultText.innerText = '❌ Something went wrong. Please try again.';
    }
}


// Attach event listener to form
const form = document.getElementById('upload-form');
const uploadForm = document.getElementById('upload-form');
uploadForm.addEventListener('submit', (e) => {
    e.preventDefault(); // prevent the page from refreshing
    uploadImage();
});
