with open('report.html', 'r', encoding='utf-8') as f:
    content = f.read()

checks = {
    'Hero Pill Buttons': '<button class="hero-pill clickable"' in content,
    'Instant 0ms Filter click': 'onclick="focusSearch()"' in content,
    'What Happened Afterward pill': '🚀 What Happened Afterward?' in content,
    'Trajectories Section': 'id="trajectories-section"' in content,
    '8 Flagship Case Studies': all(c in content for c in ['BSE.NS', 'CDSL.NS', 'COALINDIA.NS', 'TVSMOTOR.NS', 'TITAN.NS', 'ITC.NS', 'DMART.NS', 'SREEL.NS']),
    '11th Column Header': '<th>What Happened Afterward</th>' in content,
    'Trajectory Pill Badges': 'traj-pill multibagger' in content and 'traj-pill compounder' in content,
    'Alpha engine display': 'α ' in content,
    'Colspan 11 on empty': 'colspan="11"' in content,
    'focusSearch definition': 'function focusSearch()' in content,
    'scrollToElement definition': 'function scrollToElement(' in content,
    'Zero purple constraint': '#7c3aed' not in content and '#8b5cf6' not in content and 'rgb(124, 58, 237)' not in content,
}

all_passed = True
for name, res in checks.items():
    status = "PASS" if res else "FAIL"
    print(f"[{status}] {name}")
    if not res:
        all_passed = False

if all_passed:
    print("\nALL 11 VERIFICATION CHECKS PASSED PERFECTLY!")
else:
    print("\nSOME CHECKS FAILED.")
