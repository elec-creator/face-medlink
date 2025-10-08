const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const statusText = document.getElementById('status');
const captureBtn = document.getElementById('captureBtn');
const nameInput = document.getElementById('name');

let captureCount = 0;
const totalCaptures = 7;

// Aktifkan kamera
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => { video.srcObject = stream; })
  .catch(err => alert("Kamera tidak bisa diakses: " + err));

captureBtn.onclick = async () => {
  const name = nameInput.value.trim();
  if (!name) {
    alert("Masukkan nama dulu!");
    return;
  }

  if (captureCount >= totalCaptures) {
    alert("Sudah 7 foto diambil!");
    return;
  }

  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = canvas.toDataURL('image/jpeg');

  statusText.textContent = "Mengunggah foto...";

  const res = await fetch('/save_face', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: name, image: imageData })
  });

  const data = await res.json();
  if (data.status === "ok") {
    captureCount++;
    statusText.textContent = `✅ ${data.message}`;
    captureBtn.textContent = `Ambil Foto (${captureCount+1}/7)`;
    if (captureCount >= totalCaptures) {
      captureBtn.disabled = true;
      statusText.textContent = "✅ Semua 7 foto berhasil disimpan!";
    }
  } else {
    statusText.textContent = "⚠️ " + data.message;
  }
};
