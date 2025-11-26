<template>
  <div class="fixed inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-sky-50 overflow-hidden" style="z-index: 0;">
    <!-- Elementos decorativos para mejorar el efecto de vidrio -->
    <div class="absolute inset-0">
      <div class="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow"></div>
      <div class="absolute top-3/4 right-1/4 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 2s;"></div>
      <div class="absolute bottom-1/4 left-1/3 w-72 h-72 bg-sky-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse-slow" style="animation-delay: 4s;"></div>
    </div>

    <div class="absolute inset-0 overflow-y-auto pt-16 sm:pt-20 pb-3" style="z-index: 1;">
      <div class="page-container w-full max-w-sm mx-auto relative z-10 p-3 sm:p-4 lg:p-5">
        <!-- Header del historial -->
        <div class="glass-card mb-4">
          <div class="text-center mb-3">
            <div class="w-16 h-16 bg-blue-800 rounded-full flex items-center justify-center mx-auto mb-3 glass-avatar">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h1 class="text-xl font-bold text-gray-800 modern-title">Historiales</h1>
            <div class="blue-line mx-auto mb-3"></div>
            <p class="text-sm text-gray-600">Consulta el historial de tus solicitudes y actividades</p>
          </div>
        </div>

        <!-- Contenido principal -->
        <div class="glass-card">
          <div class="flex items-center mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 class="text-base font-semibold text-gray-800 modern-title">Registros</h2>
          </div>
          <div class="blue-line mb-4"></div>
          
          <div class="text-center py-8">
            <div class="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
            <p class="text-gray-500 text-sm">Próximamente podrás ver aquí tu historial completo</p>
          </div>
        </div>

        <!-- Botón para volver al inicio -->
        <div class="glass-card mt-4">
          <button
            @click="$router.push('/')"
            class="glass-button w-full flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Volver al Inicio
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Componente simple de Historial
// Puedes agregar lógica aquí más adelante
</script>

<style scoped>
/* Efecto de vidrio realista - Glassmorphism */
.glass-card {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 
    0 6px 25px 0 rgba(31, 38, 135, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  padding: 1rem;
  position: relative;
  overflow: hidden;
}

.glass-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -50%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: skewX(-25deg);
  transition: all 0.6s;
}

.glass-card:hover::before {
  left: 150%;
}

.glass-button {
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  border: 1px solid rgba(30, 58, 138, 0.3);
  background: linear-gradient(135deg, 
    rgba(30, 64, 175, 0.8) 0%, 
    rgba(30, 58, 138, 0.8) 100%);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 3px 15px 0 rgba(30, 64, 175, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.glass-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 30px 0 rgba(30, 64, 175, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.2),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, 
    rgba(30, 64, 175, 0.9) 0%, 
    rgba(30, 58, 138, 0.9) 100%);
}

.glass-button:active:not(:disabled) {
  transform: translateY(0px);
  box-shadow: 
    0 4px 15px 0 rgba(59, 130, 246, 0.3),
    inset 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.glass-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s;
}

.glass-button:hover::before {
  left: 100%;
}

.glass-avatar {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 8px 32px 0 rgba(59, 130, 246, 0.3),
    inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
}

.modern-title {
  background: linear-gradient(
    90deg, 
    #1e3a8a 0%, 
    #1e40af 25%, 
    #3b82f6 50%, 
    #1e40af 75%, 
    #1e3a8a 100%
  );
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: gradient-wave 3s ease-in-out infinite;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
  letter-spacing: -0.015em;
  font-weight: 500;
  position: relative;
}

.blue-line {
  width: 50px;
  height: 2px;
  background: linear-gradient(90deg, #1e3a8a, #1e40af, #1e3a8a);
  border-radius: 1px;
  animation: line-glow 2s ease-in-out infinite alternate;
}

@keyframes gradient-wave {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes line-glow {
  0% {
    box-shadow: 0 0 5px rgba(30, 64, 175, 0.3);
    opacity: 0.8;
  }
  100% {
    box-shadow: 0 0 15px rgba(30, 64, 175, 0.6);
    opacity: 1;
  }
}

/* Animación para elementos decorativos */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.05);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 4s ease-in-out infinite;
}

