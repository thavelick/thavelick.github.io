#!/bin/bash
# Check for broken local links and broken images in the two archived Don Rosa sites

ARCHIVE_DIR="application/static/archive"
ERRORS=0

check_site() {
  local site_dir="$1"
  local site_name="$2"
  echo "=== $site_name ==="

  for file in "$site_dir"/*.html "$site_dir"/*.htm; do
    [ -f "$file" ] || continue
    basename="$(basename "$file")"

    # Check local href links (skip external URLs, mailto, and anchors)
    grep -oiP 'href="([^"#][^"]*)"' "$file" | grep -oiP '"[^"]*"' | tr -d '"' | while read -r link; do
      # Skip external links
      case "$link" in
        http://*|https://*|mailto:*|//*)
          continue
          ;;
      esac
      target="$site_dir/$link"
      if [ ! -f "$target" ]; then
        echo "  BROKEN LINK in $basename: $link"
        ERRORS=$((ERRORS + 1))
      fi
    done

    # Check image src references
    grep -oiP 'src="([^"]+)"' "$file" | grep -oiP '"[^"]*"' | tr -d '"' | while read -r img; do
      # Skip external images
      case "$img" in
        http://*|https://*|//*)
          continue
          ;;
      esac
      target="$site_dir/$img"
      if [ ! -f "$target" ]; then
        echo "  BROKEN IMAGE in $basename: $img"
        ERRORS=$((ERRORS + 1))
      fi
    done
  done
  echo ""
}

check_site "$ARCHIVE_DIR/two-worlds-of-don-rosa" "Two Worlds of Don Rosa (original)"
check_site "$ARCHIVE_DIR/two-worlds-of-don-rosa-v2" "Two Worlds of Don Rosa (successor)"

if [ $ERRORS -eq 0 ]; then
  echo "No broken local links or images found!"
fi
