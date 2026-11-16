import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parsePublicationsResponse } from '../src/lib/publication-contract.ts';

const fixture = () => ({
  version: 'synthetic', updatedAt: '', total: 1, offset: 0, limit: 500,
  filterTags: ['EEG'], fields: ['EEG'], years: [2026],
  researchers: [{id:1,slug:'synthetic',name:'Test',paperCount:1,currentPaperCount:1}],
  papers: [{id:'test',num:'01',title:'<script>inert text</script>',authors:'Test',journal:'Test',
    year:2026,type:'journal',citedByCount:0,field:'EEG',tags:['EEG'],isTop:false,
    lead:true,representative:true,researchers:[{id:1,slug:'synthetic',name:'Test'}]}],
});
test('valid API and text containing markup remain data', () => {
  const value = fixture();
  assert.deepEqual(parsePublicationsResponse(value), value);
});
for (const [name, mutate] of [
  ['null researcher', d => d.researchers = [null]],
  ['null paper researcher', d => d.papers[0].researchers = [null]],
  ['object tag', d => d.papers[0].tags = [{}]],
  ['missing authors', d => delete d.papers[0].authors],
  ['negative total', d => d.total = -1],
  ['non-finite count', d => d.researchers[0].paperCount = Infinity],
  ['object metrics', d => d.researchers[0].scholarMetrics = {totalCitations:{}}],
  ['javascript link', d => d.researchers[0].googleScholarUrl = 'javascript:alert(1)'],
  ['protocol-relative avatar', d => d.researchers[0].avatarUrl = '//untrusted.invalid/pixel'],
  ['backslash avatar', d => d.researchers[0].avatarUrl = '/\\untrusted.invalid/pixel'],
  ['data avatar', d => d.researchers[0].avatarUrl = 'data:image/svg+xml,<svg/>'],
  ['invalid collection', d => d.papers = null],
]) {
  test('rejects '+name+' before rendering', () => {
    const value=fixture(); mutate(value);
    assert.throws(() => parsePublicationsResponse(value), /论文数据格式暂时不可用/);
  });
}
test('empty valid catalog renders normally', () => {
  const value=fixture(); value.total=0; value.papers=[]; value.researchers=[];
  assert.equal(parsePublicationsResponse(value).total, 0);
});
