const recordMyVoice = async () => {
    const stat = document.getElementById("status");
    stat.textContent = "Status: Started Recording...";

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream), chunks = [];

    mediaRecorder.ondataavailable = event => chunks.push(event.data);

    mediaRecorder.onstop = async () => {
        stat.textContent = "Status: Processing on Data...";

        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
    
        await fetch('/process-audio', { method: 'POST', body: formData,
        }).then(res => res.json()).then(data => stat.textContent = data);
    };
    
    mediaRecorder.start();
    console.log("started");
    
    setTimeout(() => {
        mediaRecorder.stop(); stream.getTracks().forEach(track => track.stop());
        console.log("stopped")
    }, 10000);
}
