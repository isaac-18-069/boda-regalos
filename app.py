<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>¡Estás Invitado/a a Nuestro Evento!</title>

  <!-- META TAGS PARA LA VISTA PREVIA EN WHATSAPP -->
  <meta property="og:title" content="¡Estás Invitado/a a Nuestra Celebración! 🎉">
  <meta property="og:description" content="Haz clic para ver los detalles, la ubicación y confirmar tu asistencia.">
  <meta property="og:image" content="https://images.unsplash.com/photo-1519741497674-611481863552?w=800">
  <meta property="og:url" content="https://tu-usuario.github.io/mi-invitacion/">

  <!-- Fuentes de Google -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Alex+Brush&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">

  <!-- Estilos CSS -->
  <style>
    :root {
      --primary: #d4af37; /* Color dorado principal */
      --text: #2c2c2c;
      --bg: #faf8f5;
      --card-bg: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Montserrat', sans-serif;
      background-color: var(--bg);
      color: var(--text);
      text-align: center;
      line-height: 1.6;
    }

    .container {
      max-width: 500px;
      margin: 0 auto;
      padding: 20px;
    }

    /* Portada / Hero */
    .hero {
      padding: 60px 20px 40px;
      border-radius: 20px;
      background: white;
      box-shadow: 0 10px 30px rgba(0,0,0,0.05);
      margin-bottom: 25px;
    }

    .subtitle {
      text-transform: uppercase;
      letter-spacing: 3px;
      font-size: 0.85rem;
      color: #888;
    }

    .title {
      font-family: 'Alex Brush', cursive;
      font-size: 3.5rem;
      color: var(--primary);
      margin: 15px 0;
    }

    /* Botón de Música */
    .music-btn {
      position: fixed;
      bottom: 25px;
      right: 25px;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: var(--primary);
      color: white;
      border: none;
      font-size: 1.2rem;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(0,0,0,0.2);
      z-index: 1000;
    }

    /* Contador */
    .countdown-title {
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 15px;
    }

    .countdown {
      display: flex;
      justify-content: space-between;
      margin-bottom: 30px;
    }

    .time-box {
      background: var(--card-bg);
      padding: 12px;
      border-radius: 12px;
      flex: 1;
      margin: 0 5px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .time-box span {
      display: block;
      font-size: 1.5rem;
      font-weight: 600;
      color: var(--primary);
    }

    .time-box label {
      font-size: 0.75rem;
      color: #777;
      text-transform: uppercase;
    }

    /* Secciones de Información */
    .card {
      background: var(--card-bg);
      padding: 30px 20px;
      border-radius: 16px;
      margin-bottom: 25px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    }

    .card h3 {
      font-family: 'Alex Brush', cursive;
      font-size: 2.2rem;
      color: var(--primary);
      margin-bottom: 10px;
    }

    /* Botones de Acción */
    .btn {
      display: inline-block;
      width: 100%;
      padding: 14px 20px;
      margin-top: 15px;
      border-radius: 30px;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.95rem;
      transition: transform 0.2s, opacity 0.2s;
      border: none;
      cursor: pointer;
    }

    .btn:active {
      transform: scale(0.98);
    }

    .btn-primary {
      background-color: #25D366; /* Verde WhatsApp */
      color: white;
    }

    .btn-secondary {
      background-color: var(--primary);
      color: white;
    }

    .btn-outline {
      border: 2px solid var(--primary);
      color: var(--primary);
      background: transparent;
    }

    /* Modal para Regalos / Cuenta bancaria */
    .modal {
      display: none;
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.6);
      justify-content: center;
      align-items: center;
      z-index: 2000;
    }

    .modal-content {
      background: white;
      padding: 30px;
      border-radius: 16px;
      max-width: 90%;
      width: 380px;
    }
  </style>
