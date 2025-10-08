const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const resultText = document.getElementById('result');
const captureBtn = document.getElementById('captureBtn');

// Pastikan ukuran canvas sama dengan video
video.addEventListener('loadedmetadata', () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
});

// Aktifkan kamera
navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } })
  .then(stream => {
    video.srcObject = stream;
  })
  .catch(err => {
    console.error("Camera access error:", err);
    resultText.textContent = "⚠️ Tidak dapat mengakses kamera.";
  });

captureBtn.onclick = async () => {
  try {
    resultText.textContent = "🔍 Sedang memproses...";

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Kompres hasil gambar (opsional: untuk mempercepat upload)
    const imageData = canvas.toDataURL('image/jpeg', 0.8);

    const res = await fetch('/recognize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: imageData })
    });

    // Cek status HTTP dulu sebelum parse JSON
    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`);
    }

    const data = await res.json();

    if (data.status === "match") {
      resultText.textContent = "✅ Wajah cocok dengan: " + data.name;
      resultText.style.color = "white";
    } else if (data.status === "no_match") {
      resultText.textContent = "❌ Tidak ada kecocokan ditemukan.";
      resultText.style.color = "white";
    } else {
      resultText.textContent = "⚠️ " + (data.message || "Terjadi kesalahan.");
      resultText.style.color = "white";
    }
  } catch (err) {
    console.error("Recognition error:", err);
    resultText.textContent = "🚫 Error: " + err.message;
    resultText.style.color = "white";
  }
};
