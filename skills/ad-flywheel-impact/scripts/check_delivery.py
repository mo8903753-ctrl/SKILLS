#!/usr/bin/env python3
"""Verify manifest-selected final assets and optionally package them. Does not perform visual QA."""
import argparse,hashlib,json,zipfile
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('manifest',type=Path);p.add_argument('--zip',dest='zip_path',type=Path);p.add_argument('--require-figma',action='store_true');p.add_argument('--require-generation',action='store_true');a=p.parse_args();root=a.root.resolve()
 mp=a.manifest if a.manifest.is_absolute() else root/a.manifest;data=json.loads(mp.read_text(encoding='utf-8'));rows=data['items'] if isinstance(data,dict) else data
 seen=set();files=[]
 for r in rows:
  ident=r['creative_id']
  if not ident or ident in seen:raise ValueError('Missing or duplicate creative_id: '+str(ident))
  seen.add(ident);rel=Path(r['asset_path'])
  if rel.is_absolute() or '..' in rel.parts:raise ValueError('asset_path must be project-relative: '+str(rel))
  f=(root/rel).resolve()
  if root not in f.parents or not f.is_file():raise ValueError('Missing/outside-root asset: '+str(rel))
  digest=hashlib.sha256(f.read_bytes()).hexdigest()
  if digest!=r['sha256']:raise ValueError('Hash mismatch: '+str(rel))
  if a.require_figma and not r.get('figma_node_id'):raise ValueError('Missing Figma node: '+ident)
  if (r.get('qa_status') or r.get('status')) not in {'passed','visually_reviewed','visually_reviewed_figma_image_node_verified'}:raise ValueError('Not QA-passed: '+ident)
  if a.require_generation:
   g=r.get('generation') or {}
   if r.get('production_method')!='image_generation' or g.get('complete_ad') is not True:raise ValueError('Not a complete generated ad: '+ident)
   if not g.get('tool') or g.get('output_sha256')!=digest:raise ValueError('Missing tool or generation hash mismatch: '+ident)
   def evidence_path(value):
    if not isinstance(value,str) or not value:raise ValueError('Missing generation evidence path: '+ident)
    q=Path(value);resolved=(root/q).resolve()
    if q.is_absolute() or '..' in q.parts or root not in resolved.parents or not resolved.is_file():raise ValueError('Invalid generation evidence path: '+ident)
    return resolved
   prompt=evidence_path(g.get('prompt_path'))
   if not prompt.read_text(encoding='utf-8').strip():raise ValueError('Empty prompt: '+ident)
   record=json.loads(evidence_path(g.get('record_path')).read_text(encoding='utf-8'))
   if record.get('tool')!=g['tool'] or record.get('output_sha256')!=digest:raise ValueError('Generation record mismatch: '+ident)
   inputs=g.get('input_assets')
   if not isinstance(inputs,list) or not inputs:raise ValueError('Missing reference inputs: '+ident)
   for inp in inputs:evidence_path(inp)
  files.append((f,rel.as_posix()))
 if not rows:raise ValueError('Empty delivery')
 if a.zip_path:
  a.zip_path.parent.mkdir(parents=True,exist_ok=True)
  with zipfile.ZipFile(a.zip_path,'w',zipfile.ZIP_DEFLATED) as z:
   for f,rel in files:z.write(f,rel)
   z.writestr('manifest.json',json.dumps(data,ensure_ascii=False,indent=2))
  with zipfile.ZipFile(a.zip_path) as z:
   if z.testzip() is not None:raise ValueError('ZIP integrity failed')
   for f,rel in files:
    if hashlib.sha256(z.read(rel)).hexdigest()!=hashlib.sha256(f.read_bytes()).hexdigest():raise ValueError('ZIP content mismatch')
 print(json.dumps({'unique_final_assets':len(rows),'hashes':'passed','zip':str(a.zip_path) if a.zip_path else None,'figma_presence_checked':a.require_figma,'visual_qa':'not performed by this script'},ensure_ascii=False))
if __name__=='__main__':main()
