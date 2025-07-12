#!/usr/bin/env python3
"""Analyze PvPoke rankings changes over time"""
import json
import sys

def compare_rankings(old_file, new_file):
    """Compare two ranking files and show significant changes"""
    with open(old_file, 'r') as f:
        old_data = json.load(f)
    with open(new_file, 'r') as f:
        new_data = json.load(f)
    
    # Create lookup dictionaries
    old_lookup = {p['speciesId']: p for p in old_data}
    new_lookup = {p['speciesId']: p for p in new_data}
    
    # Track significant changes
    significant_changes = []
    
    for species_id in new_lookup:
        if species_id in old_lookup:
            old_score = old_lookup[species_id]['score']
            new_score = new_lookup[species_id]['score']
            
            # Consider changes > 5 points significant
            if abs(new_score - old_score) > 5:
                significant_changes.append({
                    'name': new_lookup[species_id]['speciesName'],
                    'old_score': old_score,
                    'new_score': new_score,
                    'change': new_score - old_score
                })
    
    # Sort by magnitude of change
    significant_changes.sort(key=lambda x: abs(x['change']), reverse=True)
    
    print(f"Significant changes detected: {len(significant_changes)}")
    for change in significant_changes[:10]:
        direction = "↑" if change['change'] > 0 else "↓"
        print(f"{change['name']}: {change['old_score']:.1f} → {change['new_score']:.1f} "
              f"({direction}{abs(change['change']):.1f})")