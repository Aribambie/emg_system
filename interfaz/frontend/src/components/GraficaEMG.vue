<template>
  <div class="panel">
    <div class="header">
      <span class="titulo">Señal EMG</span>
      <div class="badges">
        <span class="badge" :class="badgeSensor.clase">
          <span class="dot" />{{ badgeSensor.texto }}
        </span>
        <span class="badge" :class="{ 'badge--vivo': activo, 'badge--detenido': !activo }">
          <span class="dot" />{{ activo ? 'EN VIVO' : 'DETENIDO' }}
        </span>
      </div>
    </div>
    <canvas ref="canvas" />
    <div class="controles">
      <button @click="iniciar" :disabled="activo">Iniciar</button>
      <button @click="detener" :disabled="!activo">Detener</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import Chart from 'chart.js/auto'

const canvas = ref(null)
const activo = ref(false)
// null = sin intentar, true = conectado, false = error
const sensorOk = ref(null)
let chart = null
let ws = null

const N = 2000
const buffer = Array(N).fill(0)

const badgeSensor = computed(() => {
  if (sensorOk.value === null)         return { texto: '···',        clase: 'badge--cargando'   }
  if (sensorOk.value === 'conectando') return { texto: 'CONECTANDO', clase: 'badge--conectando' }
  if (sensorOk.value === true)         return { texto: 'BITALINO',   clase: 'badge--sensor'     }
  return                                      { texto: 'SIN SENSOR', clase: 'badge--error'      }
})

onMounted(() => {
  chart = new Chart(canvas.value, {
    type: 'line',
    data: {
      labels: Array(N).fill(''),
      datasets: [{
        data: [...buffer],
        borderColor: '#00e5ff',
        borderWidth: 1.2,
        pointRadius: 0,
        tension: 0,
      }],
    },
    options: {
      animation: false,
      responsive: true,
      scales: {
        x: { display: false },
        y: {
          min: -0.4,
          max: 0.4,
          ticks: { color: '#888', stepSize: 0.1 },
          grid: { color: '#222' },
        },
      },
      plugins: { legend: { display: false } },
    },
  })
})

function iniciar() {
  sensorOk.value = null
  ws = new WebSocket('ws://localhost:8000/ws/emg')

  ws.onmessage = ({ data }) => {
    const msg = JSON.parse(data)

    if (msg.estado === 'conectando') {
      sensorOk.value = 'conectando'
      return
    }
    if (msg.conectado) {
      sensorOk.value = true
      return
    }
    if (msg.error) {
      sensorOk.value = false
      activo.value = false
      return
    }
    if (msg.muestras) {
      buffer.splice(0, msg.muestras.length)
      buffer.push(...msg.muestras)
      chart.data.datasets[0].data = [...buffer]
      chart.update('none')
    }
  }

  ws.onerror = () => { sensorOk.value = false }
  ws.onclose = () => { activo.value = false }
  activo.value = true
}

function detener() {
  ws?.close()
  activo.value = false
}

onUnmounted(detener)
</script>
