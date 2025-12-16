from importlib import util
spec = util.spec_from_file_location('consol', 'scripts/consolidate_results.py')
mod = util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.consolidate_csvs(extra_paths=['results/v11'], output='results/master_results.csv')
print('Consolidation done')
