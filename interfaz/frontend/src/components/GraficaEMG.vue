<template>
  <div class="panel">
    <div class="header">
      <span class="titulo">Señal EMG</span>
      <span class="estado" :class="{ activo }">{{ activo ? 'EN VIVO' : 'DETENIDO' }}</span>
    </div>
    <canvas ref="canvas" />
    <div class="controles">
      <button @click="iniciar" :disabled="activo">Iniciar</button>
      <button @click="detener" :disabled="!activo">Detener</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Chart from 'chart.js/auto'

const canvas = ref(null)
const activo = ref(false)
let chart = null
let ws = null

const N = 2000
const buffer = Array(N).fill(0)

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
  ws = new WebSocket('ws://localhost:8000/ws/emg')
  ws.onmessage = ({ data }) => {
    const { muestras } = JSON.parse(data)
    buffer.splice(0, muestras.length)
    buffer.push(...muestras)
    chart.data.datasets[0].data = [...buffer]
    chart.update('none')
  }
  ws.onclose = () => { activo.value = false }
  activo.value = true
}

function detener() {
  ws?.close()
  activo.value = false
}

onUnmounted(detener)
</script>
