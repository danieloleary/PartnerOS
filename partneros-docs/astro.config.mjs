// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	base: '/PartnerOS',
	site: 'https://danieloleary.github.io',
	integrations: [
		starlight({
			title: 'PartnerOS',
			description: 'The complete playbook for building and scaling strategic partnerships with AI-powered automation.',
			logo: {
				src: './src/assets/logo.svg',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/danieloleary/PartnerOS' },
				{ icon: 'linkedin', label: 'LinkedIn', href: 'https://linkedin.com/in/danieloleary' },
			],
			customCss: [
				'./src/content/docs/stylesheets/extra.css',
			],
			sidebar: [
			{ label: 'Getting Started', autogenerate: { directory: 'getting-started' } },
			{ label: 'Strategy', autogenerate: { directory: 'strategy' } },
			{ label: 'Recruitment', autogenerate: { directory: 'recruitment' } },
			{ label: 'Enablement', autogenerate: { directory: 'enablement' } },
			{ label: 'Legal', autogenerate: { directory: 'legal' } },
			{ label: 'Finance', autogenerate: { directory: 'finance' } },
			{ label: 'Security', autogenerate: { directory: 'security' } },
			{ label: 'Operations', autogenerate: { directory: 'operations' } },
			{ label: 'Executive', autogenerate: { directory: 'executive' } },
			{ label: 'Analysis', autogenerate: { directory: 'analysis' } },
			{ label: 'Partner Agent', autogenerate: { directory: 'agent' } },
			{ label: 'Skills', autogenerate: { directory: 'skills' } },
		],
		}),
	],
});
