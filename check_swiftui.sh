#!/usr/bin/env bash

# usage: check_swiftui.sh /path/to/App.app OR /path/to/binary

app_path="$1"

if [[ -z "$app_path" ]]; then
    echo "usage: $0 /path/to/App.app OR /path/to/binary"
    exit 1
fi

# if it's an app bundle, find the binary
if [[ "$app_path" == *.app ]]; then
    binary_path=$(defaults read "$app_path/Contents/Info.plist" CFBundleExecutable 2>/dev/null)
    if [[ -z "$binary_path" ]]; then
        echo "error: could not find CFBundleExecutable"
        exit 1
    fi
    binary_full_path="$app_path/Contents/MacOS/$binary_path"
else
    binary_full_path="$app_path"
fi

if [[ ! -f "$binary_full_path" ]]; then
    echo "error: binary not found at $binary_full_path"
    exit 1
fi

echo "checking: $binary_full_path"

# check for linked SwiftUI framework
if otool -L "$binary_full_path" | grep -q SwiftUI; then
    echo "✓ linked to SwiftUI.framework"
else
    echo "✗ not linked to SwiftUI.framework"
fi

# check for SwiftUI symbols
if strings "$binary_full_path" 2>/dev/null | grep -q SwiftUI; then
    echo "✓ SwiftUI symbols found"
else
    echo "✗ no SwiftUI symbols found"
fi
