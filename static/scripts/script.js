const helloWorld = () => {
    return 'Hello, World!';
}

// Get the value from the function
const message = helloWorld();

// Insert the value into the <p> element with id "dynamic-content"
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('dynamic-content').innerHTML = message;
});


const handleSubmit = () => {
    const form = document.getElementById('upload-form');
    form.submit();
}
