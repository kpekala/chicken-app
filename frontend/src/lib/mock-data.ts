export type WelfareStatus = 'good' | 'mixed' | 'concern' | 'unknown';

export interface WelfareMetric {
	label: string;
	value: string;
	status: WelfareStatus;
	detail: string;
}

export interface MockShop {
	id: number;
	name: string;
	address: string;
	coordinates: [number, number];
	lastChecked: string;
	metrics: WelfareMetric[];
	notes: string[];
}

export interface SupermarketCompany {
	id: string;
	name: string;
	shortName: string;
	brandColor: string;
	shopCount: number;
	summary: string;
	policy: string;
	shops: MockShop[];
}

export const supermarketCompanies: SupermarketCompany[] = [
	{
		id: 'biedronka',
		name: 'Biedronka',
		shortName: 'B',
		brandColor: '#e21b2d',
		shopCount: 3,
		summary: 'The largest supermarket network in Poland.',
		policy:
			'Biedronka successfully eliminated the sale of all fresh caged eggs from its stores in 2022, achieving its welfare target several years ahead of the original 2025 deadline. The supermarket chain is now expanding this commitment by working to ensure that at least 90% of eggs used as product ingredients are cage-free by 2026, alongside broader supplier policies that ban growth hormones and preventative antibiotics.',
		shops: [
			{
				id: 101,
				name: 'Biedronka · Szewska',
				address: 'ul. Szewska 15, Kraków',
				coordinates: [50.0619, 19.9368],
				lastChecked: '12 Sep 2024',
				metrics: [
					{
						label: 'Caged eggs',
						value: 'Not found',
						status: 'good',
						detail: 'No egg products from caged hens were observed.'
					},
					{
						label: 'Higher-welfare eggs',
						value: 'Some options',
						status: 'mixed',
						detail: 'Free-range and organic options were listed, but choice was limited.'
					},
					{
						label: 'Frankenchicken',
						value: 'No public policy',
						status: 'unknown',
						detail: 'No clear breed or slower-growth commitment found for chicken meat.'
					}
				],
				notes: [
					'Record the exact product, label, and price when documenting a visit.',
					'Ask staff whether cage-free eggs are planned for permanent range.'
				]
			},
			{
				id: 102,
				name: 'Biedronka · Pawia',
				address: 'ul. Pawia 5, Kraków',
				coordinates: [50.0682, 19.9451],
				lastChecked: '04 Sep 2024',
				metrics: [
					{
						label: 'Caged eggs',
						value: 'Found',
						status: 'concern',
						detail: 'Conventional eggs were available on the main shelf.'
					},
					{
						label: 'Higher-welfare eggs',
						value: 'Good choice',
						status: 'good',
						detail: 'Several free-range products were visible during the visit.'
					},
					{
						label: 'Frankenchicken',
						value: 'Not verified',
						status: 'unknown',
						detail: 'Meat provenance and breed information were not visible.'
					}
				],
				notes: ['Photograph shelf labels rather than relying on packaging colour alone.']
			},
			{
				id: 103,
				name: 'Biedronka · Dietla',
				address: 'ul. Dietla 64, Kraków',
				coordinates: [50.0524, 19.9427],
				lastChecked: '28 Aug 2024',
				metrics: [
					{
						label: 'Caged eggs',
						value: 'Found',
						status: 'concern',
						detail: 'Caged eggs were available in multiple pack sizes.'
					},
					{
						label: 'Higher-welfare eggs',
						value: 'Some options',
						status: 'mixed',
						detail: 'One organic option was identified.'
					},
					{
						label: 'Frankenchicken',
						value: 'Not verified',
						status: 'unknown',
						detail: 'No public in-store information about chicken breeds.'
					}
				],
				notes: ['Check whether the range changes after the next policy deadline.']
			}
		]
	},
	{
		id: 'lidl',
		name: 'Lidl',
		shortName: 'L',
		brandColor: '#0050aa',
		shopCount: 2,
		summary: 'A discount chain with a growing sustainability programme.',
		policy: 'Egg sourcing progress is reported, but local availability can vary.',
		shops: [
			{
				id: 201,
				name: 'Lidl · Starowiślna',
				address: 'ul. Starowiślna 75, Kraków',
				coordinates: [50.0556, 19.9478],
				lastChecked: '10 Sep 2024',
				metrics: [
					{
						label: 'Caged eggs',
						value: 'Not found',
						status: 'good',
						detail: 'No caged egg products were found in this visit.'
					},
					{
						label: 'Higher-welfare eggs',
						value: 'Good choice',
						status: 'good',
						detail: 'Free-range and organic products were clearly labelled.'
					},
					{
						label: 'Frankenchicken',
						value: 'Policy unclear',
						status: 'mixed',
						detail: 'Some welfare language exists, but breed commitments need verification.'
					}
				],
				notes: ['Compare shelf findings with Lidl public commitments before publishing a score.']
			},
			{
				id: 202,
				name: 'Lidl · Ruczaj',
				address: 'ul. Kobierzyńska 93, Kraków',
				coordinates: [50.0279, 19.9041],
				lastChecked: '02 Sep 2024',
				metrics: [
					{
						label: 'Caged eggs',
						value: 'Not found',
						status: 'good',
						detail: 'No caged egg products were found in this visit.'
					},
					{
						label: 'Higher-welfare eggs',
						value: 'Good choice',
						status: 'good',
						detail: 'Multiple free-range options were available.'
					},
					{
						label: 'Frankenchicken',
						value: 'Policy unclear',
						status: 'mixed',
						detail: 'No breed information was displayed on the meat fixture.'
					}
				],
				notes: ['Ask for supply-chain information when the product label is incomplete.']
			}
		]
	},
	{
		id: 'carrefour',
		name: 'Carrefour',
		shortName: 'C',
		brandColor: '#1455a0',
		shopCount: 1,
		summary: 'A hypermarket network with a broad private-label range.',
		policy: 'Private-label welfare claims should be checked product by product.',
		shops: [
			{
				id: 301,
				name: 'Carrefour · Galeria Krakowska',
				address: 'ul. Pawia 5, Kraków',
				coordinates: [50.0686, 19.9462],
				lastChecked: '06 Sep 2024',
				metrics: [
					{
						label: 'Caged eggs',
						value: 'Found',
						status: 'concern',
						detail: 'Caged eggs appeared in the full-price selection.'
					},
					{
						label: 'Higher-welfare eggs',
						value: 'Wide choice',
						status: 'good',
						detail: 'The store carried several non-cage systems and organic options.'
					},
					{
						label: 'Frankenchicken',
						value: 'Needs research',
						status: 'mixed',
						detail: 'More information is needed about growth rate and breed.'
					}
				],
				notes: [
					'Large stores may have different ranges by department; document the aisle and brand.'
				]
			}
		]
	}
];
