# 🎨 EngageMeter Favicon

This directory contains the favicon files for the EngageMeter application.

## 📁 Files

- **`favicon.svg`** - Vector-based favicon (modern browsers)
- **`favicon.ico`** - Traditional ICO format (legacy browsers)

## 🚀 Usage

The favicon is automatically included in the base template (`base.html`) and will appear in:

- Browser tabs
- Bookmarks
- Browser history
- Mobile home screen shortcuts

## 🔧 Customization

### Colors

The favicon uses the EngageMeter brand colors:

- **Primary Blue**: `#3B82F6` (Tailwind blue-500)
- **Dark Blue**: `#1E40AF` (Tailwind blue-800)
- **Accent Colors**: Red for likes, green for retweets, yellow for replies

### Elements

The favicon represents:

- 📊 **Chart bars** - Analytics and data visualization
- ❤️ **Heart** - Likes and engagement
- 🔄 **Arrows** - Retweets and sharing
- 💬 **Bubble** - Replies and conversations
- ⚡ **Pulse rings** - Active engagement and real-time data

## 🛠️ Development

### Converting SVG to ICO

To regenerate the ICO file from the SVG:

```bash
# Install dependencies
pip install cairosvg pillow

# Run conversion script
python scripts/create_favicon.py
```

### Manual Conversion

You can also use online tools:

1. Upload `favicon.svg` to a converter like [ConvertICO](https://convertico.com/)
2. Download the generated ICO file
3. Replace `favicon.ico` in this directory

## 🌐 Browser Support

- **Modern browsers**: Use SVG favicon (crisp at all sizes)
- **Legacy browsers**: Fall back to ICO format
- **Mobile**: Both formats supported for home screen shortcuts

## 📱 Sizes Included

The ICO file contains multiple sizes:

- 16×16 px (browser tabs)
- 32×32 px (desktop bookmarks)
- 48×48 px (Windows taskbar)

## ✨ Design Principles

The favicon follows these design principles:

- **Simple & Recognizable** - Easy to identify at small sizes
- **Brand Consistent** - Uses EngageMeter color palette
- **Meaningful** - Represents the app's core functionality
- **Scalable** - Looks good at all sizes from 16px to 48px
