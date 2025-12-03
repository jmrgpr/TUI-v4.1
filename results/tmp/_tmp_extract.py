# -*- coding: utf-8 -*-
import ast

def extract_argparse_defaults(script_path):
    defaults = {}
    with open(script_path,'r',encoding='utf-8') as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func,'attr') and node.func.attr=='add_argument':
            args=node.args
            kwargs={}
            for k in node.keywords:
                if hasattr(k,'arg') and k.arg and hasattr(k,'value'):
                    try:
                        kwargs[k.arg]=ast.literal_eval(k.value)
                    except Exception:
                        pass
            if args and isinstance(args[0], ast.Str):
                key=args[0].s.replace('--','')
                if 'default' in kwargs:
                    defaults[key]=kwargs['default']
    return defaults

print('full:', extract_argparse_defaults('scripts/run_full_experiment.py'))
print('search:', extract_argparse_defaults('scripts/run_search_pgf.py'))
print('abl:', extract_argparse_defaults('scripts/run_ablation_quick.py'))
