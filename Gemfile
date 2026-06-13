source "https://rubygems.org"

# Minimal Jekyll + the three plugins we actually use. We deliberately
# don't depend on the `github-pages` meta-gem (which pulls in ~30 extra
# gems we don't need: jekyll-paginate, jekyll-coffeescript, jekyll-opal,
# jekyll-redirect-from, jekyll-github-metadata, ...). The site is built
# by .github/workflows/jekyll.yml using this lean Gemfile.

gem "jekyll", "~> 3.10"
# Jekyll 3 no longer bundles webrick. Needed for `bundle exec jekyll
# serve` on Ruby 3+.
gem "webrick", "~> 1.7"

group :jekyll_plugins do
  gem "jekyll-seo-tag"
  gem "jekyll-sitemap"
  gem "jekyll-feed"
end

# Windows + JRuby don't ship with zoneinfo; tzinfo-data provides it.
platforms :mingw, :x64_mingw, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end
