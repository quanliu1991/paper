import json
with open(r'd:\paper\data\pending\2026-10-22.json', encoding='utf-8') as f:
    data = json.load(f)
papers = data['papers']
print('TOTAL', len(papers))
infra = [p for p in papers if p.get('infra_hit')]
other = [p for p in papers if not p.get('infra_hit')]
print('INFRA', len(infra), '| OTHER', len(other))
print('=== INFRA ===')
for p in sorted(infra, key=lambda x: -(x.get('upvotes') or 0)):
    print(p['arxiv_id'], '|', p.get('upvotes'), '|', p['title'][:95])
print('=== OTHER ===')
for p in sorted(other, key=lambda x: -(x.get('upvotes') or 0)):
    print(p['arxiv_id'], '|', p.get('upvotes'), '|', p['title'][:95])
