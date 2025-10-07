<script setup>
import { computed, ref, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import ConnectivityStatus from './components/ConnectivityStatus.vue';
import UpdateNotification from './components/UpdateNotification.vue';
import SupportBubble from './components/SupportBubble.vue';
import { useNotifications } from './composables/useNotifications.js';

const router = useRouter();
const route = useRoute();
const isLoggingOut = ref(false);
const showWelcome = ref(false);
const userData = ref(null);
const showMobileMenu = ref(false);

// Sistema de notificaciones en tiempo real
const { unreadCount, startPolling, stopPolling } = useNotifications();
let notificationPollingId = null;

// Watcher para detectar cambios de ruta y actualizar el estado
watch(() => route.path, () => {
  // Verificar estado de autenticación en cada cambio de ruta
  const storedUser = localStorage.getItem('user');
  if (storedUser && !userData.value) {
    try {
      userData.value = JSON.parse(storedUser);
    } catch (error) {
      console.error('Error parsing user data:', error);
      localStorage.clear();
      sessionStorage.clear();
    }
  } else if (!storedUser && userData.value) {
    userData.value = null;
  }
});

// Listener para cambios en localStorage (útil para logout desde otras pestañas)
const handleStorageChange = (e) => {
  if (e.key === 'user') {
    if (e.newValue === null) {
      // Si se eliminó el usuario del localStorage, limpiar estado y redirigir
      userData.value = null;
      showWelcome.value = false;
      showMobileMenu.value = false;
      
      // Detener polling de notificaciones
      if (notificationPollingId) {
        stopPolling(notificationPollingId);
        notificationPollingId = null;
      }
      
      router.push('/login');
    } else if (e.newValue && !userData.value) {
      // Si se agregó un usuario y no tenemos datos, cargarlos
      try {
        userData.value = JSON.parse(e.newValue);
        
        // Reiniciar polling de notificaciones para el nuevo usuario
        if (notificationPollingId) {
          stopPolling(notificationPollingId);
        }
        notificationPollingId = startPolling();
        
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('user');
      }
    }
  }
};

onMounted(() => {
  // Verificar el estado de autenticación al cargar la app
  const storedUser = localStorage.getItem('user');
  
  if (storedUser) {
    try {
      userData.value = JSON.parse(storedUser);
      
      // Inicializar sistema de notificaciones una vez que el usuario está identificado
      notificationPollingId = startPolling();
      
      // Mostrar mensaje de bienvenida solo si recién inició sesión
      const justLoggedIn = sessionStorage.getItem('justLoggedIn');
      if (justLoggedIn) {
        showWelcome.value = true;
        sessionStorage.removeItem('justLoggedIn');
        
        // Ocultar el mensaje después de 3 segundos
        setTimeout(() => {
          showWelcome.value = false;
        }, 3000);
      }
    } catch (error) {
      console.error('Error parsing user data:', error);
      // Si hay error al parsear, limpiar y redirigir
      localStorage.clear();
      sessionStorage.clear();
      router.push('/login');
    }
  } else {
    // Si no hay usuario logueado, asegurar que esté en login
    if (route.name !== 'Login' && route.name !== 'Register') {
      router.push('/login');
    }
  }
  
  // Escuchar cambios en localStorage
  window.addEventListener('storage', handleStorageChange);
});

onUnmounted(() => {
  // Limpiar listener
  window.removeEventListener('storage', handleStorageChange);
  // Detener el polling de notificaciones
  stopPolling(notificationPollingId);
});

const isLoggedIn = computed(() => {
  // Verificar tanto el ref como el localStorage para mayor seguridad
  return userData.value !== null && localStorage.getItem('user') !== null;
});

const userName = computed(() => {
  if (userData.value) {
    // Verificar ambos campos para compatibilidad con datos antiguos y nuevos
    return userData.value.nombre || userData.value.nombre_completo || '';
  }
  return '';
});

// Función para obtener las primeras dos letras del nombre
const getUserInitials = computed(() => {
  if (userData.value) {
    const nombreCompleto = userData.value.nombre || userData.value.nombre_completo || '';
    if (nombreCompleto) {
      const names = nombreCompleto.split(' ');
      return names.length >= 2 ? 
        (names[0][0] + names[1][0]).toUpperCase() : 
        names[0].substring(0, 2).toUpperCase();
    }
  }
  return 'US';
});

// Función para cerrar el menú móvil cuando se navega
const closeMobileMenu = () => {
  showMobileMenu.value = false;
};

function logout() {
  isLoggingOut.value = true;
  showMobileMenu.value = false;
  
  // Detener el polling de notificaciones
  stopPolling(notificationPollingId);
  notificationPollingId = null;
  
  // Limpiar el estado reactivo primero
  userData.value = null;
  showWelcome.value = false;
  
  // Guardar el estado de asistencia del localStorage antes de limpiarlo
  const today = new Date().toISOString().split('T')[0];
  const storedUser = localStorage.getItem('user');
  let userId = null;
  
  if (storedUser) {
    try {
      const user = JSON.parse(storedUser);
      userId = user.id;
    } catch (error) {
      console.error('Error parsing user data:', error);
    }
  }
  
  // Si tenemos el ID del usuario, guardar su estado de asistencia y la última fecha
  let asistenciaHoy = null;
  let ultimaFecha = null;
  
  if (userId) {
    asistenciaHoy = localStorage.getItem(`asistencia_${userId}_${today}`);
    ultimaFecha = localStorage.getItem(`asistencia_ultima_fecha_${userId}`);
  }
  
  // Limpiar localStorage y sessionStorage (excepto datos de asistencia)
  localStorage.clear();
  sessionStorage.clear();
  
  // Restaurar el estado de asistencia del día en localStorage si existe
  if (userId && asistenciaHoy) {
    localStorage.setItem(`asistencia_${userId}_${today}`, asistenciaHoy);
  }
  
  // Restaurar la última fecha consultada
  if (userId && ultimaFecha) {
    localStorage.setItem(`asistencia_ultima_fecha_${userId}`, ultimaFecha);
  }
  
  // Pequeño delay para que se vea la limpieza del estado
  setTimeout(() => {
    // Recargar la página completamente para limpiar todo el estado
    window.location.href = '/login';
  }, 100);
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-sky-50">
    <!-- Mensaje de bienvenida -->
    <transition name="slide-down">
      <div v-if="showWelcome" class="fixed top-0 inset-x-0 z-50 bg-blue-700 text-white p-3 shadow-lg">
        <div class="max-w-sm mx-auto flex items-center justify-between">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span class="font-medium text-sm">¡Bienvenido, {{ userName }}!</span>
          </div>
          <button @click="showWelcome = false" class="text-white hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </transition>

    <!-- Indicador de estado de conexión -->
    <ConnectivityStatus :show="route.name === 'Home' && !showMobileMenu" />

    <!-- Header móvil con menú hamburguesa -->
    <header v-if="isLoggedIn" class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
      <div class="max-w-sm mx-auto px-4 py-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <!-- Dron futurista con diseño elegante y animación suave -->
            <div class="relative w-8 h-8 flex items-center justify-center mr-3">
              <div class="drone-floating">
                <svg viewBox="0 0 100 100" class="w-8 h-8">
                  <!-- Definiciones avanzadas -->
                  <defs>
                    <linearGradient id="futuristicBody" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#0ea5e9"/>
                      <stop offset="30%" style="stop-color:#0284c7"/>
                      <stop offset="70%" style="stop-color:#0369a1"/>
                      <stop offset="100%" style="stop-color:#075985"/>
                    </linearGradient>
                    <linearGradient id="futuristicAccent" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#06b6d4"/>
                      <stop offset="50%" style="stop-color:#0891b2"/>
                      <stop offset="100%" style="stop-color:#0e7490"/>
                    </linearGradient>
                    <radialGradient id="propellerGlow" cx="50%" cy="50%" r="50%">
                      <stop offset="0%" style="stop-color:#60a5fa" stop-opacity="0.8"/>
                      <stop offset="70%" style="stop-color:#3b82f6" stop-opacity="0.4"/>
                      <stop offset="100%" style="stop-color:#1d4ed8" stop-opacity="0"/>
                    </radialGradient>
                    <filter id="glow">
                      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                      <feMerge> 
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                      </feMerge>
                    </filter>
                  </defs>
                  
                  <!-- Aura energética que pulsa -->
                  <circle cx="50" cy="50" r="40" fill="url(#propellerGlow)" opacity="0.2" class="energy-pulse"/>
                  
                  <!-- Cuerpo principal futurista -->
                  <g class="drone-main-body">
                    <!-- Casco principal hexagonal -->
                    <polygon points="35,45 50,35 65,45 65,55 50,65 35,55" 
                             fill="url(#futuristicBody)" 
                             stroke="#0369a1" 
                             stroke-width="0.8"
                             filter="url(#glow)"/>
                    
                    <!-- Panel superior con líneas tech -->
                    <polygon points="38,47 50,39 62,47 62,53 50,61 38,53" 
                             fill="url(#futuristicAccent)" 
                             opacity="0.9"/>
                    
                    <!-- Líneas de diseño tech -->
                    <line x1="42" y1="50" x2="58" y2="50" stroke="#60a5fa" stroke-width="1" opacity="0.8"/>
                    <line x1="46" y1="46" x2="54" y2="46" stroke="#60a5fa" stroke-width="0.5" opacity="0.6"/>
                    <line x1="46" y1="54" x2="54" y2="54" stroke="#60a5fa" stroke-width="0.5" opacity="0.6"/>
                    
                    <!-- Núcleo central con pulso -->
                    <circle cx="50" cy="50" r="4" fill="#1e40af" stroke="#3b82f6" stroke-width="1"/>
                    <circle cx="50" cy="50" r="2.5" fill="#60a5fa" opacity="0.8" class="core-pulse"/>
                    <circle cx="50" cy="50" r="1" fill="#ffffff" opacity="0.9"/>
                  </g>
                  
                  <!-- Brazos extendidos con estilo futurista -->
                  <g class="drone-arms">
                    <!-- Brazo superior izquierdo -->
                    <path d="M 42 42 L 28 28 L 25 31 L 39 45" fill="url(#futuristicAccent)" opacity="0.9"/>
                    <!-- Brazo superior derecho -->
                    <path d="M 58 42 L 72 28 L 75 31 L 61 45" fill="url(#futuristicAccent)" opacity="0.9"/>
                    <!-- Brazo inferior izquierdo -->
                    <path d="M 42 58 L 28 72 L 25 69 L 39 55" fill="url(#futuristicAccent)" opacity="0.9"/>
                    <!-- Brazo inferior derecho -->
                    <path d="M 58 58 L 72 72 L 75 69 L 61 55" fill="url(#futuristicAccent)" opacity="0.9"/>
                  </g>
                  
                  <!-- Motores en las puntas -->
                  <g class="drone-motors">
                    <circle cx="26" cy="26" r="5" fill="url(#futuristicBody)" stroke="#0369a1" stroke-width="0.5"/>
                    <circle cx="74" cy="26" r="5" fill="url(#futuristicBody)" stroke="#0369a1" stroke-width="0.5"/>
                    <circle cx="26" cy="74" r="5" fill="url(#futuristicBody)" stroke="#0369a1" stroke-width="0.5"/>
                    <circle cx="74" cy="74" r="5" fill="url(#futuristicBody)" stroke="#0369a1" stroke-width="0.5"/>
                    
                    <!-- Centros de motores -->
                    <circle cx="26" cy="26" r="2" fill="#1e40af"/>
                    <circle cx="74" cy="26" r="2" fill="#1e40af"/>
                    <circle cx="26" cy="74" r="2" fill="#1e40af"/>
                    <circle cx="74" cy="74" r="2" fill="#1e40af"/>
                  </g>
                  
                  <!-- Hélices con efecto de velocidad -->
                  <g class="propeller-blur">
                    <!-- Hélice superior izquierda -->
                    <g opacity="0.7">
                      <ellipse cx="26" cy="26" rx="9" ry="1.5" fill="#60a5fa" opacity="0.6"/>
                      <ellipse cx="26" cy="26" rx="1.5" ry="9" fill="#60a5fa" opacity="0.4"/>
                      <circle cx="26" cy="26" r="8" fill="none" stroke="#3b82f6" stroke-width="0.5" opacity="0.3"/>
                    </g>
                    
                    <!-- Hélice superior derecha -->
                    <g opacity="0.7">
                      <ellipse cx="74" cy="26" rx="9" ry="1.5" fill="#60a5fa" opacity="0.6"/>
                      <ellipse cx="74" cy="26" rx="1.5" ry="9" fill="#60a5fa" opacity="0.4"/>
                      <circle cx="74" cy="26" r="8" fill="none" stroke="#3b82f6" stroke-width="0.5" opacity="0.3"/>
                    </g>
                    
                    <!-- Hélice inferior izquierda -->
                    <g opacity="0.7">
                      <ellipse cx="26" cy="74" rx="9" ry="1.5" fill="#60a5fa" opacity="0.6"/>
                      <ellipse cx="26" cy="74" rx="1.5" ry="9" fill="#60a5fa" opacity="0.4"/>
                      <circle cx="26" cy="74" r="8" fill="none" stroke="#3b82f6" stroke-width="0.5" opacity="0.3"/>
                    </g>
                    
                    <!-- Hélice inferior derecha -->
                    <g opacity="0.7">
                      <ellipse cx="74" cy="74" rx="9" ry="1.5" fill="#60a5fa" opacity="0.6"/>
                      <ellipse cx="74" cy="74" rx="1.5" ry="9" fill="#60a5fa" opacity="0.4"/>
                      <circle cx="74" cy="74" r="8" fill="none" stroke="#3b82f6" stroke-width="0.5" opacity="0.3"/>
                    </g>
                  </g>
                  
                  <!-- LEDs de estado -->
                  <g class="status-leds">
                    <circle cx="26" cy="26" r="1" fill="#10b981" class="led-pulse" style="animation-delay: 0s;"/>
                    <circle cx="74" cy="26" r="1" fill="#ef4444" class="led-pulse" style="animation-delay: 0.5s;"/>
                    <circle cx="26" cy="74" r="1" fill="#f59e0b" class="led-pulse" style="animation-delay: 1s;"/>
                    <circle cx="74" cy="74" r="1" fill="#8b5cf6" class="led-pulse" style="animation-delay: 1.5s;"/>
                  </g>
                  
                  <!-- Antena de comunicación -->
                  <g class="communication">
                    <line x1="50" y1="35" x2="50" y2="28" stroke="#60a5fa" stroke-width="1"/>
                    <circle cx="50" cy="28" r="1.5" fill="#ef4444" class="antenna-blink"/>
                  </g>
                </svg>
              </div>
            </div>
            <div>
              <h1 class="text-base font-bold text-blue-800 mb-0">Seguimiento de Drones</h1>
              <p class="text-xs text-gray-500 -mt-0.5">{{ userName }}</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <!-- Botón de notificaciones -->
            <router-link 
              to="/notificaciones"
              class="relative p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-blue-50 text-blue-600': route.name === 'Notificaciones' }"
            >
              <!-- Icono de campanita -->
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
              <!-- Badge de notificaciones no leídas -->
              <span v-if="unreadCount > 0" class="absolute -top-1 -right-1 h-5 w-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                {{ unreadCount > 9 ? '9+' : unreadCount }}
              </span>
            </router-link>
            
            <!-- Botón del menú hamburguesa -->
          <button 
            @click="showMobileMenu = !showMobileMenu"
            class="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Menú desplegable móvil -->
    <transition name="slide-down">
      <div 
        v-if="isLoggedIn && showMobileMenu" 
        class="fixed top-16 inset-x-0 z-30 bg-white border-b border-gray-200 shadow-lg"
      >
        <div class="max-w-sm mx-auto px-4 py-2">
          <nav class="space-y-1">
            <router-link 
              to="/" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-blue/10 text-blue-600': route.name === 'Home' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span class="font-medium">Inicio</span>
            </router-link>
            
            <router-link 
              to="/historial" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-blue/10 text-blue-600': route.name === 'Historial' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
              <span class="font-medium">Historial</span>
            </router-link>
            
            <router-link 
              to="/notificaciones" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors relative"
              :class="{ 'bg-blue/10 text-blue-600': route.name === 'Notificaciones' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 2a6 6 0 00-6 6v3.586l-.707.707A1 1 0 004 14h12a1 1 0 00.707-1.707L16 11.586V8a6 6 0 00-6-6zM10 18a3 3 0 01-3-3h6a3 3 0 01-3 3z" />
              </svg>
              <span class="font-medium">Notificaciones</span>
              <!-- Badge de notificaciones no leídas en el menú -->
              <span v-if="unreadCount > 0" class="ml-auto h-5 w-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                {{ unreadCount > 9 ? '9+' : unreadCount }}
              </span>
            </router-link>
            
            <router-link 
              to="/profile" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-blue/10 text-blue-600': route.name === 'Profile' }"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span class="font-medium">Mi Perfil</span>
            </router-link>
            
            <router-link 
              to="/support" 
              @click="closeMobileMenu"
              class="flex items-center px-3 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-colors"
              :class="{ 'bg-blue/10 text-blue-600': route.name === 'Support' }"
            >
              <font-awesome-icon 
                icon="headset"
                class="h-5 w-5 mr-3"
              />
              <span class="font-medium">Soporte</span>
            </router-link>
            
            <div class="border-t border-gray-200 pt-2 mt-2">
              <button 
                @click="logout" 
                class="flex items-center w-full px-3 py-3 rounded-lg text-red-600 hover:bg-red-50 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                <span class="font-medium">Cerrar Sesión</span>
              </button>
            </div>
          </nav>
        </div>
      </div>
    </transition>

    <!-- Overlay para cerrar el menú -->
    <div 
      v-if="isLoggedIn && showMobileMenu"
      @click="closeMobileMenu"
      class="fixed inset-0 bg-black bg-opacity-25 z-20"
    ></div>

    <!-- Contenido principal -->
    <main class="main-content" :style="{ paddingTop: isLoggedIn ? '48px' : '0' }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Modal de actualización de la aplicación (obligatorio) -->
    <UpdateNotification />

    <!-- Burbuja de soporte (solo visible cuando el usuario está logueado y no está en la vista de soporte) -->
    <SupportBubble v-if="isLoggedIn" :hideOnSupportPage="route.name === 'Support'" />
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Animación para el mensaje de bienvenida */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}

/* Efecto vidrio líquido para el título */
h1 {
  position: relative;
  overflow: hidden;
  color: #1e3a8a;
}

h1::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.4) 50%,
    transparent 70%
  );
  transform: rotate(45deg);
  animation: liquidGlass 3s infinite;
  pointer-events: none;
}

