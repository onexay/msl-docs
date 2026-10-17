import clsx from 'clsx';
import styles from './styles.module.css';

export default function CardGrid({ children }) {
  return <div className={clsx(styles.grid, 'margin-top--md')}>{children}</div>;
}
