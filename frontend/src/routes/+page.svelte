<script lang="ts">
  import { onMount } from 'svelte';
  import L from 'leaflet';
  import 'leaflet/dist/leaflet.css';

  let shops = $state([]);
  let map: L.Map;

  async function fetchShops() {
    const response = await fetch('http://localhost:8000/stores');
    const data = await response.json();
    console.log('shops from backend:', data);
    shops = data;
  }

  onMount(async () => {
    // init map
    map = L.map('map').setView([50.061, 19.937], 13); // Kraków

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // fetch shops after map is ready
    await fetchShops();
  });
</script>

<div id="map"></div>

<style>
  #map {
    height: 100vh;
    width: 100%;
  }
</style>