<div align="center">
  <h1>🏪 Shop Street</h1>
  <p><strong>Modern E-commerce Platform</strong></p>
  <p>A production-ready Django e-commerce platform with modern TailwindCSS frontend</p>
  
  ![Django](https://img.shields.io/badge/Django-4.2.7-092E20?style=for-the-badge&logo=django&logoColor=white)
  ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.3.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
  ![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
  
  <p>
    <a href="#features">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#deployment">Deployment</a> •
    <a href="#api-documentation">API</a> •
    <a href="#contributing">Contributing</a>
  </p>
</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🛍️ **E-commerce Core**
- 📦 **Product Catalog** - Categories, variants, images, reviews
- 🛒 **Shopping Cart** - Session & user-based management
- ❤️ **Wishlist** - Save products for later
- 📋 **Order Management** - Complete processing workflow
- 💳 **Payment Gateway** - Stripe integration ready
- 👤 **Authentication** - Django Allauth powered
- 🎟️ **Coupons & Discounts** - Flexible promotion system

</td>
<td width="50%">

### 🎨 **Modern Frontend**
- 🎯 **TailwindCSS** - Modern, responsive design
- ⚡ **Interactive UI** - AJAX-powered interactions
- 📱 **Mobile-First** - Fully responsive design
- 🚀 **Performance** - Optimized images & lazy loading
- 🔍 **Search** - Advanced product search
- 📊 **Admin Dashboard** - Comprehensive management

</td>
</tr>
</table>

### 🔧 **Production Ready**
- 🔒 **Security** - CSRF protection, secure headers, XSS prevention
- ⚡ **Performance** - Static file optimization, caching ready
- 📈 **Scalability** - Modular architecture, database optimization
- 🔍 **SEO** - Meta tags, structured URLs, sitemap ready
- 📱 **PWA Ready** - Progressive Web App capabilities
- 🐳 **Docker Support** - Containerized deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/shop-street.git
   cd shop-street
   ```

2. **Setup Python environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```

4. **Setup database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python create_sample_data.py  # Optional: Add sample data
   ```

5. **Setup frontend**
   ```bash
   npm install
   npm run build-css
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

🎉 **Visit** `http://127.0.0.1:8000` to see your Shop Street platform!

> 💡 **Admin Panel**: `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

```
shop_street/
├── 👤 accounts/          # User management & authentication
├── 🛒 cart/             # Shopping cart & wishlist functionality
├── 🏠 core/             # Core app (home, search, etc.)
├── 📦 orders/           # Order processing & management
├── 🛍️ products/         # Product catalog & categories
├── 🏪 vendors/          # Multi-vendor support
├── 🎨 static/           # Static files (CSS, JS, images)
├── 📄 templates/        # HTML templates
├── 📁 media/            # User uploaded files
├── ⚙️ shop_street/      # Django project settings
├── 🐳 Dockerfile        # Docker configuration
├── 📋 requirements.txt  # Python dependencies
├── 📦 package.json      # Node.js dependencies
└── 🔧 setup.py         # Automated setup script
```

## ⚙️ Configuration

### Environment Variables
- `DEBUG`: Development mode (True/False)
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `STRIPE_PUBLISHABLE_KEY`: Stripe public key
- `STRIPE_SECRET_KEY`: Stripe secret key
- `EMAIL_HOST_USER`: SMTP email username
- `EMAIL_HOST_PASSWORD`: SMTP email password

### Database
Default: SQLite (development)
Production: PostgreSQL recommended

### Static Files
- Development: Django serves static files
- Production: Use WhiteNoise or CDN

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False` in environment
2. Configure production database
3. Set up email backend
4. Configure Stripe keys
5. Set up static file serving
6. Configure domain in `ALLOWED_HOSTS`

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "shop_street.wsgi:application"]
```

## 📚 API Documentation

### 🛍️ Products API
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products/` | List all products |
| `GET` | `/products/<slug>/` | Product details |
| `GET` | `/products/category/<slug>/` | Products by category |

### 🛒 Cart API
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/cart/add/` | Add item to cart |
| `POST` | `/cart/update/` | Update cart item |
| `DELETE` | `/cart/remove/<id>/` | Remove from cart |
| `GET` | `/cart/` | View cart contents |

### 📋 Orders API
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/orders/create/` | Create new order |
| `GET` | `/orders/<uuid>/` | Order details |
| `GET` | `/orders/` | User's order history |

### 👤 Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/accounts/login/` | User login |
| `POST` | `/accounts/signup/` | User registration |
| `POST` | `/accounts/logout/` | User logout |

## 🎨 Customization

### Adding New Product Fields
1. Update `products/models.py`
2. Create migration: `python manage.py makemigrations`
3. Run migration: `python manage.py migrate`
4. Update admin interface in `products/admin.py`

### Custom Styling
1. Edit `static/css/input.css`
2. Rebuild CSS: `npm run build-css`

### Payment Gateways
Extend `orders/models.py` and `orders/views.py` for additional payment methods.

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test products
```

## ⚡ Performance Optimization

### Database
- Add database indexes for frequently queried fields
- Use `select_related()` and `prefetch_related()` for queries
- Implement database connection pooling

### Caching
- Enable Django cache framework
- Use Redis for session storage
- Implement template fragment caching

### Static Files
- Use CDN for static files
- Enable gzip compression
- Optimize images

## 🔒 Security

### Implemented Security Features
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure headers
- Password validation
- Rate limiting ready

### Additional Security (Production)
- SSL/TLS certificates
- Security headers middleware
- Regular security updates
- Database backups
- Monitoring and logging

## 💬 Support & Community

- 📖 **Documentation**: [Wiki](https://github.com/yourusername/shop-street/wiki)
- 🐛 **Bug Reports**: [Issues](https://github.com/yourusername/shop-street/issues)
- 💡 **Feature Requests**: [Discussions](https://github.com/yourusername/shop-street/discussions)
- 💬 **Community**: [Discord](https://discord.gg/shopstreet)
- 📧 **Email**: support@shopstreet.com

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. 🍴 Fork the repository
2. 🌟 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💻 Make your changes
4. ✅ Add tests
5. 📝 Commit your changes (`git commit -m 'Add amazing feature'`)
6. 🚀 Push to the branch (`git push origin feature/amazing-feature`)
7. 🔄 Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the amazing framework
- TailwindCSS for the beautiful design system
- All contributors who help make this project better

---

<div align="center">
  <p><strong>Shop Street</strong> - Built by geloxh using Django and TailwindCSS</p>
  <p>⭐ Star us on GitHub if this project helped you!</p>
  
  <a href="https://github.com/yourusername/shop-street/stargazers">⭐ Stars</a> |
  <a href="https://github.com/yourusername/shop-street/network/members">🍴 Forks</a> |
  <a href="https://github.com/yourusername/shop-street/issues">🐛 Issues</a>
</div>