source "https://rubygems.org"

# Pin to versions supported by GitHub Pages.
# See: https://pages.github.com/versions/
gem "github-pages", group: :jekyll_plugins
group :jekyll_plugins do
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
  gem "jekyll-feed"
end

# Optional: Windows and JRuby do not include zoneinfo files
platforms :mingw, :x64_mingw, :msys, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.17.1", :platforms => [:mingw, :x64_mingw, :msys]
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
