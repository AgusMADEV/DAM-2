function reproducirCancion(index) {
  const audioPlayer = document.getElementById('audioPlayer');
  const canciones = [
    '0802.mp3',
    'cancion2.mp3',
    'cancion3.mp3'
  ];
  audioPlayer.src = canciones[index];
}
