function displayFileName(input) {
    const fileName = input.files[0].name;
    const outputDiv = document.getElementById('output');
    outputDiv.textContent = `Selected file: ${fileName}`;
}