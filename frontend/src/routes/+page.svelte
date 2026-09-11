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
	import { supermarketCompanies, type MockShop, type WelfareStatus } from '$lib/mock-data';

	let shops = $state([]) as Shop[];
	let polygons = $state([]) as Polygon[];
	let map: L.Map;
	let selectedCompanyId = $state(supermarketCompanies[0].id);
	let selectedShopId = $state<number | null>(null);
	let expandedCompanyId = $state<string | null>(supermarketCompanies[0].id);
	let showPanel = $state(true);

	const selectedCompany = $derived(
		supermarketCompanies.find((company) => company.id === selectedCompanyId) ??
			supermarketCompanies[0]
	);
	const selectedShop = $derived(selectedCompany.shops.find((shop) => shop.id === selectedShopId));
	const concernCount = $derived(
		selectedCompany.shops.reduce(
			(total, shop) => total + shop.metrics.filter((metric) => metric.status === 'concern').length,
			0
		)
	);

	const AREA_COLORS = {
		protected_area: '#2d6a4f',
		nature_reserve: '#52b788',
		forest: '#95d5b2'
	};

	const STATUS_STYLES: Record<WelfareStatus, { dot: string; text: string; badge: string }> = {
		good: {
			dot: 'bg-emerald-500',
			text: 'text-emerald-700',
			badge: 'bg-emerald-50 text-emerald-700'
		},
		mixed: { dot: 'bg-amber-500', text: 'text-amber-700', badge: 'bg-amber-50 text-amber-700' },
		concern: { dot: 'bg-rose-500', text: 'text-rose-700', badge: 'bg-rose-50 text-rose-700' },
		unknown: { dot: 'bg-slate-400', text: 'text-slate-600', badge: 'bg-slate-100 text-slate-600' }
	};

	function selectCompany(companyId: string) {
		selectedCompanyId = companyId;
		expandedCompanyId = companyId;
		selectedShopId = null;
	}

	function toggleCompany(companyId: string) {
		if (expandedCompanyId === companyId) {
			expandedCompanyId = null;
			return;
		}

		selectCompany(companyId);
	}

	function selectShop(companyId: string, shop: MockShop) {
		selectedCompanyId = companyId;
		expandedCompanyId = companyId;
		selectedShopId = shop.id;
		if (map) map.setView(shop.coordinates, 15, { animate: true });
	}

	function metricStyle(status: WelfareStatus) {
		return STATUS_STYLES[status];
	}

	async function fetchShops() {
		const response = await fetch('http://localhost:8000/stores');
		shops = await response.json();
	}

	async function fetchPolygons() {
		const response = await fetch('http://localhost:8000/polygons');
		polygons = await response.json();
	}

	function drawPolygons() {
		for (const area of polygons) {
			const color = AREA_COLORS[area.type] ?? '#52b788';
			const rings = area.outer as L.LatLngExpression[][];
			L.polygon(rings, { color, fillColor: color, fillOpacity: 0.3, weight: 1 })
				.bindPopup(`<b>${area.name}</b><br/>${area.type}`)
				.addTo(map);
		}
	}

	function drawShops() {
		for (const shop of shops) {
			const marker = L.marker([shop.lat, shop.lng]).bindPopup(`<b>${shop.name}</b>`);
			marker.setIcon(getIcon(shop.name));
			marker.addTo(map);
		}
	}

	function getIcon(store: string) {
		const company = supermarketCompanies.find((item) =>
			store.toLowerCase().startsWith(item.name.toLowerCase())
		);
		const icon = company?.shortName ?? store[0] ?? '?';
		const color = company?.brandColor ?? '#64748b';

		return L.divIcon({
			className: 'company-marker',
			html: `<span class="company-marker__pin" style="--marker-color: ${color}"><span>${icon}</span></span>`,
			iconSize: [42, 48],
			iconAnchor: [21, 43],
			popupAnchor: [0, -40]
		});
	}

	onMount(async () => {
		map = L.map('map', { zoomControl: false }).setView([50.061, 19.937], 13);
		L.control.zoom({ position: 'topright' }).addTo(map);
		L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '© OpenStreetMap contributors'
		}).addTo(map);

		try {
			await Promise.all([fetchShops(), fetchPolygons()]);
			drawShops();
			drawPolygons();
		} catch {
			// The panel remains useful while the local API is offline.
		}
	});
</script>

<svelte:head>
	<title>Hen welfare map | Field notes</title>
	<meta
		name="description"
		content="A fieldwork view of supermarket egg and chicken welfare information."
	/>
</svelte:head>

