import { LucideIcon } from 'lucide-react';

interface PageHeroProps {
  icon: LucideIcon;
  title: string;
  description: string;
  variant?: 'default' | 'midnight' | 'sunrise';
  backgroundImage?: string;
  className?: string;
}

export function PageHero({
  icon: Icon,
  title,
  description,
  variant = 'default',
  backgroundImage,
  className,
}: PageHeroProps) {
  const variants = {
    default: 'bg-gradient-to-br from-latte-50 to-latte-100/50',
    midnight: 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white',
    sunrise: 'bg-gradient-to-br from-orange-50 to-amber-50',
  };

  const baseClasses =
    'relative overflow-hidden p-8 md:p-10 mb-8 mt-2 shadow-sm border border-latte-200/50';
  const roundedClass = className?.includes('rounded-') ? '' : 'rounded-3xl';

  return (
    <div
      className={`
      ${baseClasses}
      ${variants[variant]}
      ${roundedClass}
      ${className || ''}
    `}
    >
      {/* Background Image Overlay */}
      {backgroundImage && (
        <>
          <div
            className="absolute inset-0 z-0 bg-cover bg-center opacity-40 mix-blend-overlay transition-opacity duration-700"
            style={{ backgroundImage: `url(${backgroundImage})` }}
          />
          <div className="absolute inset-0 z-0 bg-gradient-to-r from-black/60 to-transparent" />
        </>
      )}

      <div className="relative z-10 flex flex-col md:flex-row gap-6 md:items-center">
        <div
          className={`
          p-3 rounded-2xl w-fit
          ${variant === 'midnight' ? 'bg-white/10 text-white backdrop-blur-sm' : 'bg-white shadow-sm text-latte-600'}
        `}
        >
          <Icon className="w-8 h-8 md:w-10 md:h-10" />
        </div>
        <div className="space-y-2">
          <h1 className="text-3xl md:text-4xl font-serif font-bold tracking-tight drop-shadow-sm">
            {title}
          </h1>
          <p
            className={`
            text-base md:text-lg max-w-2xl
            ${variant === 'midnight' ? 'text-slate-200' : 'text-latte-600'}
          `}
          >
            {description}
          </p>
        </div>
      </div>

      {/* Background Decor (Only if no image, or subtle overlay) */}
      {!backgroundImage && (
        <>
          <div className="absolute top-0 right-0 -mt-10 -mr-10 w-64 h-64 bg-blob-orange/20 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-48 h-48 bg-blob-green/20 rounded-full blur-3xl pointer-events-none" />
        </>
      )}
    </div>
  );
}
