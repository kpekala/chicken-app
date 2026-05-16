<script lang="ts">
	import 'leaflet/dist/leaflet.css';
	import { onMount } from 'svelte';
	import L from 'leaflet';

	onMount(() => {
		const map = L.map('map').setView([50.049683, 19.944544], 13);

		L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '© OpenStreetMap contributors'
		}).addTo(map);
	});
</script>

<div id="map"></div>

<style>
	#map {
		height: 100vh;
	}
</style>
