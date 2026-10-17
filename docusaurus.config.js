const config = {
  title: 'MSL documentation',
  tagline: 'Linux distributions on macOS, the way WSL runs them on Windows.',
  favicon: 'img/favicon.ico',
  url: 'https://onexay.github.io',
  baseUrl: '/msl-docs/',
  organizationName: 'onexay',
  projectName: 'msl-docs',
  deploymentBranch: 'gh-pages',
  trailingSlash: true,
  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: 'docs',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/onexay/msl-docs/edit/main/docs/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themes: [
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        language: ['en'],
        docsRouteBasePath: '/docs',
      },
    ],
  ],

  themeConfig: {
    image: 'img/msl-social-card.png',
    colorMode: {
      defaultMode: 'light',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'MSL documentation',
      logo: {
        alt: 'MSL',
        src: 'img/logo.png',
      },
      items: [
        { to: '/docs/', label: 'Docs', position: 'left' },
        {
          to: '/docs/release-notes/',
          label: 'Release notes',
          position: 'left',
        },
        {
          href: 'https://github.com/onexay/msl',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'light',
      links: [
        {
          title: 'Documentation',
          items: [
            { label: 'Install MSL', to: '/docs/install/install/' },
            { label: 'Troubleshooting', to: '/docs/troubleshooting/' },
            { label: 'Release notes', to: '/docs/release-notes/' },
          ],
        },
        {
          title: 'Project',
          items: [
            { label: 'GitHub', href: 'https://github.com/onexay/msl' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} MSL contributors. MSL is an independent project, not affiliated with Microsoft or Apple.`,
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
    },
  },
};

module.exports = config;
