<script lang="ts">
	interface Shop {
		id: number;
		name: string;
		lat: number;
		lng: number;
	}
	import { onMount } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';

	let shops = $state([]) as Shop[];
	let map: L.Map;

	async function fetchShops() {
		const response = await fetch('http://localhost:8000/stores');
		const data = await response.json();
		console.log('shops from backend:', data);
		shops = data;
		addMarkers();
	}

	function addMarkers() {
		shops.forEach((shop) => {
			const marker = L.marker([shop.lat, shop.lng]).addTo(map);
			marker.bindPopup(`<b>${shop.name}</b>`);
		});
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