<main class="relative h-screen overflow-hidden bg-[#f5f3ed] text-slate-950">
	<div id="map" class="absolute inset-0"></div>

	<header
		class="map-header absolute top-4 right-4 left-4 z-[1000] flex items-start justify-end gap-3 sm:top-6 sm:right-6 sm:left-6"
	>
		<button
			type="button"
			class="flex h-11 items-center gap-2 rounded-sm border border-slate-900/10 bg-[#fffdf8]/95 px-3 text-sm font-bold shadow-xl shadow-slate-900/10 backdrop-blur transition hover:bg-white lg:hidden"
			onclick={() => (showPanel = !showPanel)}
			aria-expanded={showPanel}
		>
			<span aria-hidden="true">{showPanel ? '×' : '☰'}</span>
			<span>{showPanel ? 'Close' : 'Explore'}</span>
		</button>
	</header>

	<aside
		class:translate-x-0={showPanel}
		class:translate-x-[-110%]={!showPanel}
		class="research-panel absolute top-0 bottom-0 left-0 z-[999] flex w-full max-w-[430px] flex-col overflow-hidden border-r border-slate-900/10 bg-[#fffdf8] shadow-2xl shadow-slate-950/20 transition-transform duration-300 lg:translate-x-0"
	>
		<div class="panel-brand">
			<p class="font-mono text-[10px] font-bold tracking-[0.2em] text-emerald-700 uppercase">
				Field notes / 2024
			</p>
			<h1 class="mt-1 font-serif text-xl leading-none font-bold tracking-tight sm:text-2xl">
				Hen welfare map
			</h1>
		</div>
		<div class="research-panel__inner flex min-h-0 flex-1 flex-col px-5 pt-28 pb-5 sm:px-7 lg:pt-8">
			<div class="mb-6 border-b border-slate-900/10 pb-5">
				<div class="flex items-end justify-between gap-3">
					<div>
						<p class="font-mono text-[10px] font-bold tracking-[0.18em] text-slate-500 uppercase">
							Campaign research tool
						</p>
						<h2 class="mt-2 font-serif text-3xl leading-none font-bold tracking-tight">
							Supermarkets
						</h2>
					</div>
					<div class="text-right">
						<p class="font-mono text-2xl font-bold text-rose-600">{concernCount}</p>
						<p
							class="max-w-20 text-[10px] leading-tight font-bold tracking-wider text-slate-500 uppercase"
						>
							flags in view
						</p>
					</div>
				</div>
				<p class="mt-3 max-w-sm text-sm leading-5 text-slate-600">
					Explore local observations and the policies behind the shelf labels.
				</p>
			</div>

			<nav aria-label="Supermarket companies" class="mb-6 space-y-1">
				<p class="mb-2 font-mono text-[10px] font-bold tracking-[0.18em] text-slate-500 uppercase">
					Companies
				</p>
				{#each supermarketCompanies as company (company.id)}
					<div class="border-b border-slate-900/5 pb-1">
						<button
							type="button"
							class="group flex w-full items-center gap-3 py-3 text-left transition hover:px-2"
							class:bg-slate-100={selectedCompanyId === company.id}
							aria-expanded={expandedCompanyId === company.id}
							aria-controls={`shops-${company.id}`}
							onclick={() => toggleCompany(company.id)}
						>
							<span
								class="company-avatar grid h-8 w-8 shrink-0 place-items-center text-sm font-black text-white"
								style={`--company-color: ${company.brandColor}`}>{company.shortName}</span
							>
							<span class="min-w-0 flex-1">
								<span class="block text-sm font-bold">{company.name}</span>
								<span class="block text-xs text-slate-500"
									>{company.shopCount} mapped {company.shopCount === 1 ? 'shop' : 'shops'}</span
								>
							</span>
							<span class="grid h-7 w-7 shrink-0 place-items-center" aria-hidden="true">
								<span
									class:company-chevron--expanded={expandedCompanyId === company.id}
									class="company-chevron"
								></span>
							</span>
						</button>

						{#if expandedCompanyId === company.id}
							<div
								id={`shops-${company.id}`}
								class="mb-3 ml-11 space-y-1 border-l border-slate-200 pl-3"
							>
								{#each company.shops as shop (shop.id)}
									<button
										type="button"
										class="w-full rounded-r-md px-3 py-2 text-left transition hover:bg-slate-100"
										class:bg-emerald-50={selectedShopId === shop.id}
										onclick={() => selectShop(company.id, shop)}
									>
										<span class="flex items-start justify-between gap-3">
											<span class="text-sm leading-4 font-bold">{shop.name}</span>
											<span class="shrink-0 text-xs text-slate-400" aria-hidden="true">⌖</span>
										</span>
										<span class="mt-1 block text-xs text-slate-500">{shop.address}</span>
										<span
											class="mt-2 flex items-center gap-1.5 text-[10px] font-bold tracking-wider text-slate-400 uppercase"
										>
											<span class="h-1.5 w-1.5 rounded-full bg-slate-400"></span>
											Checked {shop.lastChecked}
										</span>
									</button>
								{/each}
							</div>
						{/if}
					</div>
				{/each}
			</nav>
		</div>
	</aside>

	{#if selectedShop}
		<section class="selected-location-panel" aria-labelledby="shop-detail-title">
			<div class="selected-location-panel__scroll">
				<div class="flex items-start justify-between gap-4">
					<div>
						<p class="font-mono text-[10px] font-bold tracking-[0.18em] text-emerald-700 uppercase">
							Selected location
						</p>
						<h2 id="shop-detail-title" class="mt-1 font-serif text-2xl leading-tight font-bold">
							{selectedShop.name}
						</h2>
					</div>
					<span
						class="rounded-full bg-amber-50 px-2 py-1 text-[10px] font-bold tracking-wider text-amber-700 uppercase"
					>
						{selectedCompany.name}
					</span>
				</div>
				<p class="mt-2 text-xs text-slate-500">
					{selectedShop.address} · Last checked {selectedShop.lastChecked}
				</p>

				<div class="mt-5 space-y-2">
					{#each selectedShop.metrics as metric (metric.label)}
						{@const style = metricStyle(metric.status)}
						<div class="border border-slate-900/10 p-3">
							<div class="flex items-center justify-between gap-3">
								<span class="flex items-center gap-2 text-xs font-bold">
									<span class={`h-2 w-2 rounded-full ${style.dot}`}></span>{metric.label}
								</span>
								<span
									class={`rounded-full px-2 py-1 text-[10px] font-bold tracking-wide uppercase ${style.badge}`}
								>
									{metric.value}
								</span>
							</div>
							<p class="mt-2 text-xs leading-4 text-slate-600">{metric.detail}</p>
						</div>
					{/each}
				</div>

				<div class="mt-5 border-l-2 border-amber-400 bg-amber-50/70 px-4 py-3">
					<p class="text-[10px] font-bold tracking-[0.16em] text-amber-800 uppercase">
						Company context
					</p>
					<p class="mt-1 text-xs leading-5 text-amber-950">{selectedCompany.policy}</p>
				</div>

				<div class="mt-5 pb-4">
					<p class="font-mono text-[10px] font-bold tracking-[0.18em] text-slate-500 uppercase">
						Useful for campaigners
					</p>
					<ul class="mt-3 space-y-2">
						{#each selectedShop.notes as note (note)}
							<li class="flex gap-2 text-xs leading-5 text-slate-600">
								<span class="font-bold text-emerald-700">+</span>{note}
							</li>
						{/each}
					</ul>
				</div>
			</div>
		</section>
	{/if}
</main>

<style>
	:global(html),
	:global(body) {
		margin: 0;
		min-width: 320px;
	}

	:global(body) {
		font-family: 'Avenir Next', 'Segoe UI', sans-serif;
	}

	#map {
		height: 100vh;
		width: 100%;
	}

	.research-panel {
		background: #fffdf8;
	}

	.panel-brand {
		padding: 24px 28px 20px;
		border-bottom: 1px solid rgb(15 23 42 / 10%);
	}

	.selected-location-panel {
		position: absolute;
		top: 24px;
		right: 24px;
		z-index: 998;
		width: min(390px, calc(100vw - 480px));
		max-height: calc(100vh - 48px);
		overflow: hidden;
		border: 1px solid rgb(15 23 42 / 12%);
		border-radius: 18px;
		background: #fffdf8;
		box-shadow: 0 16px 40px rgb(15 23 42 / 20%);
	}

	.selected-location-panel__scroll {
		max-height: calc(100vh - 48px);
		overflow-y: auto;
		padding: 24px;
	}

	.research-panel__inner {
		padding: 32px 28px 28px;
	}

	@media (max-width: 1023px) {
		.map-header {
			top: 14px;
			right: 14px;
			left: 14px;
		}

		.research-panel {
			top: auto;
			right: 12px;
			bottom: 12px;
			left: 12px;
			width: auto;
			max-width: none;
			max-height: 78vh;
			border: 1px solid rgb(15 23 42 / 12%);
			border-radius: 18px 18px 10px 10px;
			box-shadow: 0 16px 40px rgb(15 23 42 / 24%);
		}

		.research-panel__inner {
			padding: 20px 20px 20px;
		}

		.panel-brand {
			padding: 16px 20px 14px;
		}

		.research-panel__inner > :global(div:first-child) {
			margin-bottom: 20px;
			padding-bottom: 16px;
		}

		.research-panel__inner nav {
			margin-bottom: 20px;
		}

		.selected-location-panel {
			top: 78px;
			right: 12px;
			width: min(390px, calc(100vw - 24px));
			max-height: calc(100vh - 100px);
			border-radius: 16px;
		}

		.selected-location-panel__scroll {
			max-height: calc(100vh - 100px);
			padding: 20px;
		}
	}

	@media (min-width: 1024px) {
		.research-panel {
			border-radius: 0 18px 18px 0;
		}
	}
</style>
