import { motion } from 'framer-motion';

interface SkeletonProps {
  className?: string;
  count?: number;
}

const Skeleton = ({ className = '', count = 1 }: SkeletonProps) => {
  const skeletons = Array.from({ length: count }, (_, index) => (
    <motion.div
      key={index}
      className={`rounded-xl bg-slate-800/40 border border-slate-700/30 ${className}`}
      initial={{ opacity: 0.5 }}
      animate={{ opacity: [0.5, 0.8, 0.5] }}
      transition={{
        repeat: Infinity,
        duration: 1.5,
        ease: 'easeInOut'
      }}
    />
  ));

  return <>{skeletons}</>;
};

export default Skeleton;