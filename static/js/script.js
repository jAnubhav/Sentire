const recordMyVoice = async () => {
    const stat = document.getElementById("status");
    stat.textContent = "Status: Started Recording...";

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream), chunks = [];

    mediaRecorder.ondataavailable = event => chunks.push(event.data);

    mediaRecorder.onstop = async () => {
        stat.textContent = "Status: Processing on Data...";

        const formData = new FormData(); 
        formData.append('audio', new Blob(chunks, { type: 'audio/webm' }));
    
        await fetch('/process-audio', { method: 'POST', body: formData })
        .then(res => res.json()).then(data => stat.textContent = `Result: ${data["data"]}`);
    };
    
    mediaRecorder.start();
    
    setTimeout(() => {
        mediaRecorder.stop(); stream.getTracks().forEach(track => track.stop());
    }, 10000);
}
