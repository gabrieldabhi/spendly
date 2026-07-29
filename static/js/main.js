// main.js — students will add JavaScript here as features are built

// Video Modal Functions
const videoUrl = 'https://www.youtube.com/embed/dQw4w9WgXcQ'; // Placeholder URL
let videoFrame = null;

function openModal() {
  const modal = document.getElementById('videoModal');
  modal.classList.add('active');

  videoFrame = document.getElementById('videoFrame');
  videoFrame.src = videoUrl + '?autoplay=1';

  document.body.style.overflow = 'hidden';
}

function closeModal(event) {
  const modal = document.getElementById('videoModal');

  // Stop video playback
  if (videoFrame) {
    videoFrame.src = '';
  }

  modal.classList.remove('active');
  document.body.style.overflow = '';
}

// Close modal on Escape key
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    closeModal();
  }
});
