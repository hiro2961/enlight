// realtime_preview.js

document.addEventListener('DOMContentLoaded', function() {
    // プレビュー対象となる画像フィールドのIDリスト
    const imageFields = ['image1', 'image2', 'image3', 'image4', 'image5'];

    imageFields.forEach(function(fieldName) {
        const inputId = 'id_' + fieldName;
        const previewId = 'preview_' + fieldName;

        const inputElement = document.getElementById(inputId);
        const livePreview = document.getElementById(previewId + '_live');
        const existingPreview = document.getElementById(previewId + '_existing');
        
        if (inputElement) {
            inputElement.addEventListener('change', function(event) {
                const file = event.target.files[0];
                
                if (existingPreview) {
                    existingPreview.style.display = 'none'; // 既存画像を非表示
                }

                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        livePreview.innerHTML = '<img src="' + e.target.result + '" style="max-width: 200px; height: auto; border: 2px solid #007bff;">';
                    };
                    reader.readAsDataURL(file);
                } else {
                    livePreview.innerHTML = '';
                    if (existingPreview) {
                        existingPreview.style.display = 'block'; // ファイルが選択されなければ元に戻す
                    }
                }
            });
        }
    });
});