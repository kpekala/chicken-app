<script lang="ts">
	interface Shop {
		id: number;
		name: string;
		lat: number;
		lng: number;
	}
	interface Polygon {
		id: number;
		name: string;
		type: 'protected_area' | 'nature_reserve' | 'forest';
		outer: number[][][];
		inner: number[][][];
	}

	import { onMount } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';

	let shops = $state([]) as Shop[];
	let polygons = $state([]) as Polygon[];
	let map: L.Map;

	const AREA_COLORS = {
		protected_area: '#2d6a4f',
		nature_reserve: '#52b788',
		forest: '#95d5b2'
	};

	async function fetchShops() {
		const response = await fetch('http://localhost:8000/stores');
		const data = await response.json();
		console.log('shops:', data);
		shops = data;
	}

	async function fetchPolygons() {
		const response = await fetch('http://localhost:8000/polygons');
		const data = await response.json();
		console.log('polygons:', data);
		polygons = data;
	}

	function drawPolygons() {
		for (const area of polygons) {
			const color = AREA_COLORS[area.type] ?? '#52b788';

			// Leaflet polygon format: [outerRing, holeRing1, holeRing2, ...]
			const rings = [...area.outer, ...area.inner] as L.LatLngExpression[][];

			L.polygon(rings, {
				color: color,
				fillColor: color,
				fillOpacity: 0.3,
				weight: 1
			})
				.bindPopup(`<b>${area.name}</b><br/>${area.type}`)
				.addTo(map);
		}
	}

	function drawShops() {
		for (const shop of shops) {
			L.marker([shop.lat, shop.lng]).bindPopup(`<b>${shop.name}</b>`).addTo(map);
		}
	}

	onMount(async () => {
		map = L.map('map').setView([50.061, 19.937], 13);

		L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '© OpenStreetMap contributors'
		}).addTo(map);

		await Promise.all([fetchShops(), fetchPolygons()]);

		drawShops();
		drawPolygons();
	});
</script>

<div id="map"></div>

<style>
	#map {
		height: 100vh;
		width: 100%;
	}
</style>
