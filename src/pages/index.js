import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './index.module.css';

const features = [
  {
    title: 'The WSL command line',
    description: 'Same arguments, output, and exit codes. Use the scripts and READMEs your team already has.',
    to: '/docs/overview/basic-commands/',
  },
  {
    title: 'WSL Linux distributions',
    description: 'Use Ubuntu, Debian, Fedora, and other WSL images with their normal first-run setup.',
    to: '/docs/how-to/use-custom-distro/',
  },
  {
    title: 'Files both ways',
    description: 'Open Mac files from Linux and browse distribution files in Finder.',
    to: '/docs/concepts/filesystems/',
  },
  {
    title: 'One localhost',
    description: 'Reach services running in Linux from Mac apps, with DNS routed through macOS.',
    to: '/docs/concepts/networking/',
  },
  {
    title: 'VS Code and friends',
    description: 'Open folders inside a distribution from VS Code, Insiders, VSCodium, or Cursor.',
    to: '/docs/tutorials/msl-vscode/',
  },
  {
    title: 'Built on Apple virtualization',
    description: 'Run distributions in one lightweight VM on Apple silicon.',
    to: '/docs/concepts/how-it-works/',
  },
];

function TerminalPreview() {
  return (
    <div className={styles.terminal} aria-label="Example MSL terminal session">
      <div className={styles.terminalBar}>
        <span className={styles.terminalDots} aria-hidden="true"><i /><i /><i /></span>
        <span>Ubuntu · MSL</span>
        <span className={styles.running}><i /> Running</span>
      </div>
      <pre>
        <code>
          <span className={styles.prompt}>$</span> msl --install Ubuntu{'\n'}
          <span className={styles.prompt}>$</span> msl{'\n'}
          <span className={styles.comment}># You are now in Ubuntu</span>{'\n'}
          <span className={styles.prompt}>$</span> msl -l -v{'\n\n'}
          {'  NAME       STATE     VERSION\n'}
          {'  Ubuntu     Running   2'}
        </code>
      </pre>
    </div>
  );
}

export default function Home() {
  const logoUrl = useBaseUrl('img/logo.png');

  return (
    <Layout
      title="WSL Linux distributions on macOS"
      description="MSL runs Linux distributions on macOS with the commands WSL users already know."
    >
      <main className={styles.main}>
        <section className={styles.hero}>
          <div className={styles.heroCopy}>
            <img className={styles.heroLogo} src={logoUrl} alt="MSL logo" />
            <h1>WSL Linux environment, on Mac.</h1>
            <p className={styles.lede}>
              Run the WSL Linux distributions and commands your team already knows,
              in a lightweight virtual machine built with Apple’s Virtualization framework.
            </p>
            <div className={styles.actions}>
              <Link className={styles.primaryAction} to="/docs/install/install/">
                Install MSL <span aria-hidden="true">→</span>
              </Link>
              <Link className={styles.secondaryAction} to="/docs/">
                Explore the docs
              </Link>
            </div>
            <p className={styles.requirements}>Apple silicon · macOS 27 or later</p>
          </div>
          <TerminalPreview />
        </section>

        <section className={styles.capabilities}>
          <p className={styles.eyebrow}>A familiar WSL Linux workflow</p>
          <h2>Work across Mac and Linux without changing your tools.</h2>
          <div className={styles.featureGrid}>
            {features.map((feature) => (
              <Link className={styles.featureCard} key={feature.title} to={feature.to}>
                <span className={styles.featureTitle}>{feature.title}</span>
                <span className={styles.featureDescription}>{feature.description}</span>
                <span className={styles.featureArrow} aria-hidden="true">→</span>
              </Link>
            ))}
          </div>
        </section>
      </main>
    </Layout>
  );
}