</head>
<body>

  <!-- Reproductor de música de fondo (opcional) -->
  <audio id="bgMusic" loop>
    <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
  </audio>
  <button class="music-btn" onclick="toggleMusic()" id="musicBtn">🎵</button>

  <div class="container">
    
    <!-- Encabezado / Portada -->
    <div class="hero">
      <p class="subtitle">¡Nos Casamos! / Mis 15 Años</p>
      <h1 class="title">María & Juan</h1>
      <p>Queremos compartir este día tan especial contigo.</p>
    </div>

    <!-- Cuenta Regresiva -->
    <div class="card">
      <p class="countdown-title">FALTAN SÓLO</p>
      <div class="countdown">
        <div class="time-box"><span id="days">00</span><label>Días</label></div>
        <div class="time-box"><span id="hours">00</span><label>Hs</label></div>
        <div class="time-box"><span id="minutes">00</span><label>Min</label></div>
        <div class="time-box"><span id="seconds">00</span><label>Seg</label></div>
      </div>
    </div>

    <!-- Fecha y Hora -->
    <div class="card">
      <h3>¿Cuándo & Dónde?</h3>
      <p><strong>Fecha:</strong> Sábado, 15 de Noviembre de 2026</p>
      <p><strong>Hora:</strong> 18:00 Hs</p>
      <p style="margin-top: 10px;"><strong>Lugar:</strong> Salón de Eventos "El Paraíso"</p>
      <p>Av. Principal #123, Ciudad</p>

      <a href="https://maps.google.com/?q=-0.180653,-78.467838" target="_blank" class="btn btn-secondary">
        📍 Ver Ubicación en Google Maps
      </a>
      
      <a href="https://calendar.google.com/calendar/render?action=TEMPLATE&text=Boda+Maria+y+Juan&dates=20261115T180000Z/20261116T020000Z&details=Invitacion+especial" target="_blank" class="btn btn-outline">
        📅 Agendar en Google Calendar
      </a>
    </div>

    <!-- Dress Code / Vestimenta -->
    <div class="card">
      <h3>Código de Vestimenta</h3>
      <p><strong>Formal / Elegante</strong></p>
      <p style="font-size: 0.85rem; color: #666; margin-top: 5px;">Nos reservamos el color blanco para la novia.</p>
    </div>

    <!-- Mesa de Regalos / Cuenta bancaria -->
    <div class="card">
      <h3>Mesa de Regalos</h3>
      <p>Tu presencia es nuestro mejor regalo, pero si deseas realizar un detalle:</p>
      <button class="btn btn-outline" onclick="openModal()">🎁 Datos Bancarios / Regalo</button>
    </div>

    <!-- Confirmación por WhatsApp -->
    <div class="card">
      <h3>Confirmación de Asistencia</h3>
      <p>Por favor, confírmanos tu asistencia antes del 1 de Noviembre.</p>
      <button onclick="sendRSVP()" class="btn btn-primary">
        💬 Confirmar Asistencia por WhatsApp
      </button>
    </div>

  </div>

  <!-- Modal Datos Bancarios -->
  <div class="modal" id="bankModal">
    <div class="modal-content">
      <h3>Datos Bancarios</h3>
      <p style="margin-top: 10px;"><strong>Banco:</strong> Banco Pichincha / Guayaquil</p>
      <p><strong>Tipo de Cuenta:</strong> Ahorros</p>
      <p><strong>Número:</strong> 1234567890</p>
      <p><strong>Titular:</strong> Juan Pérez</p>
      <p><strong>C.I.:</strong> 1712345678</p>
      <button class="btn btn-secondary" onclick="closeModal()" style="margin-top: 20px;">Cerrar</button>
    </div>
  </div>

  <!-- JavaScript -->
  <script>
    // 1. Configuración de Fecha del Evento
    const eventDate = new Date("Nov 15, 2026 18:00:00").getTime();

    // Cuenta Regresiva
    const timer = setInterval(() => {
      const now = new Date().getTime();
      const distance = eventDate - now;

      if (distance < 0) {
        clearInterval(timer);
        document.querySelector(".countdown").innerHTML = "<b>¡Hoy es el gran día!</b>";
        return;
      }

      document.getElementById("days").innerText = Math.floor(distance / (1000 * 60 * 60 * 24));
      document.getElementById("hours").innerText = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      document.getElementById("minutes").innerText = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      document.getElementById("seconds").innerText = Math.floor((distance % (1000 * 60)) / 1000);
    }, 1000);

    // 2. Reproductor de Música
    const music = document.getElementById("bgMusic");
    let isPlaying = false;

    function toggleMusic() {
      if (isPlaying) {
        music.pause();
        document.getElementById("musicBtn").innerText = "🎵";
      } else {
        music.play();
        document.getElementById("musicBtn").innerText = "⏸️";
      }
      isPlaying = !isPlaying;
    }

    // 3. Confirmación por WhatsApp (Cambia el número de teléfono con tu código de país)
    function sendRSVP() {
      const phone = "593999999999"; // Ejemplo: Ecuador (+593), México (+52), Colombia (+57)
      const text = encodeURIComponent("¡Hola! Confirmo mi asistencia para el evento. ¡Muchas gracias por la invitación! 🎉");
      window.open(`https://wa.me/${phone}?text=${text}`, '_blank');
    }

    // 4. Abrir y Cerrar Modal
    function openModal() { document.getElementById("bankModal").style.display = "flex"; }
    function closeModal() { document.getElementById("bankModal").style.display = "none"; }
  </script>
</body>
</html>
