document.addEventListener("DOMContentLoaded", function() {
    const fileInput        = document.getElementById('file-upload');
    const dropZone         = document.getElementById('drop-zone');
    const fileNameDisplay  = document.getElementById('file-name');
    const imagePreview     = document.getElementById('image-preview');
    const previewContainer = document.getElementById('preview-container');
    const loadingMessage   = document.getElementById('loading');
    const uploadForm       = document.getElementById('upload-form');
    const removeFileBtn    = document.getElementById('remove-file');
    const submitBtn        = document.getElementById('submit-btn');

    // Função para mostrar a prévia
    function showPreview(file) {
        fileNameDisplay.textContent = file.name;
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);

        removeFileBtn.style.display = 'inline-block';
    }

    // Função para remover imagem
    function removeFile() {
        fileInput.value = '';
        fileNameDisplay.textContent = 'Nenhum arquivo selecionado';
        imagePreview.src = '#';
        imagePreview.style.display = 'none';
        removeFileBtn.style.display = 'none';
    }

    // Evento de seleção (botão "Escolher Imagem")
    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            showPreview(file);
        } else {
            removeFile();
        }
    });

    // Drag & Drop
    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (event) => {
        event.preventDefault();
        dropZone.classList.remove('dragover');
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            showPreview(files[0]);
        }
    });

    // Validar envio se não tiver arquivo
    uploadForm.addEventListener('submit', function(e) {
        // Se não houver arquivo selecionado
        if (!fileInput.files || fileInput.files.length === 0) {
            e.preventDefault();  // Bloqueia envio
            alert('Por favor, selecione uma imagem antes de enviar!');
            return;
        }
        // Se houver arquivo, mostre a mensagem de loading
        loadingMessage.style.display = 'block';
    });

    // Remover imagem
    removeFileBtn.addEventListener('click', function() {
        removeFile();
    });
});
