// chatbot.js
(function(){
  // Elementos
  const toggle = document.getElementById('chat-toggle');
  const panel = document.getElementById('chat-panel');
  const closeBtn = document.getElementById('chat-close');
  const messages = document.getElementById('chat-messages');
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send');

  let greeted = false;

  // Escape para mensajes de usuario (evitar XSS)
  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, function(m){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m];});
  }

  function appendMessage(role, content, isHtml=false){
    const el = document.createElement('div');
    el.className = 'msg ' + (role === 'user' ? 'user' : 'bot');
    if(isHtml) {
      // content viene confiable del backend (ej. lista) — usar con precaución
      el.innerHTML = content;
    } else {
      el.textContent = content;
    }
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;
  }

  function openPanel(){
    panel.hidden = false;
    // Si no saludó antes, poner saludo del asistente localmente
    if(!greeted){
    fetch(`/chat/ask/?message=__init__`)
      .then(r => r.json())
      .then(data => {
          appendMessage('bot', data.respuesta, true);
          greeted = true;
      })
      .catch(err => console.error(err));
}

  }

  function closePanel(){
    panel.hidden = true;
  }

  function sendMessage(){
    const text = input.value.trim();
    if(!text) return;
    appendMessage('user', text, false);
    input.value = '';
    // mostrar loader del bot
    const loaderId = 'loader-' + Date.now();
    appendMessage('bot', 'Escribiendo...', false);
    messages.lastChild.id = loaderId;

    // Llamada al backend (usa GET porque tu endpoint actual acepta GET)
    fetch(`/chat/ask/?message=${encodeURIComponent(text)}`)
      .then(r => {
        if(!r.ok) throw new Error('Error en la comunicación');
        return r.json();
      })
      .then(data => {
        // El backend ya limpia asteriscos y puede devolver HTML (listas)
        // Reemplazamos el loader con la respuesta
        const loaderEl = document.getElementById(loaderId);
        if(loaderEl){
          // Mantener formato: si la respuesta contiene etiquetas HTML, mostramos como HTML
          loaderEl.remove(); // borra el loader
        }
        // Añadir respuesta (si contiene etiquetas <ul> o similares, se renderiza)
        // Si querés evitar HTML no seguro, cambiar el tercer param a false y escapeHtml(data.respuesta)
        appendMessage('bot', data.respuesta, true);
      })
      .catch(err => {
        const loaderEl = document.getElementById(loaderId);
        if(loaderEl) loaderEl.remove();
        appendMessage('bot', 'Lo siento, hubo un error al consultar el servidor.', false);
        console.error(err);
      });
  }

  // Eventos
  toggle.addEventListener('click', () => {
    if(panel.hidden) openPanel();
    else closePanel();
  });
  closeBtn.addEventListener('click', closePanel);

  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keypress', (e)=>{
    if(e.key === 'Enter') sendMessage();
  });

  // Si querés que el panel abra automáticamente en cierta ruta:
  // if(window.location.pathname === '/checkout/') openPanel();

})();
