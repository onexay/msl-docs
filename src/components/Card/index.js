import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';

export default function Card({ title, description, href }) {
  const link = useBaseUrl(href);

  return (
    <Link className={styles.card} to={link}>
      <span className={styles.title}>{title}</span>
      {description && <span className={styles.description}>{description}</span>}
      <span className={styles.arrow} aria-hidden="true">→</span>
    </Link>
  );
}
