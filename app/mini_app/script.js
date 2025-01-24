document.getElementById('generateText').addEventListener('click', async () => {
    const response = await fetch('/generate_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: 'Напиши шутку про кенгуру' }),
    });
    const data = await response.json();
    alert(data.text);
});

document.getElementById('generateImage').addEventListener('click', async () => {
    const response = await fetch('/generate_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: 'кенгуру с ноутбуком' }),
    });
    const data = await response.json();
    if (data.image_url) {
        window.open(data.image_url, '_blank');
    } else {
        alert('Не удалось сгенерировать изображение.');
    }
});