/* Respaldo para navegadores que no soportan background-clip: text */
@supports not (-webkit-background-clip: text) {
  .modern-title {
    color: #1e3a8a;
    animation: none;
  }
}

/* Mejoras de responsividad para pantallas móviles */
@media (max-width: 480px) {
  .page-container {
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
  }
  
  .glass-card {
    padding: 0.875rem;
    margin-bottom: 0.5rem;
    border-radius: 14px;
  }
  
  .text-xl {
    font-size: 1.125rem;
  }
  
  .text-base {
    font-size: 0.875rem;
  }
  
  .text-sm {
    font-size: 0.8rem;
  }
  
  .w-16, .h-16 {
    width: 3.5rem;
    height: 3.5rem;
  }
  
  .h-8, .w-8 {
    height: 1.75rem;
    width: 1.75rem;
  }
}

@media (max-width: 375px) {
  .page-container {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    max-width: calc(100vw - 1rem);
  }
  
  .glass-card {
    padding: 0.75rem;
    margin-bottom: 0.375rem;
    border-radius: 12px;
  }
  
  .text-xl {
    font-size: 1rem;
  }
  
  .text-base {
    font-size: 0.8rem;
  }
  
  .text-sm {
    font-size: 0.75rem;
  }
  
  .w-16, .h-16 {
    width: 3rem;
    height: 3rem;
  }
  
  .h-8, .w-8 {
    height: 1.5rem;
    width: 1.5rem;
  }
}

@media (max-height: 700px) {
  .page-container {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
  }
  
  .glass-card {
    margin-bottom: 0.375rem;
    padding: 0.75rem;
  }
  
  .mb-3 {
    margin-bottom: 0.5rem;
  }
  
  .mb-4 {
    margin-bottom: 0.625rem;
  }
  
  .py-8 {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
  }
}

@media (max-height: 600px) {
  .page-container {
    max-width: 300px;
    padding: 0.375rem 0.5rem;
  }
  
  .glass-card {
    padding: 0.625rem;
    margin-bottom: 0.25rem;
  }
  
  .w-16, .h-16 {
    width: 2.5rem;
    height: 2.5rem;
  }
  
  .w-20, .h-20 {
    width: 4rem;
    height: 4rem;
  }
  
  .py-8 {
    padding-top: 1rem;
    padding-bottom: 1rem;
  }
}

/* Para pantallas grandes */
@media (min-width: 768px) {
  .page-container {
    max-width: 380px;
    padding: 1rem;
  }
  
  .glass-card {
    padding: 1.25rem;
    margin-bottom: 1rem;
  }
}

@media (min-width: 1024px) {
  .page-container {
    max-width: 420px;
    padding: 1.25rem 1rem;
  }
  
  .glass-card {
    padding: 1.5rem;
    margin-bottom: 1.25rem;
  }
}

/* Prevenir superposición de elementos */
.glass-card {
  position: relative;
  z-index: 2;
  clear: both;
}

/* Z-index hierarchy para elementos principales */
.page-container {
  position: relative;
  z-index: 2;
}

/* Contenedor de fondo con z-index bajo */
.fixed.inset-0[style*="z-index: 0"] {
  z-index: 0 !important;
}

/* Contenedor scrollable */
.absolute.inset-0[style*="z-index: 1"] {
  z-index: 1 !important;
}

/* Mejoras para el contenedor scrollable */
.absolute.inset-0.overflow-y-auto {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

/* Soporte adicional para navegadores que no soportan backdrop-filter */
@supports not (backdrop-filter: blur(20px)) {
  .glass-card {
    background: rgba(255, 255, 255, 0.85);
  }
  
  .glass-button {
    background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  }
}
</style>
