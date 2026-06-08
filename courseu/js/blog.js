const articles = [
  {
    id: 1,
    slug: '404.html',
    image: '../img/blog/articles/article-1.webp',
    imageAlt: 'Аналітика digital-маркетингу на дашборді',
    category: 'digital',
    categoryLabel: 'Digital-маркетинг',
    author: 'Андрій Мельник',
    date: '12 травня',
    readTime: '7 хв читання',
    title: '5 трендів digital-маркетингу, що визначатимуть ринок у найближчі роки',
    excerpt: 'Розбираємо ключові тенденції у digital-маркетингу, які вже зараз змінюють підходи компаній до просування своїх продуктів і послуг.',
  },
  {
    id: 2,
    slug: '404.html',
    image: '../img/blog/articles/article-2.webp',
    imageAlt: 'Розробка фірмового стилю та логотипу',
    category: 'brand',
    categoryLabel: 'Брендинг',
    author: 'Олена Іваненко',
    date: '8 травня',
    readTime: '10 хв читання',
    title: 'Як побудувати сильний бренд з нуля: покроковий гід від стратегів',
    excerpt: 'Від нейму та логотипу до єдиного комунікаційного стилю — все, що потрібно знати для створення впізнаваного бренду.',
  },
  {
    id: 3,
    slug: '404.html',
    image: '../img/blog/articles/article-3.webp',
    imageAlt: 'Розробка email-розсилку на ноутбуці',
    category: 'email',
    categoryLabel: 'Email-маркетинг',
    author: 'Дмитро Шевченко',
    date: '2 травня',
    readTime: '6 хв читання',
    title: 'Email-воронки з конверсією 15%+: реальні кейси та перевірені техніки',
    excerpt: 'Практичні поради зі створення автоматизованих email-послідовностей на основі реальних кампаній наших клієнтів.',
  },
  {
    id: 4,
    slug: '404.html',
    image: '../img/blog/articles/article-4.webp',
    imageAlt: 'SEO аудит та аналіз ключових слів',
    category: 'seo',
    categoryLabel: 'SEO',
    author: 'Максим Бондаренко',
    date: '25 квітня',
    readTime: '9 хв читання',
    title: 'SEO просування: що змінилося після оновлень Google і як адаптуватися',
    excerpt: 'Детальний розбір останніх алгоритмічних змін Google та практичні рекомендації для збереження позицій у пошуку.',
  },
  {
    id: 5,
    slug: '404.html',
    image: '../img/blog/articles/article-5.webp',
    imageAlt: 'Планування контенту для соціальних мереж',
    category: 'smm',
    categoryLabel: 'Соціальні мережі',
    author: 'Олена Іваненко',
    date: '18 квітня',
    readTime: '5 хв читання',
    title: 'Instagram, TikTok чи LinkedIn: який канал обрати для вашого бізнесу',
    excerpt: 'Порівнюємо аудиторії, формати і рекламні можливості трьох провідних платформ, щоб ви зробили правильний вибір.',
  },
  {
    id: 6,
    slug: '404.html',
    image: '../img/blog/articles/article-6.webp',
    imageAlt: 'Команда розробляє маркетингову стратегію',
    category: 'strategy',
    categoryLabel: 'Стратегія',
    author: 'Андрій Мельник',
    date: '10 квітня',
    readTime: '11 хв читання',
    title: 'Як скласти маркетинговий план на рік: структура, KPI і типові помилки',
    excerpt: 'Шаблон маркетингового плану, яким користується наша команда при роботі з клієнтами, та пояснення ключових елементів.',
  },
  {
    id: 7,
    slug: '404.html',
    image: '../img/blog/articles/article-7.webp',
    imageAlt: 'Дизайн упаковки та фірмового стилю',
    category: 'brand',
    categoryLabel: 'Брендинг',
    author: 'Дмитро Шевченко',
    date: '3 квітня',
    readTime: '8 хв читання',
    title: 'Ребрендинг без втрат: як змінити образ компанії і не злякати клієнтів',
    excerpt: 'Кейси успішного ребрендингу та список критичних помилок, яких варто уникати, щоб зберегти лояльність аудиторії.',
  },
  {
    id: 8,
    slug: '404.html',
    image: '../img/blog/articles/article-8.webp',
    imageAlt: 'Аналіз даних та маркетингова аналітика',
    category: 'digital',
    categoryLabel: 'Digital-маркетинг',
    author: 'Максим Бондаренко',
    date: '28 березня',
    readTime: '7 хв читання',
    title: 'Контент-маркетинг vs платна реклама: що обрати при обмеженому бюджеті',
    excerpt: 'Порівнюємо обидва підходи за вартістю, швидкістю результату та довгостроковим ефектом з реальними цифрами.',
  },
  {
    id: 9,
    slug: '404.html',
    image: '../img/blog/articles/article-9.webp',
    imageAlt: 'Технічний SEO аудит сайту',
    category: 'seo',
    categoryLabel: 'SEO',
    author: 'Андрій Мельник',
    date: '20 березня',
    readTime: '12 хв читання',
    title: 'Технічний SEO-аудит: чекліст із 30 пунктів, який варто пройти кожному сайту',
    excerpt: 'Покроковий чекліст для самостійного технічного аудиту сайту, що допоможе виявити приховані проблеми з індексацією.',
  },
];

function renderCard(article) {
  return `
    <article class="blog-card" data-cat="${article.category}">
      <a href="${article.slug}" class="blog-card-img-link">
        <img
          src="${article.image}"
          alt="${article.imageAlt}"
          class="blog-card-img"
          width="500"
          height="280"
          loading="lazy"
        >
        <span class="blog-tag blog-tag-over">${article.categoryLabel}</span>
      </a>
      <div class="blog-card-body">
        <div class="blog-card-meta">
          <span class="blog-meta-author">${article.author}</span>
          <span class="blog-meta-dot" aria-hidden="true">·</span>
          <span class="blog-meta-date">${article.date}</span>
        </div>
        <h3 class="blog-card-title">
          <a href="${article.slug}">${article.title}</a>
        </h3>
        <p class="blog-card-excerpt">${article.excerpt}</p>
        <div class="blog-card-footer">
          <span class="blog-card-read">${article.readTime}</span>
          <a href="${article.slug}" class="blog-card-more">Читати<svg class="link-arrow" aria-hidden="true"><use href="icons/sprite.svg#arrow-right"></use></svg></a>
        </div>
      </div>
    </article>
  `;
}

document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('blogGrid');
  const catButtons = document.querySelectorAll('.blog-cat');

  function renderArticles(filter = 'all') {
    const filtered = filter === 'all'
      ? articles
      : articles.filter(a => a.category === filter);

    grid.innerHTML = filtered.map(renderCard).join('');
  }

  catButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      catButtons.forEach(b => b.classList.remove('blog-cat-active'));
      btn.classList.add('blog-cat-active');
      renderArticles(btn.dataset.cat);
    });
  });

  renderArticles();
});