@keyframes liquidGlass {
  0% {
    transform: translateX(-100%) translateY(-100%) rotate(45deg);
  }
  50% {
    transform: translateX(0%) translateY(0%) rotate(45deg);
  }
  100% {
    transform: translateX(100%) translateY(100%) rotate(45deg);
  }
}

/* Animaciones del dron futurista - Sin flotación */
.drone-floating {
  /* Sin animación de flotación, mantiene posición fija */
  transform-origin: center;
}

.drone-main-body {
  animation: bodyStabilize 3s ease-in-out infinite;
  transform-origin: 50px 50px;
}

.drone-arms {
  /* Sin animación de flexión para mantener estático */
  transform-origin: 50px 50px;
}

.propeller-blur {
  animation: ultraFastSpin 0.15s linear infinite;
  transform-origin: 50px 50px;
}

.energy-pulse {
  animation: energyWave 3s ease-in-out infinite;
  transform-origin: center;
}

.core-pulse {
  animation: coreGlow 2s ease-in-out infinite;
}

.led-pulse {
  animation: ledBlink 2s ease-in-out infinite;
}

.antenna-blink {
  animation: antennaFlash 1.5s ease-in-out infinite;
}

/* Estabilización del cuerpo - Solo rotaciones sutiles sin movimiento vertical */
@keyframes bodyStabilize {
  0%, 100% {
    transform: rotate(0deg);
  }
  33% {
    transform: rotate(0.3deg);
  }
  66% {
    transform: rotate(-0.3deg);
  }
}

/* Rotación ultra rápida de hélices */
@keyframes ultraFastSpin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Onda de energía - Solo pulso de opacidad sin escalado */
@keyframes energyWave {
  0%, 100% {
    opacity: 0.2;
  }
  50% {
    opacity: 0.4;
  }
}

/* Resplandor del núcleo */
@keyframes coreGlow {
  0%, 100% {
    opacity: 0.8;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.3);
  }
}

/* Parpadeo de LEDs */
@keyframes ledBlink {
  0%, 80%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  90% {
    opacity: 1;
    transform: scale(1.5);
  }
}

/* Flash de antena */
@keyframes antennaFlash {
  0%, 90%, 100% {
    opacity: 0.7;
  }
  95% {
    opacity: 1;
    transform: scale(1.2);
  }
}
</style>
